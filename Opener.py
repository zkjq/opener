import tkinter as tk
from tkinter import filedialog, messagebox
import subprocess
import json
import os

class SoftwareLauncherApp:
    def __init__(self, master):
        self.master = master
        self.master.title("连开器")

        # 配置文件路径
        self.config_file = "config.json"

        # 输入框和添加按钮
        self.label = tk.Label(master, text="添加软件路径:")
        self.label.pack()

        self.entry = tk.Entry(master, width=50)
        self.entry.pack()

        # 命令行参数输入框
        self.args_label = tk.Label(master, text="命令行参数（可选）:")
        self.args_label.pack()

        self.args_entry = tk.Entry(master, width=50)
        self.args_entry.pack()

        self.add_button = tk.Button(master, text="添加", command=self.add_software)
        self.add_button.pack()

        # 浏览文件按钮
        self.browse_button = tk.Button(master, text="浏览文件", command=self.browse_file)
        self.browse_button.pack()

        # 显示已添加的软件路径和参数
        self.listbox = tk.Listbox(master, width=50, height=10)
        self.listbox.pack()

        # 启动所有按钮
        self.launch_all_button = tk.Button(master, text="启动所有", command=self.launch_all_software)
        self.launch_all_button.pack()

        # 关闭所有按钮
        self.close_all_button = tk.Button(master, text="关闭所有", command=self.close_all_software)
        self.close_all_button.pack()

        # 状态栏
        self.status_label = tk.Label(master, text="状态: 等待操作", bd=1, relief=tk.SUNKEN, anchor=tk.W)
        self.status_label.pack(side=tk.BOTTOM, fill=tk.X)

        # 存储进程的列表
        self.processes = []

        # 加载配置
        self.load_config()

        # 窗口关闭时保存配置
        self.master.protocol("WM_DELETE_WINDOW", self.on_close)

    def add_software(self):
        software_path = self.entry.get()
        args = self.args_entry.get()
        if software_path:
            # 将路径和参数组合成一个字符串，添加到 Listbox
            if args:
                self.listbox.insert(tk.END, f"{software_path} {args}")
            else:
                self.listbox.insert(tk.END, software_path)
            self.entry.delete(0, tk.END)
            self.args_entry.delete(0, tk.END)
            self.update_status("软件路径和参数已添加")
        else:
            self.update_status("警告: 请输入软件路径")

    def browse_file(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            # 验证文件路径是否合法
            if os.path.exists(file_path):
                self.entry.delete(0, tk.END)
                self.entry.insert(0, file_path)
                self.update_status("已选择文件路径")
            else:
                self.update_status("警告: 选择的文件路径无效")

    def launch_all_software(self):
        if self.listbox.size() > 0:
            for i in range(self.listbox.size()):
                software_info = self.listbox.get(i)
                try:
                    # 将路径和参数拆分为列表
                    args_list = software_info.split()
                    # 验证路径和参数是否合法
                    if os.path.exists(args_list[0]):
                        process = subprocess.Popen(args_list)
                        self.processes.append(process)
                        self.update_status(f"已启动软件")
                    else:
                        self.update_status(f"错误: 软件路径无效: {args_list[0]}")
                except subprocess.SubprocessError as e:
                    self.update_status(f"错误: 无法启动软件: {e}")
                except Exception as e:
                    self.update_status(f"未知错误: {e}")
        else:
            self.update_status("警告: 请先添加软件路径")

    def close_all_software(self):
        if self.processes:
            for process in self.processes:
                try:
                    process.terminate()
                except Exception as e:
                    self.update_status(f"错误: 无法关闭软件: {e}")
            self.processes = []
            self.update_status("已关闭所有软件")
        else:
            self.update_status("警告: 没有正在运行的软件")

    def update_status(self, message):
        """更新状态栏信息"""
        self.status_label.config(text=f"状态: {message}")

    def load_config(self):
        """加载配置文件"""
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, "r", encoding="utf-8") as f:
                    config = json.load(f)
                    for item in config:
                        self.listbox.insert(tk.END, item)
                self.update_status("配置已加载")
            except json.JSONDecodeError as e:
                messagebox.showerror("错误", f"配置文件格式错误: {e}")
            except Exception as e:
                messagebox.showerror("错误", f"无法加载配置文件: {e}")

    def save_config(self):
        """保存配置文件"""
        try:
            config = [self.listbox.get(i) for i in range(self.listbox.size())]
            with open(self.config_file, "w", encoding="utf-8") as f:
                json.dump(config, f, ensure_ascii=False, indent=4)
            self.update_status("配置已保存")
        except Exception as e:
            messagebox.showerror("错误", f"无法保存配置文件: {e}")

    def on_close(self):
        """窗口关闭时保存配置"""
        self.save_config()
        self.master.destroy()

if __name__ == "__main__":
    master = tk.Tk()
    app = SoftwareLauncherApp(master)
    master.mainloop()
