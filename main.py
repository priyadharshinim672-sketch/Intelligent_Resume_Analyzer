import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from pathlib import Path
import re
import zlib

from knowledge_base import get_role, get_role_key, get_role_names
from resume_analyzer import ResumeAnalyzer


class ResumeAnalyzerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Intelligent Resume Analyzer")
        self.root.geometry("1100x850")
        self.root.minsize(950, 750)

        self.selected_file = None
        self.file_type = None
        self.analyzer = ResumeAnalyzer()

        self.setup_window()
        self.create_header()
        self.create_job_input_section()
        self.create_upload_section()
        self.create_status_section()
        self.create_footer()

    # =========================================================
    # WINDOW
    # =========================================================

    def setup_window(self):
        self.root.configure(bg="#0F172A")

    # =========================================================
    # HEADER
    # =========================================================

    def create_header(self):
        header = tk.Frame(self.root, bg="#0F172A")
        header.pack(fill="x", padx=50, pady=(25, 8))

        tk.Label(
            header,
            text="INTELLIGENT RESUME ANALYZER",
            font=("Segoe UI", 25, "bold"),
            fg="#F8FAFC",
            bg="#0F172A",
        ).pack()

        tk.Label(
            header,
            text="Offline • Evidence-Based • Job-Specific Candidate Screening",
            font=("Segoe UI", 11),
            fg="#94A3B8",
            bg="#0F172A",
        ).pack(pady=(4, 7))

        tk.Label(
            header,
            text="Developed by Priyadharshini  •  AI & Data Science  •  3rd Year",
            font=("Segoe UI", 9),
            fg="#CBD5E1",
            bg="#0F172A",
        ).pack()

    # =========================================================
    # JOB INPUT
    # =========================================================

    def create_job_input_section(self):
        section = tk.Frame(self.root, bg="#1E293B")
        section.pack(fill="x", padx=55, pady=15)

        tk.Label(
            section,
            text="JOB ROLE",
            font=("Segoe UI", 11, "bold"),
            fg="#E2E8F0",
            bg="#1E293B",
        ).pack(anchor="w", padx=20, pady=(14, 5))

        role_row = tk.Frame(section, bg="#1E293B")
        role_row.pack(fill="x", padx=20)

        self.role_entry = tk.Entry(
            role_row,
            font=("Segoe UI", 11),
            bg="#0F172A",
            fg="#F8FAFC",
            insertbackground="white",
            relief="flat",
        )
        self.role_entry.pack(side="left", fill="x", expand=True, ipady=9)

        self.role_status = tk.Label(
            role_row,
            text="",
            font=("Segoe UI", 9, "bold"),
            bg="#1E293B",
            fg="#94A3B8",
            width=22,
            anchor="w",
        )
        self.role_status.pack(side="left", padx=(12, 0))

        self.role_entry.bind("<KeyRelease>", self.update_role_status)

        tk.Label(
            section,
            text="JOB DESCRIPTION",
            font=("Segoe UI", 11, "bold"),
            fg="#E2E8F0",
            bg="#1E293B",
        ).pack(anchor="w", padx=20, pady=(14, 5))

        self.jd_text = tk.Text(
            section,
            height=5,
            wrap="word",
            font=("Segoe UI", 10),
            bg="#0F172A",
            fg="#F8FAFC",
            insertbackground="white",
            relief="flat",
            padx=10,
            pady=10,
        )
        self.jd_text.pack(fill="x", padx=20, pady=(0, 15))

        tk.Label(
            section,
            text="Tip: You can enter any role. The offline knowledge base is used when the role is recognized.",
            font=("Segoe UI", 8),
            fg="#64748B",
            bg="#1E293B",
        ).pack(anchor="w", padx=20, pady=(0, 12))

    def update_role_status(self, event=None):
        role = self.role_entry.get().strip()

        if not role:
            self.role_status.config(text="")
            return

        if get_role(role):
            normalized = get_role_key(role)
            self.role_status.config(
                text=f"✓ Offline role: {normalized}",
                fg="#34D399",
            )
        else:
            self.role_status.config(
                text="• JD-based analysis",
                fg="#FBBF24",
            )

    # =========================================================
    # UPLOAD SECTION
    # =========================================================

    def create_upload_section(self):
        section = tk.Frame(self.root, bg="#0F172A")
        section.pack(fill="both", expand=True, padx=55, pady=10)

        tk.Label(
            section,
            text="UPLOAD CANDIDATE RESUME",
            font=("Segoe UI", 13, "bold"),
            fg="#E2E8F0",
            bg="#0F172A",
        ).pack(pady=(5, 14))

        cards = tk.Frame(section, bg="#0F172A")
        cards.pack()

        self.create_upload_card(
            cards,
            "TEXT RESUME",
            "Upload a .txt resume",
            "#38BDF8",
            "#0284C7",
            self.select_text_resume,
        )

        self.create_upload_card(
            cards,
            "PDF RESUME",
            "Text is extracted using Python built-ins",
            "#A78BFA",
            "#7C3AED",
            self.select_pdf_resume,
        )

    def create_upload_card(
        self,
        parent,
        title,
        description,
        title_color,
        button_color,
        command,
    ):
        card = tk.Frame(
            parent,
            bg="#1E293B",
            width=340,
            height=165,
        )
        card.pack(side="left", padx=15)
        card.pack_propagate(False)

        tk.Label(
            card,
            text=title,
            font=("Segoe UI", 16, "bold"),
            fg=title_color,
            bg="#1E293B",
        ).pack(pady=(20, 5))

        tk.Label(
            card,
            text=description,
            font=("Segoe UI", 9),
            fg="#CBD5E1",
            bg="#1E293B",
        ).pack()

        tk.Button(
            card,
            text="SELECT FILE",
            command=command,
            font=("Segoe UI", 9, "bold"),
            bg=button_color,
            fg="white",
            activebackground=button_color,
            relief="flat",
            cursor="hand2",
            padx=25,
            pady=8,
        ).pack(pady=17)

    # =========================================================
    # FILE SELECTION
    # =========================================================

    def select_text_resume(self):
        file_path = filedialog.askopenfilename(
            title="Select Text Resume",
            filetypes=[("Text Files", "*.txt")],
        )

        if file_path:
            self.selected_file = file_path
            self.file_type = "text"
            self.update_status()

    def select_pdf_resume(self):
        file_path = filedialog.askopenfilename(
            title="Select PDF Resume",
            filetypes=[("PDF Files", "*.pdf")],
        )

        if file_path:
            self.selected_file = file_path
            self.file_type = "pdf"
            self.update_status()

    # =========================================================
    # STATUS
    # =========================================================

    def create_status_section(self):
        frame = tk.Frame(self.root, bg="#1E293B")
        frame.pack(fill="x", padx=55, pady=(5, 15))

        self.status_label = tk.Label(
            frame,
            text="Resume: Not Selected",
            font=("Segoe UI", 10),
            fg="#CBD5E1",
            bg="#1E293B",
        )
        self.status_label.pack(pady=(12, 7))

        self.analyze_button = tk.Button(
            frame,
            text="ANALYZE RESUME",
            command=self.analyze_resume,
            font=("Segoe UI", 11, "bold"),
            bg="#10B981",
            fg="white",
            activebackground="#059669",
            relief="flat",
            cursor="hand2",
            padx=35,
            pady=9,
        )
        self.analyze_button.pack(pady=(0, 14))

    def update_status(self):
        file_name = Path(self.selected_file).name

        self.status_label.config(
            text=f"Resume: {file_name}   |   Format: {self.file_type.upper()}",
            fg="#34D399",
        )

    # =========================================================
    # ANALYSIS
    # =========================================================

    def analyze_resume(self):
        role = self.role_entry.get().strip()
        description = self.jd_text.get("1.0", "end").strip()

        if not role:
            messagebox.showwarning(
                "Job Role Required",
                "Please enter the job role.",
            )
            return

        if not description:
            messagebox.showwarning(
                "Job Description Required",
                "Please enter the job description.",
            )
            return

        if not self.selected_file:
            messagebox.showwarning(
                "Resume Required",
                "Please upload a candidate resume.",
            )
            return

        try:
            if self.file_type == "text":
                resume_text = self.read_text_resume()
            else:
                resume_text = self.read_pdf_resume()

            if not resume_text.strip():
                raise ValueError("No readable resume text was extracted.")

            result = self.analyzer.analyze(
                resume_text,
                role,
                description,
            )

            self.show_analysis_result(result, resume_text)

        except Exception as error:
            messagebox.showerror(
                "Analysis Error",
                str(error),
            )

    # =========================================================
    # TEXT BACKEND
    # =========================================================

    def read_text_resume(self):
        with open(
            self.selected_file,
            "r",
            encoding="utf-8",
            errors="replace",
        ) as file:
            return file.read()

    # =========================================================
    # PDF BACKEND
    # =========================================================

    def read_pdf_resume(self):
        with open(self.selected_file, "rb") as file:
            pdf_data = file.read()

        if not pdf_data.startswith(b"%PDF"):
            raise ValueError("The selected file is not a valid PDF.")

        text = self.extract_pdf_text(pdf_data)

        if not text.strip():
            raise ValueError(
                "No machine-readable text was found in this PDF.\n\n"
                "Scanned/image-only PDFs cannot be OCR'd because this project "
                "does not use external OCR or PDF packages."
            )

        return text

    def extract_pdf_text(self, pdf_data):
        extracted_text = []

        # We inspect PDF content streams. Image objects are skipped.
        stream_pattern = re.compile(
            rb"(\d+\s+\d+\s+obj\b.*?stream\r?\n)"
            rb"(.*?)"
            rb"(\r?\nendstream)",
            re.DOTALL,
        )

        for header, stream_data, _ in stream_pattern.findall(pdf_data):
            header_lower = header.lower()

            if (
                b"/subtype /image" in header_lower
                or b"/type /xobject" in header_lower
                and b"/image" in header_lower
            ):
                continue

            decoded = stream_data

            if b"/flatedecode" in header_lower:
                try:
                    decoded = zlib.decompress(stream_data)
                except zlib.error:
                    decoded = self.try_decompress(stream_data)

                    if decoded is None:
                        continue

            # Other binary streams are harmless because only text
            # operators are examined below.
            extracted_text.extend(
                self.extract_pdf_text_operators(decoded)
            )

        cleaned = []

        for text in extracted_text:
            text = "".join(
                char
                for char in text
                if char in "\n\t"
                or ord(char) >= 32
            )

            text = re.sub(r"[ \t]+", " ", text).strip()

            if text:
                cleaned.append(text)

        return "\n".join(cleaned)

    def try_decompress(self, data):
        # Small fallback search for an embedded zlib stream.
        # This is intentionally bounded so a large image cannot cause
        # excessive processing.
        limit = min(len(data), 20000)

        for index in range(limit):
            try:
                return zlib.decompress(data[index:])
            except zlib.error:
                continue

        return None

    # =========================================================
    # PDF TEXT OPERATORS
    # =========================================================

    def extract_pdf_text_operators(self, stream):
        text_parts = []

        # Tj: (Hello) Tj
        for match in re.finditer(
            rb"\((.*?)\)\s*Tj",
            stream,
            re.DOTALL,
        ):
            text = self.decode_pdf_string(match.group(1))
            if text.strip():
                text_parts.append(text)

        # TJ: [(Hello) 20 (World)] TJ
        for match in re.finditer(
            rb"\[(.*?)\]\s*TJ",
            stream,
            re.DOTALL,
        ):
            strings = re.findall(
                rb"\((.*?)\)",
                match.group(1),
                re.DOTALL,
            )

            combined = []

            for raw in strings:
                text = self.decode_pdf_string(raw)
                if text:
                    combined.append(text)

            if combined:
                text_parts.append("".join(combined))

        return text_parts

    # =========================================================
    # PDF STRING DECODER
    # =========================================================

    def decode_pdf_string(self, raw_text):
        result = []
        i = 0

        while i < len(raw_text):
            byte = raw_text[i]

            if byte != ord("\\"):
                if byte >= 32:
                    result.append(chr(byte))
                i += 1
                continue

            i += 1

            if i >= len(raw_text):
                break

            escaped = raw_text[i]

            escape_map = {
                ord("n"): "\n",
                ord("r"): "\r",
                ord("t"): "\t",
                ord("b"): "\b",
                ord("f"): "\f",
                ord("("): "(",
                ord(")"): ")",
                ord("\\"): "\\",
            }

            if escaped in escape_map:
                result.append(escape_map[escaped])
                i += 1
                continue

            # PDF octal escape: \123
            if ord("0") <= escaped <= ord("7"):
                octal = bytes([escaped])
                i += 1
                count = 1

                while (
                    i < len(raw_text)
                    and count < 3
                    and ord("0") <= raw_text[i] <= ord("7")
                ):
                    octal += bytes([raw_text[i]])
                    i += 1
                    count += 1

                try:
                    result.append(chr(int(octal, 8)))
                except ValueError:
                    pass

                continue

            # Unknown escape: keep the escaped character.
            result.append(chr(escaped))
            i += 1

        return "".join(result)

    # =========================================================
    # RESULT WINDOW
    # =========================================================

    def show_analysis_result(self, result, resume_text):
        window = tk.Toplevel(self.root)
        window.title("Resume Analysis Report")
        window.geometry("1200x850")
        window.minsize(1050, 760)
        window.configure(bg="#0F172A")

        tk.Label(
            window,
            text="RESUME ANALYSIS REPORT",
            font=("Segoe UI", 23, "bold"),
            fg="#F8FAFC",
            bg="#0F172A",
        ).pack(pady=(18, 2))

        tk.Label(
            window,
            text=f"Role: {result['job_role']}   •   {result['scoring_basis']}",
            font=("Segoe UI", 9),
            fg="#94A3B8",
            bg="#0F172A",
        ).pack(pady=(0, 10))

        # ---------------------------------------------------------
        # SCORE CARD
        # ---------------------------------------------------------
        score_card = tk.Frame(window, bg="#1E293B")
        score_card.pack(fill="x", padx=35, pady=6)

        score_color = self.score_color(result["score"])

        tk.Label(
            score_card,
            text=f"{result['score']:.1f}%",
            font=("Segoe UI", 31, "bold"),
            fg=score_color,
            bg="#1E293B",
        ).pack(pady=(10, 0))

        tk.Label(
            score_card,
            text=result["recommendation"],
            font=("Segoe UI", 11, "bold"),
            fg="#E2E8F0",
            bg="#1E293B",
        ).pack()

        role_state = (
            "✓ Role found in offline knowledge base"
            if result["role_known"]
            else "• Role not in knowledge base — JD-only knowledge used"
        )

        tk.Label(
            score_card,
            text=role_state,
            font=("Segoe UI", 8),
            fg="#94A3B8",
            bg="#1E293B",
        ).pack(pady=(1, 10))

        # ---------------------------------------------------------
        # COMPONENT SCORES
        # ---------------------------------------------------------
        metrics = tk.Frame(window, bg="#0F172A")
        metrics.pack(fill="x", padx=35, pady=8)

        self.create_metric_card(
            metrics, "JD MATCH", result["jd_score"], "Explicit requirements", "#38BDF8"
        )
        self.create_metric_card(
            metrics, "ROLE FIT", result["role_score"], "Offline knowledge", "#A78BFA"
        )
        self.create_metric_card(
            metrics, "PROJECT FIT", result["project_score"], "Practical evidence", "#FBBF24"
        )
        self.create_metric_card(
            metrics, "SKILLS FOUND", len(result["resume_skills"]), "Detected skills", "#34D399", percent=False
        )

        # ---------------------------------------------------------
        # MAIN CONTENT
        # ---------------------------------------------------------
        body = tk.Frame(window, bg="#0F172A")
        body.pack(fill="both", expand=True, padx=35, pady=5)

        left = tk.Frame(body, bg="#0F172A")
        left.pack(side="left", fill="both", expand=True, padx=(0, 6))

        right = tk.Frame(body, bg="#0F172A")
        right.pack(side="left", fill="both", expand=True, padx=(6, 0))

        self.create_skill_coverage(left, result)
        self.create_requirement_table(right, result)
        self.create_project_evidence(left, result)
        self.create_why_score(right, result)

        # ---------------------------------------------------------
        # BUTTONS
        # ---------------------------------------------------------
        button_row = tk.Frame(window, bg="#0F172A")
        button_row.pack(pady=(5, 15))

        tk.Button(
            button_row,
            text="VIEW EXTRACTED RESUME",
            command=lambda: self.show_extracted_text(resume_text),
            font=("Segoe UI", 9, "bold"),
            bg="#334155",
            fg="white",
            relief="flat",
            cursor="hand2",
            padx=18,
            pady=8,
        ).pack(side="left", padx=5)

        tk.Button(
            button_row,
            text="CLOSE",
            command=window.destroy,
            font=("Segoe UI", 9, "bold"),
            bg="#475569",
            fg="white",
            relief="flat",
            cursor="hand2",
            padx=25,
            pady=8,
        ).pack(side="left", padx=5)

    def score_color(self, score):
        if score >= 85:
            return "#34D399"
        if score >= 70:
            return "#22C55E"
        if score >= 55:
            return "#FBBF24"
        if score >= 40:
            return "#FB923C"
        return "#F87171"

    def create_metric_card(self, parent, title, value, subtitle, accent, percent=True):
        card = tk.Frame(parent, bg="#1E293B", height=82)
        card.pack(side="left", fill="both", expand=True, padx=4)
        card.pack_propagate(False)

        value_text = f"{value:.1f}%" if percent else str(value)

        tk.Label(
            card,
            text=title,
            font=("Segoe UI", 8, "bold"),
            fg=accent,
            bg="#1E293B",
        ).pack(pady=(8, 0))

        tk.Label(
            card,
            text=value_text,
            font=("Segoe UI", 17, "bold"),
            fg="#F8FAFC",
            bg="#1E293B",
        ).pack()

        tk.Label(
            card,
            text=subtitle,
            font=("Segoe UI", 7),
            fg="#64748B",
            bg="#1E293B",
        ).pack()

    def create_section(self, parent, title, color):
        frame = tk.LabelFrame(
            parent,
            text=f"  {title}  ",
            font=("Segoe UI", 9, "bold"),
            fg=color,
            bg="#0F172A",
            bd=1,
            relief="groove",
        )
        frame.pack(fill="both", expand=True, pady=5)
        return frame

    def create_skill_coverage(self, parent, result):
        frame = self.create_section(parent, "SKILL COVERAGE", "#38BDF8")

        canvas = tk.Canvas(
            frame,
            bg="#020617",
            highlightthickness=0,
            height=245,
        )
        canvas.pack(fill="both", expand=True, padx=7, pady=7)

        requirements = result["explicit"] if "explicit" in result else result["explicit_requirements"]
        matched = set(result["matched_skills"]) | set(result["project_matches"])

        if not requirements:
            canvas.create_text(
                20, 30,
                anchor="w",
                text="No recognizable technical requirements in the job description.",
                fill="#94A3B8",
                font=("Segoe UI", 9),
            )
            return

        # Display the most important requirements first.
        weighted = []
        for skill in requirements:
            # Score visualization uses equal display width; actual score is weighted.
            status = skill in matched
            weighted.append((skill, status))

        weighted.sort(key=lambda item: (not item[1], item[0]))
        weighted = weighted[:12]

        frame.update_idletasks()
        width = max(430, frame.winfo_width() - 20)
        bar_x = 170
        bar_width = max(160, width - bar_x - 70)
        y = 18

        for skill, is_match in weighted:
            display = skill.title()
            canvas.create_text(
                10, y + 8,
                anchor="w",
                text=display[:24],
                fill="#E2E8F0",
                font=("Segoe UI", 8),
            )

            canvas.create_rectangle(
                bar_x, y, bar_x + bar_width, y + 16,
                fill="#172033",
                outline="",
            )

            fill_width = bar_width if is_match else 0
            if fill_width:
                canvas.create_rectangle(
                    bar_x, y, bar_x + fill_width, y + 16,
                    fill="#34D399",
                    outline="",
                )

            canvas.create_text(
                bar_x + bar_width + 8, y + 8,
                anchor="w",
                text="MATCH" if is_match else "MISS",
                fill="#34D399" if is_match else "#F87171",
                font=("Segoe UI", 7, "bold"),
            )
            y += 27

    def create_requirement_table(self, parent, result):
        frame = self.create_section(parent, "REQUIREMENT STATUS", "#A78BFA")

        columns = ("requirement", "status", "type")
        tree = ttk.Treeview(frame, columns=columns, show="headings", height=10)

        tree.heading("requirement", text="Requirement")
        tree.heading("status", text="Status")
        tree.heading("type", text="Priority")

        tree.column("requirement", width=190, anchor="w")
        tree.column("status", width=110, anchor="center")
        tree.column("type", width=90, anchor="center")

        tree.pack(fill="both", expand=True, padx=7, pady=7)

        tree.tag_configure("match", foreground="#34D399")
        tree.tag_configure("project", foreground="#38BDF8")
        tree.tag_configure("missing", foreground="#F87171")

        for item in result["requirement_status"][:20]:
            status = item["status"]
            tag = "match" if status == "Direct match" else "project" if status == "Project evidence" else "missing"
            priority = "Core" if item["weight"] >= 3 else "Technical" if item["weight"] >= 2 else "Soft"
            tree.insert(
                "",
                "end",
                values=(item["skill"].title(), status, priority),
                tags=(tag,),
            )

    def create_project_evidence(self, parent, result):
        frame = self.create_section(parent, "PROJECT EVIDENCE", "#FBBF24")

        text = tk.Text(
            frame,
            height=7,
            wrap="word",
            font=("Segoe UI", 8),
            bg="#020617",
            fg="#CBD5E1",
            relief="flat",
            padx=10,
            pady=8,
        )
        text.pack(fill="both", expand=True, padx=7, pady=7)

        if not result["projects"]:
            text.insert("1.0", "No known project pattern detected in the resume.")
        else:
            for name, info in result["projects"].items():
                relevance = self.project_display_relevance(info["skills"], result["explicit_requirements"])
                text.insert("end", f"✓ {name.title()}  •  {relevance:.0f}% relevant\n")
                text.insert("end", f"  Evidence: {info['evidence']}\n")
                text.insert("end", f"  Skills: {', '.join(info['skills'])}\n\n")

        text.config(state="disabled")

    def project_display_relevance(self, skills, requirements):
        if not requirements:
            return 0.0
        relevant = set(skills) & set(requirements)
        return (len(relevant) / len(requirements)) * 100

    def create_why_score(self, parent, result):
        frame = self.create_section(parent, "WHY THIS SCORE?", "#34D399")

        text = tk.Text(
            frame,
            height=7,
            wrap="word",
            font=("Segoe UI", 8),
            bg="#020617",
            fg="#CBD5E1",
            relief="flat",
            padx=10,
            pady=8,
        )
        text.pack(fill="both", expand=True, padx=7, pady=7)

        matched = result["matched_skills"]
        project_matches = result["project_matches"]
        missing = result["missing_skills"]

        text.insert("end", f"✓ {len(matched)} direct JD requirements matched\n")
        text.insert("end", f"✓ {len(project_matches)} additional requirements supported by projects\n")
        text.insert("end", f"✓ {len(result['projects'])} relevant project(s) detected\n")
        text.insert("end", f"✓ JD coverage: {result['jd_score']:.1f}%\n")
        text.insert("end", f"✓ Role fit: {result['role_score']:.1f}%\n")

        if missing:
            text.insert("end", "\nMissing / not evidenced:\n")
            for skill in missing[:8]:
                text.insert("end", f"  • {skill.title()}\n")
        else:
            text.insert("end", "\n✓ No explicit JD requirement is currently missing.\n")

        text.config(state="disabled")

    def show_extracted_text(self, text):
        window = tk.Toplevel(self.root)
        window.title("Extracted Resume Content")
        window.geometry("900x650")
        window.configure(bg="#0F172A")

        tk.Label(
            window,
            text="EXTRACTED RESUME CONTENT",
            font=("Segoe UI", 18, "bold"),
            fg="#F8FAFC",
            bg="#0F172A",
        ).pack(pady=18)

        area = tk.Text(
            window,
            wrap="word",
            font=("Consolas", 10),
            bg="#020617",
            fg="#E2E8F0",
            insertbackground="white",
            relief="flat",
            padx=20,
            pady=20,
        )
        area.pack(fill="both", expand=True, padx=30, pady=(0, 25))

        area.insert("1.0", text)
        area.config(state="disabled")

    # =========================================================
    # FOOTER
    # =========================================================

    def create_footer(self):
        footer = tk.Frame(self.root, bg="#020617")
        footer.pack(fill="x")

        tk.Label(
            footer,
            text=(
                "Python Standard Library • Offline Processing • "
                "No External Resume Analysis Packages • No APIs"
            ),
            font=("Segoe UI", 9),
            fg="#64748B",
            bg="#020617",
        ).pack(pady=10)


if __name__ == "__main__":
    root = tk.Tk()
    app = ResumeAnalyzerApp(root)
    root.mainloop()
