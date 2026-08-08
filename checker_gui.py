import os, sys, traceback, threading
import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
from datetime import datetime

class CodeChecker:
    def __init__(self, target_path):
        self.target_path = target_path
        self.max_lines = 50
    def scan_files(self):
        py_files = []
        if not os.path.exists(self.target_path): return py_files
        for root, _, files in os.walk(self.target_path):
            for file in files:
                if file.endswith(".py"): py_files.append(os.path.join(root, file))
        return py_files
    def analyze_file(self, file_path):
        try:
            with open(file_path, 'r', encoding='utf-8') as f: lines = f.readlines()
            total_lines, func_warnings = len(lines), []
            in_func, func_start, func_name = False, 0, ""
            for i, line in enumerate(lines):
                stripped = line.strip()
                if stripped.startswith("def "):
                    if in_func and (i - func_start) > self.max_lines:
                        func_warnings.append(f"  - 警告: 函数 '{func_name}' 长度 {i - func_start} 行，建议拆分！")
                    in_func, func_start = True, i
                    func_name = stripped.split("(")[0].replace("def ", "")
            if in_func and (len(lines) - func_start) > self.max_lines:
                func_warnings.append(f"  - 警告: 函数 '{func_name}' 长度 {len(lines) - func_start} 行，建议拆分！")
            return {"path": file_path, "lines": total_lines, "warnings": func_warnings}
        except Exception as e:
            return {"path": file_path, "lines": 0, "warnings": [f"  - 读取失败: {str(e)}"]}

class CodeCheckerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("代码检查助手 v2.0")
        self.root.geometry("700x550")
        path_frame = tk.Frame(root)
        path_frame.pack(pady=10, padx=10, fill="x")
        tk.Label(path_frame, text="目标文件夹:").pack(side="left")
        self.path_entry = tk.Entry(path_frame, width=50)
        self.path_entry.pack(side="left", padx=5, expand=True, fill="x")
        tk.Button(path_frame, text="浏览...", command=self.select_folder).pack(side="left")
        tk.Button(root, text="开始检查", command=self.start_check, bg="#4CAF50", fg="white", font=("Arial", 12, "bold"), height=2).pack(pady=10)
        self.result_text = scrolledtext.ScrolledText(root, wrap=tk.WORD, font=("Consolas", 10))
        self.result_text.pack(pady=10, padx=10, fill="both", expand=True)
    def select_folder(self):
        folder = filedialog.askdirectory()
        if folder:
            self.path_entry.delete(0, tk.END)
            self.path_entry.insert(0, folder)
    def start_check(self):
        path = self.path_entry.get().strip()
        if not path or not os.path.exists(path):
            messagebox.showerror("错误", "请选择有效的文件夹路径！")
            return
        self.result_text.delete(1.0, tk.END)
        self.result_text.insert(tk.END, "正在检查，请稍候...\n")
        threading.Thread(target=self.run_check, args=(path,), daemon=True).start()
    def run_check(self, path):
        checker = CodeChecker(path)
        files = checker.scan_files()
        report = [f"检查时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", "="*50]
        total = 0
        for file in files:
            res = checker.analyze_file(file)
            total += res["lines"]
            report.append(f"\n文件: {res['path']}\n  行数: {res['lines']}")
            report.extend(res["warnings"]) if res["warnings"] else report.append("  结构良好，无超长函数警告。")
        report.extend(["\n" + "="*50, f"共扫描: {len(files)} 个 | 总行数: {total} 行"])
        self.result_text.delete(1.0, tk.END)
        self.result_text.insert(tk.END, "\n".join(report))

def main():
    root = tk.Tk()
    CodeCheckerApp(root)
    root.mainloop()

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        err_root = tk.Tk()
        err_root.withdraw()
        messagebox.showerror("程序发生严重错误", f"请检查以下错误信息：\n\n{traceback.format_exc()}")
        err_root.destroy()