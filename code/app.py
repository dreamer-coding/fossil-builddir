"""
Module: app.py
Description: This Python source file is part of the Native Python Application, which is a project under the Trilobite Coder Lab.

Author:
- Name: Michael Gene Brockus (Dreamer)
- Email: michaelbrockus@gmail.com
- Website: https://trilobite.code.blog

License: This software is released under the Apache License 2.0. Please refer to the LICENSE file for more details.

Purpose:
- This Python source file contains the implementation for the Native Python Application.
- It includes the main logic and functionality required for the application to run.
- Review and modify this file as needed for your specific project requirements.

For more information on the Native Python Application and the Trilobite Coder Lab project, please refer to the project documentation and website.
"""
import tkinter as tk
from tkinter import ttk, simpledialog
from tkinter.scrolledtext import ScrolledText
import subprocess
import threading
import os

class SetupDialog(simpledialog.Dialog):
    def body(self, master):
        ttk.Label(master, text="Meson Setup Options").grid(row=0, column=0, columnspan=2, pady=10)

        ttk.Label(master, text="Build Directory:").grid(row=1, column=0, sticky=tk.W)
        self.build_dir_entry = ttk.Entry(master, width=40)
        self.build_dir_entry.insert(0, "builddir")
        self.build_dir_entry.grid(row=1, column=1, pady=10, sticky=tk.W + tk.E)

        ttk.Label(master, text="Other Options:").grid(row=2, column=0, sticky=tk.W)
        self.other_options_entry = ttk.Entry(master, width=40)
        self.other_options_entry.grid(row=2, column=1, pady=10, sticky=tk.W + tk.E)

    def apply(self):
        build_dir = self.build_dir_entry.get()
        other_options = self.other_options_entry.get()
        self.result = (build_dir, other_options)

class MesonBuildGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Meson Build GUI")
        self.root.geometry("650x400")

        self.create_widgets()

    def create_widgets(self):
        # Create a style for Orange buttons
        ttk.Style().configure('Orange.TButton', foreground='black', background='#FFA500')

        self.setup_button = ttk.Button(self.root, text="Setup", command=self.setup_project, style='Orange.TButton')
        self.compile_button = ttk.Button(self.root, text="Compile", command=self.compile_project, style='Orange.TButton')
        self.test_button = ttk.Button(self.root, text="Test", command=self.test_project, style='Orange.TButton')
        self.install_button = ttk.Button(self.root, text="Install", command=self.install_project, style='Orange.TButton')

        self.version_button = ttk.Button(self.root, text="Version", command=self.show_version, style='Orange.TButton')
        self.introspect_button = ttk.Button(self.root, text="Introspection", command=self.show_introspection, style='Orange.TButton')
        self.clear_terminal_button = ttk.Button(self.root, text="Clear Terminal", command=self.clear_terminal, style='Orange.TButton')
        self.tool_info_button = ttk.Button(self.root, text="Tool Info", command=self.get_tool_info, style='Orange.TButton')

        # Input boxes for source directory and build directory
        self.source_dir_label = ttk.Label(self.root, text="Source Directory:")
        self.source_dir_entry = ttk.Entry(self.root, width=50)
        self.source_dir_entry.insert(0, os.getcwd())  # Default to current directory

        self.build_dir_label = ttk.Label(self.root, text="Build Directory:")
        self.build_dir_entry = ttk.Entry(self.root, width=50)
        self.build_dir_entry.insert(0, os.path.join(os.getcwd(), "builddir"))  # Default build directory name

        self.terminal = ScrolledText(self.root, height=10, state=tk.DISABLED, wrap=tk.WORD, background="black", foreground="light blue", font="helvetica 10 bold")

        # Arrange buttons in two rows
        row1_buttons = [self.setup_button, self.compile_button, self.test_button, self.install_button]
        row2_buttons = [self.version_button, self.introspect_button, self.clear_terminal_button, self.tool_info_button]

        for col, button in enumerate(row1_buttons):
            button.grid(row=0, column=col, pady=10, padx=10, sticky=tk.W + tk.E)

        for col, button in enumerate(row2_buttons):
            button.grid(row=1, column=col, pady=10, padx=10, sticky=tk.W + tk.E)

        self.source_dir_label.grid(row=2, column=0, pady=5, padx=10, sticky=tk.W)
        self.source_dir_entry.grid(row=2, column=1, pady=5, padx=10, sticky=tk.W + tk.E, columnspan=3)
        self.build_dir_label.grid(row=3, column=0, pady=5, padx=10, sticky=tk.W)
        self.build_dir_entry.grid(row=3, column=1, pady=5, padx=10, sticky=tk.W + tk.E, columnspan=3)

        self.terminal.grid(row=4, column=0, columnspan=4, pady=10, padx=10, sticky=tk.W + tk.E + tk.N + tk.S)

    def run_command(self, command, cwd=None):
        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, cwd=cwd)

        while True:
            line = process.stdout.readline()
            if not line:
                break
            self.update_terminal(line)

        process.communicate()

    def update_terminal(self, message):
        self.terminal.configure(state=tk.NORMAL)
        self.terminal.insert(tk.END, message, "custom")
        self.terminal.yview(tk.END)
        self.terminal.configure(state=tk.DISABLED)

    def setup_project(self):
        build_dir, other_options = SetupDialog(self.root).result

        if build_dir:
            threading.Thread(target=self.run_setup_thread, args=(build_dir, other_options)).start()

    def run_setup_thread(self, build_dir, other_options):
        source_dir = self.source_dir_entry.get()
        self.update_terminal(f"Setting up the project in {build_dir}...\n")
        command = ["meson", "setup", build_dir]

        if other_options:
            command += other_options.split()

        self.run_command(command, cwd=source_dir)

    def compile_project(self):
        threading.Thread(target=self.run_compile_thread).start()

    def run_compile_thread(self):
        build_dir = self.build_dir_entry.get()
        self.update_terminal(f"Compiling the project in {build_dir}...\n")
        self.run_command(["ninja", "-C", build_dir])

    def test_project(self):
        threading.Thread(target=self.run_test_thread).start()

    def run_test_thread(self):
        build_dir = self.build_dir_entry.get()
        self.update_terminal(f"Testing the project in {build_dir}...\n")
        self.run_command(["ninja", "-C", build_dir, "test"])

    def install_project(self):
        threading.Thread(target=self.run_install_thread).start()

    def run_install_thread(self):
        build_dir = self.build_dir_entry.get()
        self.update_terminal(f"Installing the project in {build_dir}...\n")
        self.run_command(["ninja", "-C", build_dir, "install"])

    def show_version(self):
        threading.Thread(target=self.run_version_thread).start()

    def run_version_thread(self):
        self.update_terminal("Meson Version:\n")
        self.run_command(["meson", "--version"])

    def show_introspection(self):
        threading.Thread(target=self.run_introspection_thread).start()

    def run_introspection_thread(self):
        source_dir = self.source_dir_entry.get()
        build_dir = self.build_dir_entry.get()

        if not build_dir:
            self.update_terminal("Build directory not specified. Introspecting source directory...\n")
            self.run_command(["meson", "introspect", "/"], cwd=source_dir)
        else:
            self.update_terminal(f"Introspecting build directory {build_dir}...\n")
            self.run_command(["meson", "introspect", "/"], cwd=build_dir)

    def clear_terminal(self):
        self.terminal.configure(state=tk.NORMAL)
        self.terminal.delete("1.0", tk.END)
        self.terminal.configure(state=tk.DISABLED)

    def get_tool_info(self):
        threading.Thread(target=self.run_tool_info_thread).start()

    def run_tool_info_thread(self):
        self.update_terminal("Meson Build GUI Information:\n")
        self.update_terminal("This tool assists in building Meson projects using a graphical user interface.\n")
        self.update_terminal("It provides options to set up, compile, test, install, and get information about the Meson project.\n\n")
        self.update_terminal("Created by Dreamer lead developer at Fossil Logic.\n")

if __name__ == "__main__":
    root = tk.Tk()
    app = MesonBuildGUI(root)
    root.mainloop()
