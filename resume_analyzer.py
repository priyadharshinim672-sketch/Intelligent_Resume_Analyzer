import re

from knowledge_base import (
    JOB_ROLES,
    SKILL_ALIASES,
    PROJECT_SKILL_MAP,
    RELATED_CONCEPTS,
    normalize_text,
    normalize_skill,
    get_role_key,
)


class ResumeAnalyzer:
    """Offline, explainable resume analyzer using only Python built-ins."""

    # Generic words should never dominate a technical resume score.
    GENERIC_TERMS = {
        "programming", "technology", "software", "tools", "projects",
        "experience", "development", "skills", "technical skills",
        "knowledge", "work", "application", "applications", "computer",
    }

    SOFT_SKILLS = {
        "communication", "leadership", "teamwork", "problem solving",
        "time management", "adaptability", "critical thinking",
        "collaboration", "presentation", "decision making",
    }

    def __init__(self):
        self.skill_patterns = {}

        for canonical, aliases in SKILL_ALIASES.items():
            names = set([canonical] + aliases)
            ordered = sorted(
                names,
                key=lambda value: len(normalize_text(value)),
                reverse=True,
            )

            patterns = []
            for name in ordered:
                normalized = normalize_text(name)
                if not normalized:
                    continue
                pattern = r"(?<![a-z0-9])" + re.escape(normalized) + r"(?![a-z0-9])"
                patterns.append((normalized, re.compile(pattern)))

            self.skill_patterns[canonical] = patterns

    def extract_skills(self, text):
        normalized = normalize_text(text)
        found = set()

        for canonical, patterns in self.skill_patterns.items():
            for _, pattern in patterns:
                if pattern.search(normalized):
                    found.add(canonical)
                    break

        return sorted(found)

    def detect_projects(self, resume_text):
        text = normalize_text(resume_text)
        detected = {}

        for project_name, skills in PROJECT_SKILL_MAP.items():
            project_phrase = normalize_text(project_name)
            words = [w for w in project_phrase.split() if len(w) > 2]
            if not words:
                continue

            if project_phrase in text:
                confidence = 1.0
                evidence = "Exact project title detected"
            else:
                matched = sum(
                    1 for word in words
                    if re.search(r"(?<![a-z0-9])" + re.escape(word) + r"(?![a-z0-9])", text)
                )
                confidence = matched / len(words)
                evidence = "Project title keywords detected"

            if confidence >= 0.67:
                detected[project_name] = {
                    "skills": [normalize_skill(s) for s in skills],
                    "evidence": evidence,
                    "confidence": round(confidence, 2),
                }

        return detected

    def identify_role(self, job_role):
        key = get_role_key(job_role)
        role = JOB_ROLES.get(key)
        if not role:
            return None

        return {
            "key": key,
            "role": key,
            "category": role["category"],
            "skills": [normalize_skill(x) for x in role["skills"]],
            "tools": [normalize_skill(x) for x in role["tools"]],
            "concepts": [normalize_skill(x) for x in role["concepts"]],
        }

    def extract_job_description_requirements(self, job_description):
        return set(self.extract_skills(job_description))

    def get_role_knowledge(self, job_role):
        role = self.identify_role(job_role)
        if not role:
            return {
                "known": False,
                "skills": set(),
                "tools": set(),
                "concepts": set(),
            }

        return {
            "known": True,
            "skills": set(role["skills"]),
            "tools": set(role["tools"]),
            "concepts": set(role["concepts"]),
        }

    def extract_job_requirements(self, job_role, job_description):
        explicit = self.extract_job_description_requirements(job_description)
        role = self.get_role_knowledge(job_role)
        role_expected = role["skills"] | role["tools"] | role["concepts"]

        return {
            "explicit": explicit,
            "role_expected": role_expected,
            "known_role": role["known"],
        }

    def classify_requirement(self, skill):
        value = normalize_skill(skill)
        if value in self.GENERIC_TERMS:
            return "generic", 0.0
        if value in self.SOFT_SKILLS:
            return "soft", 0.5

        # Core technical skills and concrete tools are more important.
        role_words = {
            "machine learning", "deep learning", "python", "sql",
            "data preprocessing", "feature engineering", "model evaluation",
            "statistics", "computer vision", "natural language processing",
            "api development", "databases", "programming", "data structures",
            "algorithms", "software testing", "cloud computing", "cybersecurity",
        }
        if value in role_words:
            return "core", 3.0

        return "technical", 2.0

    def requirement_weight(self, skill):
        return self.classify_requirement(skill)[1]

    def weighted_coverage(self, required, matched):
        total = 0.0
        earned = 0.0

        for skill in required:
            weight = self.requirement_weight(skill)
            if weight <= 0:
                continue
            total += weight
            if skill in matched:
                earned += weight

        if total == 0:
            return 0.0
        return (earned / total) * 100

    def find_evidence(self, resume_text, skill):
        text = normalize_text(resume_text)
        aliases = SKILL_ALIASES.get(skill, [skill])

        for alias in sorted(aliases, key=lambda x: len(normalize_text(x)), reverse=True):
            value = normalize_text(alias)
            if not value:
                continue

            pattern = r"(?<![a-z0-9])" + re.escape(value) + r"(?![a-z0-9])"
            match = re.search(pattern, text)
            if match:
                start = max(0, match.start() - 75)
                end = min(len(text), match.end() + 120)
                snippet = text[start:end].strip()
                return re.sub(r"\s+", " ", snippet)

        return ""

    def project_relevance(self, project_skills, explicit_requirements):
        if not project_skills or not explicit_requirements:
            return 0.0
        relevant = project_skills & explicit_requirements
        return self.weighted_coverage(explicit_requirements, relevant)

    def analyze(self, resume_text, job_role, job_description):
        resume_skills = set(self.extract_skills(resume_text))
        requirements = self.extract_job_requirements(job_role, job_description)
        explicit = requirements["explicit"]
        role_expected = requirements["role_expected"]

        projects = self.detect_projects(resume_text)
        project_skills = set()
        for project in projects.values():
            project_skills.update(project["skills"])

        evidence_skills = resume_skills | project_skills
        direct_matches = resume_skills & explicit
        project_only_matches = (project_skills & explicit) - direct_matches
        all_explicit_matches = evidence_skills & explicit
        missing_explicit = explicit - all_explicit_matches
        role_matches = resume_skills & role_expected

        # 60% explicit JD fit, 20% role knowledge fit, 20% practical project evidence.
        # Each component uses its own evidence source so the same evidence is not
        # silently counted twice.
        jd_score = self.weighted_coverage(explicit, direct_matches) if explicit else 0.0
        role_score = self.weighted_coverage(role_expected, role_matches) if role_expected else 0.0

        # Project evidence is judged against the role's expected skills when the
        # role is known; otherwise it is judged against explicit JD requirements.
        project_target = role_expected if role_expected else explicit
        project_score = self.project_relevance(project_skills, project_target)

        if explicit:
            score = (jd_score * 0.60) + (role_score * 0.20) + (project_score * 0.20)
            basis = "Weighted JD + Role Knowledge + Project Evidence"
        elif role_expected:
            score = (role_score * 0.75) + (project_score * 0.25)
            basis = "Weighted Offline Role Knowledge + Project Evidence"
        else:
            score = 0.0
            basis = "No recognizable requirements"

        score = round(min(100.0, score), 2)

        if score >= 85:
            recommendation = "EXCELLENT MATCH"
        elif score >= 70:
            recommendation = "STRONG MATCH"
        elif score >= 55:
            recommendation = "GOOD MATCH"
        elif score >= 40:
            recommendation = "PARTIAL MATCH"
        else:
            recommendation = "LOW MATCH"

        evidence = {}
        for skill in sorted(all_explicit_matches | missing_explicit):
            snippet = self.find_evidence(resume_text, skill)
            evidence[skill] = snippet

        requirement_status = []
        for skill in sorted(explicit):
            category, weight = self.classify_requirement(skill)
            if skill in direct_matches:
                status = "Direct match"
            elif skill in project_only_matches:
                status = "Project evidence"
            else:
                status = "Missing"
            requirement_status.append({
                "skill": skill,
                "status": status,
                "category": category,
                "weight": weight,
            })

        return {
            "job_role": job_role,
            "normalized_role": get_role_key(job_role),
            "role_known": requirements["known_role"],
            "resume_skills": sorted(resume_skills),
            "explicit_requirements": sorted(explicit),
            "role_expected": sorted(role_expected),
            "matched_skills": sorted(direct_matches),
            "project_matches": sorted(project_only_matches),
            "missing_skills": sorted(missing_explicit),
            "role_matches": sorted(role_matches),
            "projects": projects,
            "project_skills": sorted(project_skills),
            "evidence": evidence,
            "requirement_status": requirement_status,
            "jd_score": round(jd_score, 1),
            "role_score": round(role_score, 1),
            "project_score": round(project_score, 1),
            "score": score,
            "recommendation": recommendation,
            "scoring_basis": basis,
        }
