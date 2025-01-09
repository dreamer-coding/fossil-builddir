#
# ==============================================================================
# Author: Michael Gene Brockus (Dreamer)
# Email: michaelbrockus@gmail.com
# Organization: Fossil Logic
# Description:
#     This file is part of the Fossil Logic project, where innovation meets
#     excellence in software development. Michael Gene Brockus, also known as
#     "Dreamer," is a dedicated contributor to this project. For any inquiries,
#     feel free to contact Michael at michaelbrockus@gmail.com.
# ==============================================================================
#
import tkinter as tk
from tkinter import ttk, simpledialog
from tkinter.scrolledtext import ScrolledText
import subprocess
import threading
import os


class SetupDialog(simpledialog.Dialog):
    def body(self, master):
        master.configure(bg="dark gray")
        ttk.Label(master, text="Meson Setup Options", background="dark gray", foreground="white").grid(
            row=0, column=0, columnspan=2, pady=10
        )

        ttk.Label(master, text="Build Directory:", background="dark gray", foreground="white").grid(row=1, column=0, sticky=tk.W)
        self.build_dir_entry = ttk.Entry(master, width=40)
        self.build_dir_entry.insert(0, "builddir")
        self.build_dir_entry.grid(row=1, column=1, pady=10, sticky=tk.W + tk.E)

        ttk.Label(master, text="Other Options:", background="dark gray", foreground="white").grid(row=2, column=0, sticky=tk.W)
        self.other_options_entry = ttk.Entry(master, width=40)
        self.other_options_entry.grid(row=2, column=1, pady=10, sticky=tk.W + tk.E)

    def apply(self):
        build_dir = self.build_dir_entry.get()
        other_options = self.other_options_entry.get()
        self.result = (build_dir, other_options)


class ConfigureDialog(simpledialog.Dialog):
    def body(self, master):
        master.configure(bg="dark gray")
        ttk.Label(master, text="Meson Configure Options", background="dark gray", foreground="white").grid(
            row=0, column=0, columnspan=2, pady=10
        )

        ttk.Label(master, text="Build Directory:", background="dark gray", foreground="white").grid(row=1, column=0, sticky=tk.W)
        self.build_dir_entry = ttk.Entry(master, width=40)
        self.build_dir_entry.insert(0, "builddir")
        self.build_dir_entry.grid(row=1, column=1, pady=10, sticky=tk.W + tk.E)

        ttk.Label(master, text="Other Options:", background="dark gray", foreground="white").grid(row=2, column=0, sticky=tk.W)
        self.other_options_entry = ttk.Entry(master, width=40)
        self.other_options_entry.grid(row=2, column=1, pady=10, sticky=tk.W + tk.E)

    def apply(self):
        build_dir = self.build_dir_entry.get()
        other_options = self.other_options_entry.get()
        self.result = (build_dir, other_options)


class TutorialDialog(simpledialog.Dialog):
    def body(self, master):
        master.configure(bg="dark gray")
        ttk.Label(master, text="Tutorial: How to Use Meson Build GUI", background="dark gray", foreground="white", font=("Helvetica", 10, "bold")).grid(
            row=0, column=0, columnspan=2, pady=10
        )

        self.notebook = ttk.Notebook(master)
        self.notebook.grid(row=1, column=0, columnspan=2, pady=10)

        steps = [
            ("Step 1: Setup", "  - Click the 'Setup' button to configure your project.\n  - Specify the build directory and any additional options."),
            ("Step 2: Compile", "  - Use the 'Compile' button to build your project using Ninja.\n  - Make sure the build directory is correctly set."),
            ("Step 3: Test", "  - Click 'Test' to run the project's tests."),
            ("Step 4: Install", "  - The 'Install' button installs the built project."),
            ("Other Features", "  - 'Version': Displays the installed Meson version.\n  - 'Introspection': Explore project metadata.\n  - 'Clear Terminal': Clears the terminal output.\n  - 'Tool Info': Provides general information about this GUI.\n\nEnjoy using the Meson Build GUI for your projects!")
        ]

        for title, content in steps:
            frame = ttk.Frame(self.notebook, padding=10)
            self.notebook.add(frame, text=title)
            text = ScrolledText(frame, wrap=tk.WORD, height=10, width=60, background="black", foreground="white")
            text.insert(tk.END, content)
            text.configure(state=tk.DISABLED)
            text.pack(expand=True, fill=tk.BOTH)

    def apply(self):
        pass


class MesonBuildGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Meson Build GUI")
        self.root.geometry("660x400")
        self.root.resizable(False, False)  # Disable window resizing

        self.root.configure(bg="dark gray")
        self.create_widgets()

    def create_widgets(self):
        ttk.Style().configure("Blue.TButton", foreground="black", background="#ADD8E6", font=("Helvetica", 10, "bold"))

        self.setup_button = ttk.Button(
            self.root, text="Setup",
            command=self.setup_project,
            style="Blue.TButton"
        )
        self.configure_button = ttk.Button(
            self.root,
            text="Configure",
            command=self.configure_project,
            style="Blue.TButton",
        )
        self.compile_button = ttk.Button(
            self.root,
            text="Compile",
            command=self.compile_project,
            style="Blue.TButton",
        )
        self.test_button = ttk.Button(
            self.root, text="Test", command=self.test_project, style="Blue.TButton"
        )
        self.install_button = ttk.Button(
            self.root,
            text="Install",
            command=self.install_project,
            style="Blue.TButton",
        )

        self.version_button = ttk.Button(
            self.root, text="Version", command=self.show_version, style="Blue.TButton"
        )
        self.introspect_button = ttk.Button(
            self.root,
            text="Introspection",
            command=self.show_introspection,
            style="Blue.TButton",
        )
        self.clear_terminal_button = ttk.Button(
            self.root,
            text="Clear Terminal",
            command=self.clear_terminal,
            style="Blue.TButton",
        )
        self.tool_info_button = ttk.Button(
            self.root,
            text="Tool Info",
            command=self.get_tool_info,
            style="Blue.TButton",
        )
        self.tutorial_button = ttk.Button(
            self.root, text="Tutorial", command=self.show_tutorial, style="Blue.TButton"
        )

        self.source_dir_label = ttk.Label(
            self.root, text="Source Directory:", background="dark gray", font=("Helvetica", 10, "bold")
        )
        self.source_dir_entry = ttk.Entry(self.root, width=50)
        self.source_dir_entry.insert(0, os.getcwd())

        self.build_dir_label = ttk.Label(
            self.root, text="Build Directory:", background="dark gray", font=("Helvetica", 10, "bold")
        )
        self.build_dir_entry = ttk.Entry(self.root, width=50)
        self.build_dir_entry.insert(0, os.path.join(os.getcwd(), "builddir"))

        self.terminal = ScrolledText(
            self.root,
            height=10,
            state=tk.DISABLED,
            wrap=tk.WORD,
            background="black",
            foreground="white",
            font="helvetica 10 bold",
        )

        row1_buttons = [
            self.setup_button,
            self.configure_button,
            self.compile_button,
            self.test_button,
            self.install_button,
        ]

        for col, button in enumerate(row1_buttons):
            button.grid(row=0, column=col, pady=10, padx=10, sticky=tk.W + tk.E)

        self.source_dir_label.grid(row=1, column=0, pady=5, padx=10, sticky=tk.W)
        self.source_dir_entry.grid(
            row=1, column=1, pady=5, padx=10, sticky=tk.W + tk.E, columnspan=3
        )
        self.build_dir_label.grid(row=2, column=0, pady=5, padx=10, sticky=tk.W)
        self.build_dir_entry.grid(
            row=2, column=1, pady=5, padx=10, sticky=tk.W + tk.E, columnspan=3
        )

        self.terminal.grid(
            row=3,
            column=0,
            columnspan=5,
            pady=10,
            padx=10,
            sticky=tk.W + tk.E + tk.N + tk.S,
        )

        row2_buttons = [
            self.version_button,
            self.introspect_button,
            self.clear_terminal_button,
            self.tool_info_button,
            self.tutorial_button,
        ]

        for col, button in enumerate(row2_buttons):
            button.grid(row=4, column=col, pady=10, padx=10, sticky=tk.W + tk.E)

    def run_command(self, command, cwd=None):
        process = subprocess.Popen(
            command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, cwd=cwd
        )

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
            threading.Thread(
                target=self.run_setup_thread, args=(build_dir, other_options)
            ).start()

    def run_setup_thread(self, build_dir, other_options):
        source_dir = self.source_dir_entry.get()
        self.update_terminal(f"Setting up the project in {build_dir}...\n")
        command = ["meson", "setup", build_dir]

        if other_options:
            command += other_options.split()

        self.run_command(command, cwd=source_dir)

    def configure_project(self):
        build_dir, other_options = ConfigureDialog(self.root).result

        if build_dir:
            threading.Thread(
                target=self.run_configure_thread, args=(build_dir, other_options)
            ).start()

    def run_configure_thread(self, build_dir, other_options):
        source_dir = self.source_dir_entry.get()
        self.update_terminal(f"Configuring the project in {build_dir}...\n")
        command = ["meson", "configure", build_dir]

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
            self.update_terminal(
                "Build directory not specified. Introspecting source directory...\n"
            )
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
        self.update_terminal(
            "This tool assists in building Meson projects using a graphical user interface.\n"
        )
        self.update_terminal(
            "It provides options to set up, compile, test, install, and get information about the Meson project.\n\n"
        )
        self.update_terminal("Created by Dreamer, lead developer at Fossil Logic.\n")

    def show_tutorial(self):
        TutorialDialog(self.root)


if __name__ == "__main__":
    root = tk.Tk()
    app = MesonBuildGUI(root)
    root.mainloop()
