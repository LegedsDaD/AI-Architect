import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext

class AIArchitectApp:
    def __init__(self, root):
        self.root = root
        self.root.title("AI Architect - Professional Prompt Engine")
        self.root.geometry("1050x800")
        
        # --- Modern Style Configuration ---
        self.style = ttk.Style()
        self.style.theme_use('clam')
        
        # Define Colors
        bg_color = "#f0f0f0"
        self.root.configure(bg=bg_color)
        
        # Font Styles
        header_font = ("Helvetica", 14, "bold")
        subheader_font = ("Helvetica", 11, "bold")
        label_font = ("Helvetica", 10)
        
        self.style.configure("TFrame", background=bg_color)
        self.style.configure("TLabelframe", background=bg_color, foreground="#333")
        self.style.configure("TLabelframe.Label", font=subheader_font, foreground="#444")
        self.style.configure("TLabel", background=bg_color, font=label_font)
        self.style.configure("Header.TLabel", font=header_font, background="#2c3e50", foreground="white", padding=10)
        self.style.configure("TButton", font=("Helvetica", 10, "bold"), padding=6, relief="flat")
        
        # --- Data Options ---
        self.personas = [
            "Software Engineer", "Senior Data Scientist", "Professional Copywriter", 
            "CEO / Business Strategist", "Academic Researcher", "Legal Consultant", 
            "Product Manager", "UX/UI Designer", "Python Expert", "Cybersecurity Analyst"
        ]
        self.tones = ["Professional", "Direct & Concise", "Academic", "Empathetic", "Sarcastic", "Persuasive", "Technical", "Casual"]
        self.formats = ["Detailed Markdown", "Bulleted List", "Code Snippets", "Step-by-Step Guide", "JSON Data", "CSV Data", "Table"]
        self.complexity = ["Simple (ELI5)", "Standard", "Advanced", "Expert / PhD Level"]

        # --- UI Layout ---
        self.create_layout()
        
        # Bind events for auto-update
        self.entry_task.bind("<KeyRelease>", lambda e: self.generate_prompt())
        self.entry_context.bind("<KeyRelease>", lambda e: self.generate_prompt())
        self.txt_rules.bind("<KeyRelease>", lambda e: self.generate_prompt())
        self.entry_negative.bind("<KeyRelease>", lambda e: self.generate_prompt())

    def create_layout(self):
        # Main Header
        header = ttk.Frame(self.root, style="TFrame")
        header.pack(fill=tk.X)
        ttk.Label(header, text="AI ARCHITECT", style="Header.TLabel").pack(fill=tk.X)
        
        # Main Container
        main_frame = ttk.Frame(self.root, padding="15")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # === LEFT PANEL: Configuration ===
        left_panel = ttk.Frame(main_frame)
        left_panel.pack(side=tk.LEFT, fill=tk.BOTH, expand=False, padx=(0, 10))

        # Global Settings
        settings_frame = ttk.LabelFrame(left_panel, text="1. Global Parameters", padding="10")
        settings_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Dropdowns
        self.create_dropdown(settings_frame, "AI Persona:", self.personas, "Software Engineer", 0)
        self.create_dropdown(settings_frame, "Tone of Voice:", self.tones, "Professional", 1)
        self.create_dropdown(settings_frame, "Output Format:", self.formats, "Detailed Markdown", 2)
        self.create_dropdown(settings_frame, "Complexity Level:", self.complexity, "Standard", 3)

        # Advanced Logic Toggles
        logic_frame = ttk.LabelFrame(left_panel, text="2. Prompt Logic Models", padding="10")
        logic_frame.pack(fill=tk.X, pady=(0, 10))

        self.cot_var = tk.BooleanVar(value=True) # Chain of Thought
        ttk.Checkbutton(logic_frame, text="Enforce Chain-of-Thought (Reason before answering)", 
                        variable=self.cot_var, command=self.generate_prompt).pack(anchor="w", pady=2)
        
        self.example_var = tk.BooleanVar(value=False) # Few Shot
        ttk.Checkbutton(logic_frame, text="Request Output Examples (Few-Shot)", 
                        variable=self.example_var, command=self.generate_prompt).pack(anchor="w", pady=2)

        self.iterative_var = tk.BooleanVar(value=False)
        ttk.Checkbutton(logic_frame, text="Iterative Improvement (Self-Correction)", 
                        variable=self.iterative_var, command=self.generate_prompt).pack(anchor="w", pady=2)

        # Action Buttons
        btn_frame = ttk.Frame(left_panel)
        btn_frame.pack(fill=tk.X, pady=20)
        ttk.Button(btn_frame, text="GENERATE PROMPT", command=self.generate_prompt).pack(fill=tk.X, pady=5)
        ttk.Button(btn_frame, text="Clear All", command=self.clear_all).pack(fill=tk.X, pady=5)
        ttk.Button(btn_frame, text="Copy to Clipboard", command=self.copy_to_clipboard).pack(fill=tk.X, pady=5)


        # === CENTER/RIGHT PANEL: Structured Inputs & Output ===
        center_panel = ttk.Frame(main_frame)
        center_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        # --- Specific Input Section ---
        input_section = ttk.LabelFrame(center_panel, text="3. Project Specification", padding="10")
        input_section.pack(fill=tk.BOTH, expand=True, pady=(0, 10))

        # Grid layout for inputs
        grid_frame = ttk.Frame(input_section)
        grid_frame.pack(fill=tk.BOTH, expand=True)

        # Task
        ttk.Label(grid_frame, text="Core Objective (The Task):").grid(row=0, column=0, sticky="w", pady=(5,0))
        self.entry_task = ttk.Entry(grid_frame, font=("Helvetica", 11))
        self.entry_task.grid(row=1, column=0, sticky="ew", pady=(0,10))
        
        # Context
        ttk.Label(grid_frame, text="Background Context (Who, Where, Why):").grid(row=2, column=0, sticky="w", pady=(5,0))
        self.entry_context = ttk.Entry(grid_frame, font=("Helvetica", 11))
        self.entry_context.grid(row=3, column=0, sticky="ew", pady=(0,10))
        
        # Specific Rules (Bullet Points)
        ttk.Label(grid_frame, text="Specific Rules / Steps (One per line):").grid(row=4, column=0, sticky="w", pady=(5,0))
        self.txt_rules = scrolledtext.ScrolledText(grid_frame, height=5, font=("Consolas", 9))
        self.txt_rules.grid(row=5, column=0, sticky="ew", pady=(0,10))
        self.txt_rules.insert("1.0", "- Rule 1\n- Rule 2")
        
        # Negative Constraints
        ttk.Label(grid_frame, text="Negative Constraints (What to avoid):").grid(row=6, column=0, sticky="w", pady=(5,0))
        self.entry_negative = ttk.Entry(grid_frame, font=("Helvetica", 11))
        self.entry_negative.grid(row=7, column=0, sticky="ew", pady=(0,10))

        grid_frame.columnconfigure(0, weight=1)

        # --- Output Section (The Blueprint) ---
        output_frame = ttk.LabelFrame(center_panel, text="4. Generated Prompt Blueprint", padding="10")
        output_frame.pack(fill=tk.BOTH, expand=True)

        self.output_text = scrolledtext.ScrolledText(output_frame, font=("Consolas", 10), wrap=tk.WORD, bg="#1e1e1e", fg="#00ff00", insertbackground="white")
        self.output_text.pack(fill=tk.BOTH, expand=True)
        
        # Initial Placeholder
        self.output_text.insert("1.0", "// Configure parameters and fill the specification boxes above to generate a production-grade prompt...")

    def create_dropdown(self, parent, label_text, options, default_value, row):
        """Helper to create labeled dropdowns"""
        ttk.Label(parent, text=label_text).grid(row=row, column=0, sticky="w", padx=5, pady=2)
        var = tk.StringVar(value=default_value)
        combo = ttk.Combobox(parent, textvariable=var, values=options, state="readonly")
        combo.grid(row=row+1, column=0, sticky="ew", padx=5, pady=2)
        
        # Store variable in object to access later
        if label_text.startswith("AI"):
            self.persona_var = var
        elif label_text.startswith("Tone"):
            self.tone_var = var
        elif label_text.startswith("Output"):
            self.format_var = var
        elif label_text.startswith("Complexity"):
            self.complex_var = var
            
        combo.bind("<<ComboboxSelected>>", lambda e: self.generate_prompt())
        parent.columnconfigure(0, weight=1)

    def generate_prompt(self):
        """Constructs a highly structured, advanced prompt using CO-STAR principles."""
        
        # --- Gather Inputs ---
        task = self.entry_task.get().strip()
        context = self.entry_context.get().strip()
        raw_rules = self.txt_rules.get("1.0", "end-1c").strip()
        negative = self.entry_negative.get().strip()
        
        persona = self.persona_var.get()
        tone = self.tone_var.get()
        fmt = self.format_var.get()
        complexity = self.complex_var.get()
        
        # Logic Toggles
        use_cot = self.cot_var.get()
        use_examples = self.example_var.get()
        use_iterative = self.iterative_var.get()

        # --- Validation ---
        if not task and not context and not raw_rules:
            return

        # --- Process Rules ---
        # Convert list into strict bullet points
        requirements = []
        for line in raw_rules.split('\n'):
            clean = line.strip()
            if clean:
                if clean.startswith(("-", "*", "•")):
                    clean = clean[1:].strip()
                requirements.append(f"- {clean}")

        # --- CONSTRUCT THE PROMPT ---
        # We use XML tags <tag> content </tag> for LLM precision
        
        prompt_lines = []
        
        # 1. System Identity
        prompt_lines.append("### SYSTEM IDENTITY")
        prompt_lines.append(f"You are acting as a {persona}.")
        prompt_lines.append(f"Your response complexity must be {complexity}.")
        prompt_lines.append("")
        
        # 2. Context (CO-STAR: Context)
        if context:
            prompt_lines.append("### CONTEXT")
            prompt_lines.append("<context>")
            prompt_lines.append(context)
            prompt_lines.append("</context>")
            prompt_lines.append("")
            
        # 3. Task (CO-STAR: Objective)
        prompt_lines.append("### OBJECTIVE")
        prompt_lines.append("<task>")
        prompt_lines.append(task)
        prompt_lines.append("</task>")
        prompt_lines.append("")

        # 4. Specific Rules (CO-STAR: Style & Instructions)
        if requirements or negative or use_cot or use_examples or use_iterative:
            prompt_lines.append("### CONSTRAINTS & INSTRUCTIONS")
            prompt_lines.append("")
            
            # Rules
            if requirements:
                prompt_lines.append("Adhere to the following rules strictly:")
                for r in requirements:
                    prompt_lines.append(r)
                prompt_lines.append("")

            # Logic Models
            if use_cot:
                prompt_lines.append("- CRITICAL: Use 'Chain-of-Thought' reasoning. Break the problem down step-by-step before providing the final answer.")
            
            if use_iterative:
                prompt_lines.append("- Review your output once before finalizing. Ensure there are no hallucinations or logical errors.")

            if use_examples:
                prompt_lines.append("- Provide a concrete example to illustrate the concept if applicable.")
            
            # Negative Constraints
            if negative:
                prompt_lines.append(f"- RESTRICTION: Do not include the following: {negative}")
            prompt_lines.append("")

        # 5. Tone & Format (CO-STAR: Tone & Response)
        prompt_lines.append("### OUTPUT SPECIFICATIONS")
        prompt_lines.append(f"- Tone: {tone}")
        prompt_lines.append(f"- Format: {fmt}")
        
        if fmt == "Code Snippets":
            prompt_lines.append("- Ensure code is wrapped in appropriate markdown blocks (e.g., ```python ```).")
        if fmt == "JSON Data":
            prompt_lines.append("- Output valid JSON only. No markdown formatting or explanation outside the JSON.")
            
        # Final Delimiter
        prompt_lines.append("")
        prompt_lines.append("### BEGIN RESPONSE")
        
        # --- Final Assembly ---
        final_prompt = "\n".join(prompt_lines)
        
        self.output_text.delete("1.0", tk.END)
        self.output_text.insert(tk.END, final_prompt)

    def copy_to_clipboard(self):
        content = self.output_text.get("1.0", "end-1c")
        if content and not content.startswith("//"):
            self.root.clipboard_clear()
            self.root.clipboard_append(content)
            self.root.update()
            messagebox.showinfo("Success", "Blueprint copied to clipboard.")
        else:
            messagebox.showwarning("Warning", "Generate a prompt first.")

    def clear_all(self):
        self.entry_task.delete(0, tk.END)
        self.entry_context.delete(0, tk.END)
        self.txt_rules.delete("1.0", tk.END)
        self.txt_rules.insert("1.0", "- Rule 1\n- Rule 2")
        self.entry_negative.delete(0, tk.END)
        self.output_text.delete("1.0", tk.END)
        self.output_text.insert("1.0", "// Configure parameters and fill the specification boxes above to generate a production-grade prompt...")
        
        # Reset defaults
        self.persona_var.set("Software Engineer")
        self.tone_var.set("Professional")
        self.format_var.set("Detailed Markdown")
        self.complex_var.set("Standard")
        self.cot_var.set(True)

if __name__ == "__main__":
    root = tk.Tk()
    app = AIArchitectApp(root)
    root.mainloop()
