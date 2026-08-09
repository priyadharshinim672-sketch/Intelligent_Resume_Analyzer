"""Offline career knowledge base for Intelligent Resume Analyzer.
Python standard library only. No APIs or external packages are required.
"""

import re

JOB_ROLES = {
    "artificial intelligence engineer": {
        "category": "AI & Machine Learning",
        "skills": ["python", "machine learning", "deep learning", "neural networks",
                   "natural language processing", "computer vision", "statistics"],
        "tools": ["pytorch", "tensorflow", "scikit-learn", "jupyter", "git"],
        "concepts": ["generative ai", "transformers", "large language models",
                     "reinforcement learning", "model deployment"]
    },
    "machine learning engineer": {
        "category": "AI & Machine Learning",
        "skills": ["python", "machine learning", "statistics", "data preprocessing",
                   "feature engineering", "model evaluation", "deep learning"],
        "tools": ["pytorch", "tensorflow", "scikit-learn", "mlflow", "git"],
        "concepts": ["classification", "regression", "clustering", "model training",
                     "model deployment", "mlops"]
    },
    "data scientist": {
        "category": "Data & AI",
        "skills": ["python", "sql", "statistics", "machine learning", "data analysis",
                   "data visualization", "feature engineering"],
        "tools": ["pandas", "numpy", "jupyter", "power bi", "tableau", "git"],
        "concepts": ["eda", "classification", "regression", "clustering",
                     "predictive modeling", "hypothesis testing"]
    },
    "data analyst": {
        "category": "Data & Analytics",
        "skills": ["sql", "python", "excel", "data analysis", "statistics",
                   "data visualization"],
        "tools": ["power bi", "tableau", "pandas", "excel"],
        "concepts": ["eda", "dashboard", "reporting", "business intelligence",
                     "data cleaning"]
    },
    "business intelligence analyst": {
        "category": "Data & Analytics",
        "skills": ["sql", "data analysis", "business intelligence", "statistics"],
        "tools": ["power bi", "tableau", "excel", "sql server"],
        "concepts": ["dashboard", "reporting", "data warehouse", "kpi", "etl"]
    },
    "business analyst": {
        "category": "Business Technology",
        "skills": ["requirements analysis", "data analysis", "sql", "communication",
                   "problem solving"],
        "tools": ["excel", "power bi", "jira"],
        "concepts": ["requirements gathering", "process modeling",
                     "stakeholder management", "business intelligence"]
    },
    "data engineer": {
        "category": "Data Engineering",
        "skills": ["python", "sql", "etl", "databases", "data pipelines",
                   "data warehousing"],
        "tools": ["spark", "hadoop", "airflow", "kafka", "aws", "azure"],
        "concepts": ["big data", "data lake", "data warehouse",
                     "batch processing", "stream processing"]
    },
    "big data engineer": {
        "category": "Data Engineering",
        "skills": ["python", "java", "sql", "big data", "distributed systems"],
        "tools": ["hadoop", "spark", "hive", "kafka", "airflow"],
        "concepts": ["hdfs", "mapreduce", "stream processing", "data pipelines"]
    },
    "analytics engineer": {
        "category": "Data Engineering",
        "skills": ["sql", "data modeling", "data analysis", "data warehousing"],
        "tools": ["dbt", "snowflake", "bigquery", "git"],
        "concepts": ["etl", "elt", "dimensional modeling", "data transformation"]
    },
    "database developer": {
        "category": "Database",
        "skills": ["sql", "database design", "data modeling"],
        "tools": ["mysql", "postgresql", "oracle", "sql server"],
        "concepts": ["stored procedures", "triggers", "query optimization", "normalization"]
    },
    "database administrator": {
        "category": "Database",
        "skills": ["sql", "database administration", "database security"],
        "tools": ["mysql", "postgresql", "oracle", "sql server"],
        "concepts": ["backup", "recovery", "replication", "performance tuning"]
    },
    "software engineer": {
        "category": "Software Development",
        "skills": ["programming", "data structures", "algorithms",
                   "object oriented programming", "debugging", "testing"],
        "tools": ["git", "github", "gitlab", "vscode"],
        "concepts": ["software development", "version control", "code review",
                     "problem solving"]
    },
    "software developer": {
        "category": "Software Development",
        "skills": ["programming", "data structures", "algorithms",
                   "object oriented programming", "debugging"],
        "tools": ["git", "github", "vscode"],
        "concepts": ["software development", "testing", "version control"]
    },
    "application developer": {
        "category": "Software Development",
        "skills": ["programming", "software development", "databases",
                   "api development", "testing"],
        "tools": ["git", "vscode"],
        "concepts": ["application development", "debugging", "version control"]
    },
    "systems software developer": {
        "category": "Software Development",
        "skills": ["c", "c++", "data structures", "operating systems",
                   "computer architecture"],
        "tools": ["gcc", "git", "linux"],
        "concepts": ["system programming", "memory management", "concurrency"]
    },
    "embedded software engineer": {
        "category": "Embedded Systems",
        "skills": ["c", "c++", "embedded systems", "microcontrollers",
                   "electronics", "debugging"],
        "tools": ["arduino", "stm32", "keil", "git"],
        "concepts": ["firmware", "rtos", "interrupts", "serial communication"]
    },
    "firmware engineer": {
        "category": "Embedded Systems",
        "skills": ["c", "c++", "embedded systems", "microcontrollers", "electronics"],
        "tools": ["stm32", "arduino", "keil", "gcc"],
        "concepts": ["firmware", "device drivers", "interrupts", "rtos"]
    },
    "mobile app developer": {
        "category": "Mobile Development",
        "skills": ["mobile development", "programming", "api development", "databases"],
        "tools": ["android studio", "flutter", "react native", "git"],
        "concepts": ["android", "ios", "mobile ui", "app deployment"]
    },
    "android developer": {
        "category": "Mobile Development",
        "skills": ["kotlin", "java", "android development", "api development"],
        "tools": ["android studio", "gradle", "git"],
        "concepts": ["android sdk", "mobile ui", "app lifecycle"]
    },
    "ios developer": {
        "category": "Mobile Development",
        "skills": ["swift", "ios development", "mobile development", "api development"],
        "tools": ["xcode", "git"],
        "concepts": ["swiftui", "uikit", "app lifecycle"]
    },
    "frontend developer": {
        "category": "Web Development",
        "skills": ["html", "css", "javascript", "typescript", "web development"],
        "tools": ["react", "angular", "vue", "git"],
        "concepts": ["responsive design", "ui development", "web accessibility"]
    },
    "backend developer": {
        "category": "Web Development",
        "skills": ["programming", "api development", "databases", "backend development"],
        "tools": ["node.js", "django", "flask", "spring", "git"],
        "concepts": ["rest api", "authentication", "server", "microservices"]
    },
    "full stack developer": {
        "category": "Web Development",
        "skills": ["html", "css", "javascript", "frontend development",
                   "backend development", "databases"],
        "tools": ["react", "node.js", "python", "django", "git"],
        "concepts": ["rest api", "web application", "authentication"]
    },
    "web developer": {
        "category": "Web Development",
        "skills": ["html", "css", "javascript", "web development"],
        "tools": ["react", "angular", "vue", "git"],
        "concepts": ["frontend", "backend", "responsive design"]
    },
    "react developer": {
        "category": "Web Development",
        "skills": ["javascript", "typescript", "react", "html", "css"],
        "tools": ["npm", "git", "webpack"],
        "concepts": ["components", "state management", "frontend"]
    },
    "node.js developer": {
        "category": "Web Development",
        "skills": ["javascript", "node.js", "api development", "databases"],
        "tools": ["npm", "express", "git", "mongodb"],
        "concepts": ["rest api", "backend", "microservices"]
    },
    "cloud engineer": {
        "category": "Cloud Computing",
        "skills": ["cloud computing", "linux", "networking", "virtualization", "automation"],
        "tools": ["aws", "azure", "google cloud", "docker", "kubernetes"],
        "concepts": ["cloud architecture", "scalability", "deployment"]
    },
    "cloud architect": {
        "category": "Cloud Computing",
        "skills": ["cloud architecture", "networking", "security",
                   "distributed systems"],
        "tools": ["aws", "azure", "google cloud", "terraform"],
        "concepts": ["high availability", "scalability", "disaster recovery"]
    },
    "devops engineer": {
        "category": "DevOps",
        "skills": ["linux", "git", "automation", "cloud computing", "containerization"],
        "tools": ["docker", "kubernetes", "jenkins", "terraform", "aws"],
        "concepts": ["ci/cd", "continuous integration", "continuous deployment",
                     "infrastructure as code"]
    },
    "site reliability engineer": {
        "category": "DevOps & Reliability",
        "skills": ["linux", "cloud computing", "automation", "networking", "monitoring"],
        "tools": ["kubernetes", "docker", "prometheus", "grafana"],
        "concepts": ["reliability", "observability", "incident management", "scalability"]
    },
    "platform engineer": {
        "category": "Cloud & Platform",
        "skills": ["cloud computing", "linux", "automation", "containerization"],
        "tools": ["kubernetes", "docker", "terraform", "jenkins"],
        "concepts": ["platform engineering", "infrastructure as code",
                     "developer experience"]
    },
    "cloud security engineer": {
        "category": "Cloud Security",
        "skills": ["cloud security", "cybersecurity", "network security",
                   "identity management"],
        "tools": ["aws", "azure", "kubernetes"],
        "concepts": ["iam", "zero trust", "security monitoring"]
    },
    "cybersecurity analyst": {
        "category": "Cybersecurity",
        "skills": ["cybersecurity", "network security", "linux",
                   "risk assessment", "security analysis"],
        "tools": ["wireshark", "splunk", "nmap", "metasploit"],
        "concepts": ["vulnerability assessment", "incident response",
                     "security monitoring"]
    },
    "security engineer": {
        "category": "Cybersecurity",
        "skills": ["cybersecurity", "network security", "secure coding", "cryptography"],
        "tools": ["wireshark", "nmap", "splunk"],
        "concepts": ["security architecture", "threat modeling", "incident response"]
    },
    "penetration tester": {
        "category": "Cybersecurity",
        "skills": ["ethical hacking", "penetration testing", "network security",
                   "linux", "web security"],
        "tools": ["burp suite", "metasploit", "nmap", "wireshark"],
        "concepts": ["vulnerability assessment", "exploitation", "web security"]
    },
    "security operations analyst": {
        "category": "Cybersecurity",
        "skills": ["cybersecurity", "security monitoring", "incident response",
                   "network security"],
        "tools": ["splunk", "wireshark"],
        "concepts": ["soc", "siem", "threat detection"]
    },
    "network engineer": {
        "category": "Networking",
        "skills": ["computer networks", "tcp/ip", "routing", "switching",
                   "network security"],
        "tools": ["cisco ios", "wireshark", "packet tracer"],
        "concepts": ["lan", "wan", "vpn", "dns", "dhcp"]
    },
    "network administrator": {
        "category": "Networking",
        "skills": ["networking", "linux", "tcp/ip", "network security"],
        "tools": ["wireshark", "packet tracer"],
        "concepts": ["routing", "switching", "dns", "dhcp", "vpn"]
    },
    "qa engineer": {
        "category": "Quality Assurance",
        "skills": ["software testing", "test automation", "debugging",
                   "programming", "quality assurance"],
        "tools": ["selenium", "jira", "git"],
        "concepts": ["test cases", "regression testing", "integration testing"]
    },
    "software test engineer": {
        "category": "Quality Assurance",
        "skills": ["software testing", "test automation", "debugging"],
        "tools": ["selenium", "postman", "jira"],
        "concepts": ["unit testing", "integration testing", "regression testing"]
    },
    "automation test engineer": {
        "category": "Quality Assurance",
        "skills": ["test automation", "software testing", "programming"],
        "tools": ["selenium", "cypress", "playwright", "pytest"],
        "concepts": ["automated testing", "regression testing", "ci/cd"]
    },
    "blockchain developer": {
        "category": "Blockchain",
        "skills": ["blockchain", "programming", "cryptography", "smart contracts"],
        "tools": ["solidity", "ethereum", "web3.js", "git"],
        "concepts": ["distributed ledger", "smart contract", "consensus"]
    },
    "smart contract developer": {
        "category": "Blockchain",
        "skills": ["solidity", "blockchain", "smart contracts", "cryptography"],
        "tools": ["ethereum", "hardhat", "web3.js"],
        "concepts": ["ethereum", "decentralized applications", "defi"]
    },
    "iot engineer": {
        "category": "IoT",
        "skills": ["iot", "embedded systems", "python", "c", "networking"],
        "tools": ["arduino", "raspberry pi", "mqtt"],
        "concepts": ["sensors", "edge computing", "device communication"]
    },
    "robotics engineer": {
        "category": "Robotics & AI",
        "skills": ["python", "c++", "robotics", "control systems",
                   "computer vision", "linear algebra"],
        "tools": ["ros", "gazebo", "opencv", "git"],
        "concepts": ["path planning", "slam", "sensor fusion",
                     "motion planning", "autonomous systems"]
    },
    "computer vision engineer": {
        "category": "AI & Machine Learning",
        "skills": ["python", "computer vision", "deep learning",
                   "image processing", "machine learning", "linear algebra"],
        "tools": ["pytorch", "tensorflow", "opencv", "jupyter"],
        "concepts": ["image classification", "object detection",
                     "image segmentation", "ocr", "face recognition"]
    },
    "nlp engineer": {
        "category": "AI & Machine Learning",
        "skills": ["python", "natural language processing",
                   "machine learning", "deep learning", "statistics"],
        "tools": ["pytorch", "tensorflow", "jupyter"],
        "concepts": ["text classification", "named entity recognition",
                     "sentiment analysis", "tokenization", "transformers"]
    },
    "generative ai engineer": {
        "category": "Generative AI",
        "skills": ["python", "generative ai", "machine learning",
                   "deep learning", "natural language processing"],
        "tools": ["pytorch", "tensorflow", "git"],
        "concepts": ["large language models", "prompt engineering", "rag",
                     "embeddings", "vector databases", "fine tuning",
                     "transformers", "agents"]
    },
    "llm engineer": {
        "category": "Generative AI",
        "skills": ["python", "large language models",
                   "natural language processing", "machine learning", "deep learning"],
        "tools": ["pytorch", "hugging face", "git"],
        "concepts": ["rag", "prompt engineering", "embeddings",
                     "fine tuning", "transformers", "vector databases", "evaluation"]
    },
    "ai research scientist": {
        "category": "AI Research",
        "skills": ["python", "machine learning", "deep learning",
                   "mathematics", "statistics", "research"],
        "tools": ["pytorch", "tensorflow", "jupyter"],
        "concepts": ["optimization", "representation learning",
                     "generative models", "reinforcement learning"]
    },
    "vlsi engineer": {
        "category": "VLSI",
        "skills": ["digital electronics", "verilog", "vhdl", "computer architecture"],
        "tools": ["vivado", "quartus"],
        "concepts": ["fpga", "asic", "rtl design", "verification"]
    },
    "hardware engineer": {
        "category": "Hardware",
        "skills": ["digital electronics", "computer architecture",
                   "microprocessors", "embedded systems"],
        "tools": ["verilog", "vhdl", "vivado"],
        "concepts": ["fpga", "asic", "pcb", "digital logic"]
    },
    "ui ux designer": {
        "category": "Design & Technology",
        "skills": ["ui design", "ux design", "user research",
                   "interaction design", "prototyping"],
        "tools": ["figma", "adobe xd", "sketch"],
        "concepts": ["wireframe", "usability", "design system"]
    },
    "technical product manager": {
        "category": "Product & Technology",
        "skills": ["product management", "requirements analysis",
                   "communication", "data analysis"],
        "tools": ["jira", "confluence", "excel"],
        "concepts": ["roadmap", "product strategy", "user stories", "kpi"]
    },
    "technical project manager": {
        "category": "Project Management",
        "skills": ["project management", "communication",
                   "requirements analysis", "risk management"],
        "tools": ["jira", "confluence", "trello"],
        "concepts": ["agile", "scrum", "project planning", "stakeholder management"]
    }
}

# Canonical skill -> aliases. Add aliases here instead of changing analyzer code.
SKILL_ALIASES = {
    "python": ["python", "python programming", "python3", "py"],
    "machine learning": ["machine learning", "ml", "machine-learning",
                         "predictive modeling", "predictive modelling"],
    "deep learning": ["deep learning", "dl", "deep neural networks", "dnn"],
    "artificial intelligence": ["artificial intelligence", "ai"],
    "natural language processing": ["natural language processing", "nlp"],
    "computer vision": ["computer vision", "cv", "image understanding"],
    "generative ai": ["generative ai", "genai", "gen ai"],
    "large language models": ["large language model", "large language models",
                              "llm", "llms"],
    "prompt engineering": ["prompt engineering", "prompt design", "prompting"],
    "retrieval augmented generation": ["retrieval augmented generation", "rag"],
    "vector databases": ["vector database", "vector databases", "vector db"],
    "fine tuning": ["fine tuning", "fine-tuning", "finetuning"],
    "transformers": ["transformer", "transformers"],
    "reinforcement learning": ["reinforcement learning", "rl"],
    "data analysis": ["data analysis", "data analytics", "data analysing",
                      "analytical skills"],
    "data visualization": ["data visualization", "data visualisation", "data viz"],
    "exploratory data analysis": ["exploratory data analysis", "eda"],
    "business intelligence": ["business intelligence", "bi"],
    "power bi": ["power bi", "powerbi"],
    "microsoft excel": ["microsoft excel", "excel", "ms excel"],
    "amazon web services": ["amazon web services", "aws"],
    "microsoft azure": ["microsoft azure", "azure"],
    "google cloud platform": ["google cloud platform", "google cloud", "gcp"],
    "docker": ["docker", "docker containers"],
    "kubernetes": ["kubernetes", "k8s"],
    "continuous integration": ["continuous integration", "ci"],
    "continuous deployment": ["continuous deployment", "cd"],
    "infrastructure as code": ["infrastructure as code", "iac"],
    "node.js": ["node.js", "nodejs", "node js"],
    "react": ["react", "react.js", "reactjs"],
    "angular": ["angular", "angularjs"],
    "vue": ["vue", "vue.js", "vuejs"],
    "rest api": ["rest api", "restful api", "rest services", "restful services"],
    "mysql": ["mysql", "my sql"],
    "postgresql": ["postgresql", "postgres", "postgre sql"],
    "microsoft sql server": ["microsoft sql server", "sql server", "mssql"],
    "mongodb": ["mongodb", "mongo db", "mongo"],
    "apache spark": ["apache spark", "spark"],
    "apache hadoop": ["apache hadoop", "hadoop"],
    "apache kafka": ["apache kafka", "kafka"],
    "apache airflow": ["apache airflow", "airflow"],
    "git": ["git", "git version control"],
    "github": ["github", "git hub"],
    "cybersecurity": ["cybersecurity", "cyber security", "information security"],
    "network security": ["network security"],
    "penetration testing": ["penetration testing", "pentesting", "pen testing"],
    "ethical hacking": ["ethical hacking", "ethical hacker"],
    "object oriented programming": ["object oriented programming",
                                     "oop", "object-oriented programming"],
    "data structures": ["data structures", "data structure"],
    "algorithms": ["algorithms", "algorithm", "algorithm design"],
    "embedded systems": ["embedded systems", "embedded system"],
    "internet of things": ["internet of things", "iot"],
    "robotics": ["robotics", "robotic systems"],
    "user experience design": ["user experience design", "ux design", "ux"],
    "user interface design": ["user interface design", "ui design", "ui"],
    "c++": ["c++", "cpp"],
    "javascript": ["javascript", "js"],
    "typescript": ["typescript", "ts"],
    "java": ["java", "java programming"],
    "c": ["c", "c programming"],
    "sql": ["sql", "structured query language"],
    "statistics": ["statistics", "statistical analysis"],
    "html": ["html", "html5"],
    "css": ["css", "css3"],
    "tableau": ["tableau"],
    "pytorch": ["pytorch", "torch"],
    "tensorflow": ["tensorflow"],
    "scikit-learn": ["scikit-learn", "sklearn"],
    "opencv": ["opencv", "open cv"],
    "mlops": ["mlops", "ml ops", "machine learning operations"],
    "data preprocessing": ["data preprocessing", "data pre-processing"],
    "feature engineering": ["feature engineering"],
    "model evaluation": ["model evaluation", "model validation"],
    "classification": ["classification", "classification algorithms"],
    "regression": ["regression", "regression analysis"],
    "clustering": ["clustering", "cluster analysis"],
    "time series": ["time series", "time-series"],
    "data cleaning": ["data cleaning", "data cleansing"],
    "etl": ["etl", "extract transform load", "extract-transform-load"],
    "data pipelines": ["data pipeline", "data pipelines"],
    "data warehousing": ["data warehouse", "data warehousing"],
    "big data": ["big data", "big-data"],
    "distributed systems": ["distributed systems", "distributed computing"],
    "operating systems": ["operating systems", "os"],
    "computer architecture": ["computer architecture"],
    "linux": ["linux", "ubuntu"],
    "networking": ["networking", "computer networking"],
    "api development": ["api development", "api design", "apis"],
    "databases": ["database", "databases", "dbms"],
    "programming": ["programming", "software programming", "coding"],
    "software testing": ["software testing", "testing", "software test"],
    "test automation": ["test automation", "automated testing", "automation testing"],
    "quality assurance": ["quality assurance", "qa"],
    "communication": ["communication", "communication skills"],
    "problem solving": ["problem solving", "problem-solving"],
    "agile": ["agile", "agile methodology"],
    "scrum": ["scrum"],
    "solidity": ["solidity"],
    "blockchain": ["blockchain", "block chain"],
    "smart contracts": ["smart contract", "smart contracts"],
    "cryptography": ["cryptography", "cryptographic"],
    "embedded systems": ["embedded systems", "embedded system"],
    "microcontrollers": ["microcontroller", "microcontrollers"],
    "firmware": ["firmware"],
    "electronics": ["electronics", "electronic systems"],
    "verilog": ["verilog"],
    "vhdl": ["vhdl"],
    "digital electronics": ["digital electronics"],
    "figma": ["figma"],
    "jira": ["jira"],
    "confluence": ["confluence"],
    "research": ["research", "research experience"],
    "mathematics": ["mathematics", "mathematical"],
    "linear algebra": ["linear algebra"],
}

ROLE_ALIASES = {
    "ai engineer": "artificial intelligence engineer",
    "ai developer": "artificial intelligence engineer",
    "ai/ ml engineer": "machine learning engineer",
    "ml engineer": "machine learning engineer",
    "ml developer": "machine learning engineer",
    "machine learning developer": "machine learning engineer",
    "data science intern": "data scientist",
    "data scientist intern": "data scientist",
    "data analyst intern": "data analyst",
    "sde": "software engineer",
    "software development engineer": "software engineer",
    "software engineer intern": "software engineer",
    "frontend engineer": "frontend developer",
    "front end developer": "frontend developer",
    "backend engineer": "backend developer",
    "back end developer": "backend developer",
    "fullstack developer": "full stack developer",
    "full stack engineer": "full stack developer",
    "devops": "devops engineer",
    "cloud developer": "cloud engineer",
    "security analyst": "cybersecurity analyst",
    "cyber security analyst": "cybersecurity analyst",
    "qa tester": "qa engineer",
    "test engineer": "software test engineer",
    "android engineer": "android developer",
    "ios engineer": "ios developer",
    "embedded engineer": "embedded software engineer",
    "gen ai engineer": "generative ai engineer",
    "generative ai developer": "generative ai engineer",
    "llm developer": "llm engineer",
    "computer vision developer": "computer vision engineer",
    "nlp developer": "nlp engineer",
}

PROJECT_SKILL_MAP = {
    "chatbot": ["python", "natural language processing", "machine learning",
                "generative ai", "large language models"],
    "customer support chatbot": ["python", "natural language processing",
                                 "generative ai", "large language models", "rest api"],
    "recommendation system": ["machine learning", "data analysis",
                              "statistics", "python"],
    "fraud detection": ["machine learning", "classification",
                        "statistics", "data analysis", "python"],
    "sentiment analysis": ["natural language processing",
                           "machine learning", "text classification", "python"],
    "face recognition": ["computer vision", "deep learning",
                         "image processing", "python"],
    "object detection": ["computer vision", "deep learning",
                         "image processing", "python"],
    "image classification": ["computer vision", "deep learning",
                             "machine learning", "python"],
    "image segmentation": ["computer vision", "deep learning", "image processing"],
    "ocr": ["computer vision", "image processing", "natural language processing"],
    "sales dashboard": ["data analysis", "data visualization",
                        "business intelligence", "sql", "power bi"],
    "student performance analytics": ["data analysis", "sql", "statistics",
                                      "python", "data visualization"],
    "predictive maintenance": ["machine learning", "time series",
                               "data analysis", "predictive modeling"],
    "stock prediction": ["machine learning", "time series", "statistics",
                          "data analysis", "python"],
    "weather prediction": ["machine learning", "statistics",
                            "data analysis", "time series"],
    "web application": ["html", "css", "javascript",
                        "frontend development", "backend development", "databases"],
    "ecommerce website": ["html", "css", "javascript",
                          "backend development", "databases", "rest api"],
    "mobile application": ["mobile development", "api development", "databases"],
    "travel planner": ["python", "algorithms", "data analysis",
                       "recommendation systems"],
    "data pipeline": ["python", "sql", "etl", "data engineering",
                      "data pipelines", "databases"],
    "data warehouse": ["sql", "data warehousing", "data modeling", "etl"],
    "iot monitoring": ["internet of things", "embedded systems",
                       "sensors", "networking", "python"],
    "smart home": ["internet of things", "embedded systems",
                   "sensors", "networking"],
    "robot navigation": ["robotics", "computer vision",
                         "path planning", "slam", "c++"],
    "blockchain application": ["blockchain", "smart contracts",
                               "solidity", "cryptography"],
    "cloud deployment": ["cloud computing", "docker", "kubernetes",
                         "continuous deployment"],
    "devops pipeline": ["devops", "git", "docker",
                        "continuous integration", "continuous deployment"],
    "resume analyzer": ["python", "natural language processing",
                        "text processing", "information extraction"],
}

RELATED_CONCEPTS = {
    "machine learning": ["classification", "regression", "clustering",
                         "feature engineering", "model evaluation",
                         "predictive modeling", "supervised learning",
                         "unsupervised learning"],
    "deep learning": ["neural networks", "cnn", "rnn", "lstm",
                      "transformers", "backpropagation"],
    "natural language processing": ["text classification", "sentiment analysis",
                                    "named entity recognition", "tokenization",
                                    "language models", "embeddings"],
    "computer vision": ["image classification", "object detection",
                        "image segmentation", "ocr", "face recognition"],
    "generative ai": ["large language models", "prompt engineering", "rag",
                      "embeddings", "fine tuning", "agents"],
    "data analysis": ["data cleaning", "eda", "statistics",
                      "data visualization", "reporting"],
    "data engineering": ["etl", "elt", "data pipelines", "data warehouse",
                         "data lake", "batch processing", "stream processing"],
    "web development": ["frontend", "backend", "api", "database",
                        "responsive design"],
    "devops": ["ci/cd", "automation", "docker", "kubernetes",
               "infrastructure as code", "monitoring"],
    "cybersecurity": ["network security", "vulnerability assessment",
                      "penetration testing", "incident response",
                      "security monitoring"],
}

def normalize_text(text):
    text = str(text).lower()
    text = text.replace("&", " and ")
    text = text.replace("–", "-").replace("—", "-")
    text = re.sub(r"[^a-z0-9+#./-]+", " ", text)
    return re.sub(r"\s+", " ", text).strip()

SKILL_ALIAS_LOOKUP = {}

for canonical, names in SKILL_ALIASES.items():
    SKILL_ALIAS_LOOKUP[normalize_text(canonical)] = canonical
    for name in names:
        SKILL_ALIAS_LOOKUP[normalize_text(name)] = canonical

def normalize_skill(skill):
    value = normalize_text(skill)
    return SKILL_ALIAS_LOOKUP.get(value, value)

def get_role(role):
    key = normalize_text(role)
    key = ROLE_ALIASES.get(key, key)
    return JOB_ROLES.get(key)

def get_role_key(role):
    key = normalize_text(role)
    return ROLE_ALIASES.get(key, key)

def get_role_requirements(role):
    data = get_role(role)
    if not data:
        return set()
    values = data["skills"] + data["tools"] + data["concepts"]
    return {normalize_skill(x) for x in values}

def get_role_names():
    return sorted(JOB_ROLES.keys())
