import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
from pymongo import MongoClient
import subprocess
import os

client = MongoClient('mongodb://localhost:27017/')
db = client['coding_assessment']
prob_coll = db['problems']
sub_coll = db['submissions']
users_coll = db['users']

class CP:
    def __init__(self, root):
        self.root = root
        self.root.title("Online Coding Assessment Platform")
        self.root.geometry("840x640")
        self.root.configure(bg="#e9eff5")
        self.style = ttk.Style()
        self.style.theme_use("clam")
        self.style.configure("Card.TFrame", background="#ffffff", borderwidth=1, relief="raised")
        self.style.configure("Header.TLabel", font=("Helvetica", 26, "bold"), background="#e9eff5", foreground="#22303f")
        self.style.configure("Label.TLabel", font=("Helvetica", 11), background="#ffffff", foreground="#2f4f65")
        self.style.configure("Accent.TButton", font=("Helvetica", 11, "bold"), background="#4a90e2", foreground="white")
        self.style.map("Accent.TButton", background=[("active", "#3b78c0")])
        self.style.configure("Success.TButton", font=("Helvetica", 11, "bold"), background="#4CAF50", foreground="white")
        self.style.map("Success.TButton", background=[("active", "#3a8b44")])
        self.style.configure("Danger.TButton", font=("Helvetica", 11, "bold"), background="#e74c3c", foreground="white")
        self.style.map("Danger.TButton", background=[("active", "#c0392b")])
        self.style.configure("Input.TEntry", foreground="#2f4f65", fieldbackground="#f7fbff", background="#f7fbff")
        self.style.configure("TCombobox", fieldbackground="#f7fbff", background="#f7fbff", foreground="#2f4f65")
        self.current_user = None
        self.show_login()

    def show_login(self):
        self.clear_frame()
        card = ttk.Frame(self.root, style="Card.TFrame", padding=(30, 25))
        card.place(relx=0.5, rely=0.5, anchor="center")

        ttk.Label(card, text="Login", style="Header.TLabel").pack(pady=(0, 20))
        ttk.Label(card, text="Username:", style="Label.TLabel").pack(anchor="w", pady=(0, 6))
        self.username_entry = ttk.Entry(card, style="Input.TEntry", width=34)
        self.username_entry.pack(pady=(0, 12))
        ttk.Label(card, text="Password:", style="Label.TLabel").pack(anchor="w", pady=(0, 6))
        self.password_entry = ttk.Entry(card, show="*", style="Input.TEntry", width=34)
        self.password_entry.pack(pady=(0, 18))

        ttk.Button(card, text="Login", command=self.login, style="Success.TButton", width=30).pack(pady=(0, 10))
        ttk.Button(card, text="Register", command=self.show_register, style="Accent.TButton", width=30).pack()

    def show_register(self):
        self.clear_frame()
        card = ttk.Frame(self.root, style="Card.TFrame", padding=(30, 25))
        card.place(relx=0.5, rely=0.5, anchor="center")

        ttk.Label(card, text="Register", style="Header.TLabel").pack(pady=(0, 20))
        ttk.Label(card, text="Username:", style="Label.TLabel").pack(anchor="w", pady=(0, 6))
        self.reg_username = ttk.Entry(card, style="Input.TEntry", width=34)
        self.reg_username.pack(pady=(0, 12))
        ttk.Label(card, text="Password:", style="Label.TLabel").pack(anchor="w", pady=(0, 6))
        self.reg_password = ttk.Entry(card, show="*", style="Input.TEntry", width=34)
        self.reg_password.pack(pady=(0, 12))
        ttk.Label(card, text="Select Role:", style="Label.TLabel").pack(anchor="w", pady=(0, 6))
        self.reg_role = ttk.Combobox(card, values=["candidate", "recruiter"], state="readonly", width=32)
        self.reg_role.set("candidate")
        self.reg_role.pack(pady=(0, 18))

        ttk.Button(card, text="Register", command=self.register, style="Success.TButton", width=30).pack(pady=(0, 10))
        ttk.Button(card, text="Back to Login", command=self.show_login, style="Accent.TButton", width=30).pack()

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        user = users_coll.find_one({"username": username, "password": password})
        if user:
            self.current_user = user
            if user['role'] == 'recruiter':
                self.recruiter_dash()
            else:
                self.candidate_dash()
        else:
            messagebox.showerror("Error", "Invalid credentials")

    def register(self):
        username = self.reg_username.get()
        password = self.reg_password.get()
        role = self.reg_role.get()
        if users_coll.find_one({"username": username}):
            messagebox.showerror("Error", "Username already exists")
        else:
            users_coll.insert_one({"username": username, "password": password, "role": role, "score": 0})
            messagebox.showinfo("Success", "Registered successfully")
            self.show_login()

    def candidate_dash(self):
        self.clear_frame()
        card = ttk.Frame(self.root, style="Card.TFrame", padding=(30, 25))
        card.place(relx=0.5, rely=0.5, anchor="center")

        ttk.Label(card, text="Candidate Dashboard", style="Header.TLabel").pack(pady=(0, 24))
        ttk.Button(card, text="View Problems", command=self.show_problems, style="Success.TButton", width=30).pack(pady=8)
        ttk.Button(card, text="Leaderboard", command=self.show_leaderboard, style="Accent.TButton", width=30).pack(pady=8)
        ttk.Button(card, text="Logout", command=self.show_login, style="Danger.TButton", width=30).pack(pady=8)

    def recruiter_dash(self):
        self.clear_frame()
        card = ttk.Frame(self.root, style="Card.TFrame", padding=(30, 25))
        card.place(relx=0.5, rely=0.5, anchor="center")

        ttk.Label(card, text="Recruiter Dashboard", style="Header.TLabel").pack(pady=(0, 24))
        ttk.Button(card, text="Create Problem", command=self.create_problem, style="Success.TButton", width=30).pack(pady=8)
        ttk.Button(card, text="View Submissions", command=self.show_submissions, style="Accent.TButton", width=30).pack(pady=8)
        ttk.Button(card, text="Leaderboard", command=self.show_leaderboard, style="Accent.TButton", width=30).pack(pady=8)
        ttk.Button(card, text="Logout", command=self.show_login, style="Danger.TButton", width=30).pack(pady=8)

    def create_problem(self):
        self.clear_frame()
        card = ttk.Frame(self.root, style="Card.TFrame", padding=(30, 25))
        card.place(relx=0.5, rely=0.5, anchor="center")

        ttk.Label(card, text="Create Problem", style="Header.TLabel").pack(pady=(0, 20))
        ttk.Label(card, text="Title:", style="Label.TLabel").pack(anchor="w", pady=(0, 6))
        self.problem_title = ttk.Entry(card, style="Input.TEntry", width=54)
        self.problem_title.pack(pady=(0, 14))

        ttk.Label(card, text="Description:", style="Label.TLabel").pack(anchor="w", pady=(0, 6))
        self.problem_desc = scrolledtext.ScrolledText(card, height=6, width=70, wrap=tk.WORD)
        self.problem_desc.pack(pady=(0, 14))

        ttk.Label(card, text="Test Cases (input|output per line):", style="Label.TLabel").pack(anchor="w", pady=(0, 6))
        self.test_cases = scrolledtext.ScrolledText(card, height=6, width=70, wrap=tk.WORD)
        self.test_cases.pack(pady=(0, 18))

        ttk.Button(card, text="Save Problem", command=self.save_problem, style="Success.TButton", width=30).pack(pady=(0, 10))
        ttk.Button(card, text="Back", command=self.recruiter_dash, style="Accent.TButton", width=30).pack()

    def save_problem(self):
        title = self.problem_title.get()
        desc = self.problem_desc.get("1.0", tk.END).strip()
        test_cases = self.test_cases.get("1.0", tk.END).strip().split('\n')
        prob_coll.insert_one({"title": title, "description": desc, "test_cases": test_cases})
        messagebox.showinfo("Success", "Problem created")
        self.recruiter_dash()

    def show_problems(self):
        self.clear_frame()
        card = ttk.Frame(self.root, style="Card.TFrame", padding=(30, 25))
        card.place(relx=0.5, rely=0.5, anchor="center")

        ttk.Label(card, text="Problems", style="Header.TLabel").pack(pady=(0, 20))
        problems = list(prob_coll.find())
        if not problems:
            ttk.Label(card, text="No problems are available yet.", style="Label.TLabel").pack(pady=(0, 10))
        for problem in problems:
            ttk.Button(card, text=problem['title'], command=lambda p=problem: self.show_submit_code(p), style="Accent.TButton", width=42).pack(pady=6)

        ttk.Button(card, text="Back", command=self.candidate_dash, style="Accent.TButton", width=30).pack(pady=(15, 0))

    def show_submit_code(self, problem):
        self.clear_frame()
        card = ttk.Frame(self.root, style="Card.TFrame", padding=(30, 25))
        card.place(relx=0.5, rely=0.5, anchor="center")

        ttk.Label(card, text=problem['title'], style="Header.TLabel").pack(pady=(0, 18))
        ttk.Label(card, text=problem['description'], style="Label.TLabel", wraplength=700).pack(pady=(0, 14))

        ttk.Label(card, text="Language:", style="Label.TLabel").pack(anchor="w", pady=(0, 6))
        self.sub_lang = ttk.Combobox(card, values=["python", "javascript", "cpp", "c", "java"], state="readonly", width=32)
        self.sub_lang.set("python")
        self.sub_lang.pack(pady=(0, 14))

        ttk.Label(card, text="Write your code:", style="Label.TLabel").pack(anchor="w", pady=(0, 6))
        self.code_text = scrolledtext.ScrolledText(card, height=12, width=78, wrap=tk.WORD)
        self.code_text.pack(pady=(0, 16))

        ttk.Button(card, text="Submit", command=lambda: self.submit_code(problem), style="Success.TButton", width=30).pack(pady=(0, 10))
        ttk.Button(card, text="Back", command=self.show_problems, style="Accent.TButton", width=30).pack()

    def submit_code(self, problem):
        code = self.code_text.get("1.0", tk.END).strip()
        language = self.sub_lang.get()
        base_name = "temp_code"
        file_map = {
            "python": base_name + ".py",
            "javascript": base_name + ".js",
            "cpp": base_name + ".cpp",
            "c": base_name + ".c",
            "java": "TempCode.java",
        }
        filename = file_map.get(language, base_name + ".txt")

        with open(filename, "w", encoding="utf-8") as f:
            f.write(code)

        compile_error = None
        runtime_error = None
        execution_cmd = []

        try:
            if language == "python":
                execution_cmd = ["python", filename]
            elif language == "javascript":
                execution_cmd = ["node", filename]
            elif language == "cpp":
                exe_name = base_name + (".exe" if os.name == "nt" else "")
                compile_result = subprocess.run(["g++", filename, "-o", exe_name], text=True, capture_output=True, timeout=20)
                if compile_result.returncode != 0:
                    compile_error = compile_result.stderr or compile_result.stdout
                else:
                    execution_cmd = [exe_name]
            elif language == "c":
                exe_name = base_name + (".exe" if os.name == "nt" else "")
                compile_result = subprocess.run(["gcc", filename, "-o", exe_name], text=True, capture_output=True, timeout=20)
                if compile_result.returncode != 0:
                    compile_error = compile_result.stderr or compile_result.stdout
                else:
                    execution_cmd = [exe_name]
            elif language == "java":
                compile_result = subprocess.run(["javac", filename], text=True, capture_output=True, timeout=20)
                if compile_result.returncode != 0:
                    compile_error = compile_result.stderr or compile_result.stdout
                else:
                    execution_cmd = ["java", "TempCode"]
        except Exception as exc:
            compile_error = str(exc)

        if compile_error:
            self.cleanup_temp_files()
            messagebox.showerror("Compile Error", f"{language.capitalize()} compile failed:\n{compile_error}")
            return

        passed = 0
        total = len(problem['test_cases'])
        for test_case in problem['test_cases']:
            input_data, expected_output = test_case.split('|')
            try:
                result = subprocess.run(execution_cmd, input=input_data, text=True, capture_output=True, timeout=15)
                if result.returncode != 0:
                    runtime_error = result.stderr or result.stdout
                    break
                if result.stdout.strip() == expected_output.strip():
                    passed += 1
            except subprocess.TimeoutExpired:
                runtime_error = "Execution timed out"
                break
            except Exception as exc:
                runtime_error = str(exc)
                break

        self.cleanup_temp_files()

        if runtime_error:
            messagebox.showerror("Runtime Error", f"{language.capitalize()} runtime failed:\n{runtime_error}")
            return

        score = (passed / total) * 100 if total > 0 else 0
        sub_coll.insert_one({"user": self.current_user['username'], "problem": problem['title'], "score": score})
        users_coll.update_one({"username": self.current_user['username']}, {"$set": {"score": self.current_user['score'] + score}})
        messagebox.showinfo("Result", f"Passed {passed}/{total} tests. Score: {score}")
        self.candidate_dash()

    def cleanup_temp_files(self):
        temp_files = ["temp_code.py", "temp_code.js", "temp_code.cpp", "temp_code.c", "TempCode.java", "TempCode.class"]
        temp_files.append("temp_code.exe" if os.name == "nt" else "temp_code")
        for filename in temp_files:
            try:
                if os.path.exists(filename):
                    os.remove(filename)
            except:
                pass

    def show_leaderboard(self):
        self.clear_frame()
        card = ttk.Frame(self.root, style="Card.TFrame", padding=(30, 25))
        card.place(relx=0.5, rely=0.5, anchor="center")

        ttk.Label(card, text="Leaderboard", style="Header.TLabel").pack(pady=(0, 20))
        users = list(users_coll.find({"role": "candidate"}).sort("score", -1))
        if not users:
            ttk.Label(card, text="No leaderboard data available yet.", style="Label.TLabel").pack(pady=(0, 10))
        for user in users:
            ttk.Label(card, text=f"{user['username']}: {user['score']}", style="Label.TLabel").pack(anchor="w", pady=2)

        ttk.Button(card, text="Back", command=self.candidate_dash if self.current_user['role'] == 'candidate' else self.recruiter_dash, style="Accent.TButton", width=30).pack(pady=(15, 0))

    def show_submissions(self):
        self.clear_frame()
        card = ttk.Frame(self.root, style="Card.TFrame", padding=(30, 25))
        card.place(relx=0.5, rely=0.5, anchor="center")

        ttk.Label(card, text="Submissions", style="Header.TLabel").pack(pady=(0, 20))
        submissions = list(sub_coll.find())
        if not submissions:
            ttk.Label(card, text="No submissions have been made yet.", style="Label.TLabel").pack(pady=(0, 10))
        for sub in submissions:
            ttk.Label(card, text=f"{sub['user']} - {sub['problem']}: {sub['score']}", style="Label.TLabel").pack(anchor="w", pady=2)

        ttk.Button(card, text="Back", command=self.recruiter_dash, style="Accent.TButton", width=30).pack(pady=(15, 0))

    def clear_frame(self):
        for widget in self.root.winfo_children():
            widget.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = CP(root)
    root.mainloop()