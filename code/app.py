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
from tkinter import messagebox
from tkinter import filedialog
from tkinter.scrolledtext import ScrolledText
import subprocess
import threading
import os
import webbrowser
import configparser


class AppInfo:
    def __init__(self):
        self.name = "Meson Build GUI"
        self.version = "0.1.0"
        self.author = "Michael Gene Brockus (Dreamer)"
        self.email = "michaelbrockus@gmail.com"
        
    def get_info(self):
        return f"{self.name} v{self.version} by {self.author} ({self.email})"


class AppSettings:
    def __init__(self):
        self.config_file = "settings.ini"
        self.config = configparser.ConfigParser()
        self.load_settings()

    def load_settings(self):
        if not os.path.exists(self.config_file):
            self.create_default_settings()
        self.config.read(self.config_file)

    def create_default_settings(self):
        self.config["Settings"] = {"build_dir": "builddir", "theme": "meson"}
        with open(self.config_file, "w") as configfile:
            self.config.write(configfile)

    def get_theme(self):
        return self.config.get("Settings", "theme", fallback="meson")

    def set_theme(self, theme):
        self.config["Settings"]["theme"] = theme
        with open(self.config_file, "w") as configfile:
            self.config.write(configfile)

    def get_build_dir(self):
        return self.config.get("Settings", "build_dir", fallback="builddir")

    def set_build_dir(self, build_dir):
        self.config["Settings"]["build_dir"] = build_dir
        with open(self.config_file, "w") as configfile:
            self.config.write(configfile)


class AppThemes:
    def __init__(self, root):
        self.root = root
        self.root.title("App Themes")
        self.root.geometry("300x200")
        self.root.resizable(False, False)

        self.create_widgets()

    def create_widgets(self):
        self.theme_var = tk.StringVar()
        self.theme_var.set("light")

        self.light_theme_radio = ttk.Radiobutton(
            self.root,
            text="Light",
            variable=self.theme_var,
            value="light",
            command=self.set_theme,
        )
        self.dark_theme_radio = ttk.Radiobutton(
            self.root,
            text="Dark",
            variable=self.theme_var,
            value="dark",
            command=self.set_theme,
        )
        self.meson_theme_radio = ttk.Radiobutton(
            self.root,
            text="Meson",
            variable=self.theme_var,
            value="meson",
            command=self.set_theme,
        )

        self.light_theme_radio.pack(pady=10)
        self.dark_theme_radio.pack(pady=10)
        self.meson_theme_radio.pack(pady=10)

    def set_theme(self):
        theme = self.theme_var.get()
        self.root.event_generate("<<ThemeChanged>>", when="tail", theme=theme)
        self.root.destroy()


class SetupDialog(simpledialog.Dialog):
    def __init__(self, parent, theme):
        self.theme = theme
        super().__init__(parent)

    def body(self, master):
        self.apply_theme()
        ttk.Label(
            master,
            text="Meson Setup Options",
        ).grid(row=0, column=0, columnspan=2, pady=10)

        ttk.Label(master, text="Build Directory:").grid(row=1, column=0, sticky=tk.W)
        self.build_dir_entry = ttk.Entry(master, width=40)
        self.build_dir_entry.insert(0, "builddir")
        self.build_dir_entry.grid(row=1, column=1, pady=10, sticky=tk.W + tk.E)

        ttk.Label(master, text="Other Options:").grid(row=2, column=0, sticky=tk.W)
        self.other_options_entry = ttk.Entry(master, width=40)
        self.other_options_entry.grid(row=2, column=1, pady=10, sticky=tk.W + tk.E)

    def apply(self):
        build_dir = self.build_dir_entry.get().strip()
        other_options = self.other_options_entry.get().strip()
        if not build_dir:
            tk.messagebox.showerror("Error", "Build directory cannot be empty.")
            self.result = None
        else:
            self.result = (build_dir, other_options)

    def cancel(self, event=None):
        self.result = None
        super().cancel(event)

    def ok(self, event=None):
        self.apply()
        if self.result is not None:
            self.cancel()

    def apply_theme(self):
        if self.theme == "light":
            self.configure(bg="white")
            for widget in self.winfo_children():
                if isinstance(widget, ttk.Label):
                    widget.configure(background="white", foreground="black")
                elif isinstance(widget, ttk.Entry):
                    widget.configure(background="white", foreground="black")
                elif isinstance(widget, ttk.Button):
                    widget.configure(background="white", foreground="black")
        elif self.theme == "dark":
            self.configure(bg="black")
            for widget in self.winfo_children():
                if isinstance(widget, ttk.Label):
                    widget.configure(background="black", foreground="light blue")
                elif isinstance(widget, ttk.Entry):
                    widget.configure(background="black", foreground="light blue")
                elif isinstance(widget, ttk.Button):
                    widget.configure(background="black", foreground="light blue")
        elif self.theme == "meson":
            self.configure(bg="dark gray")
            for widget in self.winfo_children():
                if isinstance(widget, ttk.Label):
                    widget.configure(background="dark gray", foreground="black")
                elif isinstance(widget, ttk.Entry):
                    widget.configure(background="dark gray", foreground="black")
                elif isinstance(widget, ttk.Button):
                    widget.configure(background="#ADD8E6", foreground="black")


class ConfigureDialog(simpledialog.Dialog):
    def __init__(self, parent, theme):
        self.theme = theme
        super().__init__(parent)

    def body(self, master):
        self.apply_theme()
        ttk.Label(
            master,
            text="Meson Configure Options",
        ).grid(row=0, column=0, columnspan=2, pady=10)

        ttk.Label(master, text="Build Directory:").grid(row=1, column=0, sticky=tk.W)
        self.build_dir_entry = ttk.Entry(master, width=40)
        self.build_dir_entry.insert(0, "builddir")
        self.build_dir_entry.grid(row=1, column=1, pady=10, sticky=tk.W + tk.E)

        ttk.Label(master, text="Other Options:").grid(row=2, column=0, sticky=tk.W)
        self.other_options_entry = ttk.Entry(master, width=40)
        self.other_options_entry.grid(row=2, column=1, pady=10, sticky=tk.W + tk.E)

    def apply(self):
        build_dir = self.build_dir_entry.get().strip()
        other_options = self.other_options_entry.get().strip()
        if not build_dir:
            tk.messagebox.showerror("Error", "Build directory cannot be empty.")
            self.result = None
        else:
            self.result = (build_dir, other_options)

    def cancel(self, event=None):
        self.result = None
        super().cancel(event)

    def ok(self, event=None):
        self.apply()
        if self.result is not None:
            self.cancel()

    def apply_theme(self):
        if self.theme == "light":
            self.configure(bg="white")
            for widget in self.winfo_children():
                if isinstance(widget, ttk.Label):
                    widget.configure(background="white", foreground="black")
                elif isinstance(widget, ttk.Entry):
                    widget.configure(background="white", foreground="black")
                elif isinstance(widget, ttk.Button):
                    widget.configure(background="white", foreground="black")
        elif self.theme == "dark":
            self.configure(bg="black")
            for widget in self.winfo_children():
                if isinstance(widget, ttk.Label):
                    widget.configure(background="black", foreground="light blue")
                elif isinstance(widget, ttk.Entry):
                    widget.configure(background="black", foreground="light blue")
                elif isinstance(widget, ttk.Button):
                    widget.configure(background="black", foreground="light blue")
        elif self.theme == "meson":
            self.configure(bg="dark gray")
            for widget in self.winfo_children():
                if isinstance(widget, ttk.Label):
                    widget.configure(background="dark gray", foreground="black")
                elif isinstance(widget, ttk.Entry):
                    widget.configure(background="dark gray", foreground="black")
                elif isinstance(widget, ttk.Button):
                    widget.configure(background="#ADD8E6", foreground="black")


class TutorialDialog(simpledialog.Dialog):
    def __init__(self, parent, theme):
        self.theme = theme
        super().__init__(parent)

    def body(self, master):
        self.title("Meson UI Tutorial")
        self.apply_theme()
        ttk.Label(
            master,
            text="Tutorial: How to Use Meson Build GUI",
            font=("Helvetica", 10, "bold"),
        ).grid(row=0, column=0, columnspan=2, pady=10)
        self.geometry("600x400")

        self.notebook = ttk.Notebook(master)
        self.notebook.grid(row=1, column=0, columnspan=2, pady=10)

        self.create_tab()

    def create_tab(self):
        steps = [
            (
                "Step 1: Setup",
                "  - Click the 'Setup' button to configure your project.\n  - Specify the build directory and any additional options.\n  - This step initializes the build environment and prepares the project for compilation.",
            ),
            (
                "Step 2: Compile",
                "  - Use the 'Compile' button to build your project using Ninja.\n  - Make sure the build directory is correctly set.\n  - This step compiles the source code into executable binaries or libraries.",
            ),
            (
                "Step 3: Test",
                "  - Click 'Test' to run the project's tests.\n  - Ensure that the tests are properly configured in your Meson build files.\n  - This step helps verify that your code is working as expected.",
            ),
            (
                "Step 4: Install",
                "  - The 'Install' button installs the built project.\n  - This step copies the compiled binaries and other necessary files to the installation directory.\n  - Make sure you have the necessary permissions to install the files.",
            ),
            (
                "Other Features",
                "  - 'Version': Displays the installed Meson version.\n  - 'Introspection': Explore project metadata.\n  - 'Clear Terminal': Clears the terminal output.\n  - 'Tool Info': Provides general information about this GUI.\n\nEnjoy using the Meson Build GUI for your projects!",
            ),
        ]

        for title, content in steps:
            frame = ttk.Frame(self.notebook, padding=10)
            self.notebook.add(frame, text=title)
            text = ScrolledText(
                frame,
                wrap=tk.WORD,
                height=30,
                width=60,
            )
            text.insert(tk.END, content)
            text.configure(state=tk.DISABLED)
            text.pack(expand=True, fill=tk.BOTH)

    def buttonbox(self):
        box = tk.Frame(self)

        button_close = ttk.Button(
            box, text="Close", command=self.ok, style="Blue.TButton"
        )
        button_close.pack(pady=10)

        self.bind("<Return>", self.ok)
        self.bind("<Escape>", self.cancel)

        box.pack()
        box.pack(pady=10)

    def apply_theme(self):
        if self.theme == "light":
            self.configure(bg="white")
            for widget in self.winfo_children():
                if isinstance(widget, ttk.Label):
                    widget.configure(background="white", foreground="black")
                elif isinstance(widget, ttk.Entry):
                    widget.configure(background="white", foreground="black")
                elif isinstance(widget, ttk.Button):
                    widget.configure(background="white", foreground="black")
        elif self.theme == "dark":
            self.configure(bg="black")
            for widget in self.winfo_children():
                if isinstance(widget, ttk.Label):
                    widget.configure(background="black", foreground="light blue")
                elif isinstance(widget, ttk.Entry):
                    widget.configure(background="black", foreground="light blue")
                elif isinstance(widget, ttk.Button):
                    widget.configure(background="black", foreground="light blue")
        elif self.theme == "meson":
            self.configure(bg="dark gray")
            for widget in self.winfo_children():
                if isinstance(widget, ttk.Label):
                    widget.configure(background="dark gray", foreground="black")
                elif isinstance(widget, ttk.Entry):
                    widget.configure(background="dark gray", foreground="black")
                elif isinstance(widget, ttk.Button):
                    widget.configure(background="#ADD8E6", foreground="black")


class MesonBuild:
    def __init__(self, source_dir, build_dir):
        self.source_dir = source_dir
        self.build_dir = build_dir

    def setup(self, options=""):
        command = ["meson", "setup", self.build_dir, self.source_dir] + options.split()
        return self.run_command(command)

    def configure(self, options=""):
        command = ["meson", "configure", self.build_dir] + options.split()
        return self.run_command(command)

    def compile(self):
        command = ["meson", "compile", "-C", self.build_dir]
        return self.run_command(command)

    def test(self):
        command = ["meson", "test", "-C", self.build_dir]
        return self.run_command(command)

    def install(self):
        command = ["meson", "install", "-C", self.build_dir]
        return self.run_command(command)

    def introspect(self, options=""):
        command = ["meson", "introspect", self.build_dir] + options.split()
        return self.run_command(command)

    def rewrite(self, options=""):
        command = ["meson", "rewrite"] + options.split()
        return self.run_command(command)

    def dist(self, options=""):
        command = ["meson", "dist"] + options.split()
        return self.run_command(command)

    def devenv(self, options=""):
        command = ["meson", "devenv"] + options.split()
        return self.run_command(command)

    def wrap(self, options=""):
        command = ["meson", "wrap"] + options.split()
        return self.run_command(command)

    def subprojects(self, options=""):
        command = ["meson", "subprojects"] + options.split()
        return self.run_command(command)

    def init(self, options=""):
        command = ["meson", "init"] + options.split()
        return self.run_command(command)

    def run_command(self, command):
        try:
            result = subprocess.run(command, capture_output=True, text=True, check=True)
            return result.stdout
        except subprocess.CalledProcessError as e:
            return f"Command '{' '.join(command)}' failed with error: {e.stderr}"
        except Exception as e:
            return f"An unexpected error occurred: {str(e)}"


class MesonBuildGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Meson Build GUI")
        self.root.geometry("660x400")
        self.root.resizable(False, False)  # Disable window resizing

        self.theme = "meson"
        self.apply_styles()
        self.create_widgets()
        self.apply_theme()

        self.config_file = "settings.ini"
        self.config = configparser.ConfigParser()
        self.load_settings()

        self.meson_build = MesonBuild(
            self.source_dir_entry.get(), self.build_dir_entry.get()
        )

    def load_settings(self):
        if not os.path.exists(self.config_file):
            self.create_default_settings()
        self.config.read(self.config_file)
        self.build_dir_entry.delete(0, tk.END)
        self.build_dir_entry.insert(0, os.path.join(os.getcwd(), self.config["Settings"]["build_dir"]))

    def create_default_settings(self):
        self.config["Settings"] = {"build_dir": "builddir", "theme": "meson"}
        with open(self.config_file, "w") as configfile:
            self.config.write(configfile)

    def apply_styles(self):
        self.style = ttk.Style()
        self.style.configure(
            "Blue.TButton",
            foreground="black",
            background="#ADD8E6",
            font=("Helvetica", 10, "bold"),
        )

    def create_widgets(self):
        self.create_menu()

        self.setup_button = ttk.Button(
            self.root, text="Setup", command=self.setup_project, style="Blue.TButton"
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
            self.root,
            text="Source Directory:",
            background="dark gray",
            font=("Helvetica", 10, "bold"),
        )
        self.source_dir_entry = ttk.Entry(self.root, width=50)
        self.source_dir_entry.insert(0, os.getcwd())
        self.source_dir_button = ttk.Button(
            self.root,
            text="Browse",
            command=self.browse_source_dir,
            style="Blue.TButton",
        )

        self.build_dir_label = ttk.Label(
            self.root,
            text="Build Directory:",
            background="dark gray",
            font=("Helvetica", 10, "bold"),
        )
        self.build_dir_entry = ttk.Entry(self.root, width=50)
        self.build_dir_entry.insert(0, os.path.join(os.getcwd(), "builddir"))
        self.clear_paths_button = ttk.Button(
            self.root,
            text="Clear Paths",
            command=self.clear_paths,
            style="Blue.TButton",
        )

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
        self.source_dir_button.grid(
            row=1, column=4, pady=5, padx=10, sticky=tk.W + tk.E
        )

        self.build_dir_label.grid(row=2, column=0, pady=5, padx=10, sticky=tk.W)
        self.build_dir_entry.grid(
            row=2, column=1, pady=5, padx=10, sticky=tk.W + tk.E, columnspan=3
        )
        self.clear_paths_button.grid(
            row=2, column=4, pady=5, padx=10, sticky=tk.W + tk.E
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

    def create_menu(self):
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)

        options_menu = tk.Menu(menubar, tearoff=0)
        themes_menu = tk.Menu(options_menu, tearoff=0)
        themes_menu.add_command(label="Light", command=lambda: self.set_theme("light"))
        themes_menu.add_command(label="Dark", command=lambda: self.set_theme("dark"))
        themes_menu.add_command(label="Meson", command=lambda: self.set_theme("meson"))
        options_menu.add_cascade(label="Themes", menu=themes_menu)
        options_menu.add_command(label="Tutorial", command=self.show_tutorial)
        options_menu.add_command(label="Version", command=self.show_version)
        options_menu.add_command(label="Clear Terminal", command=self.clear_terminal)
        options_menu.add_command(label="Help", command=self.get_tool_info)
        menubar.add_cascade(label="Options", menu=options_menu)

        actions_menu = tk.Menu(menubar, tearoff=0)
        actions_menu.add_command(label="Setup", command=self.setup_project)
        actions_menu.add_command(label="Configure", command=self.configure_project)
        actions_menu.add_command(label="Compile", command=self.compile_project)
        actions_menu.add_command(label="Test", command=self.test_project)
        actions_menu.add_command(label="Introspection", command=self.show_introspection)
        actions_menu.add_command(label="Install", command=self.install_project)
        menubar.add_cascade(label="Actions", menu=actions_menu)

        support_menu = tk.Menu(menubar, tearoff=0)
        support_menu.add_command(
            label="Meson Website",
            command=lambda: self.open_url("https://mesonbuild.com/"),
        )
        support_menu.add_command(
            label="Documentation",
            command=lambda: self.open_url(
                "https://fossillogic.com/docs/meson-ui-overview"
            ),
        )
        support_menu.add_command(
            label="Repository",
            command=lambda: self.open_url("https://github.com/fossillogic/meson-ui"),
        )
        support_menu.add_command(
            label="Report Issue",
            command=lambda: self.open_url(
                "https://github.com/fossillogic/meson-ui/issues"
            ),
        )
        menubar.add_cascade(label="Support", menu=support_menu)

    def open_url(self, url):
        webbrowser.open(url)

    def set_theme(self, theme):
        self.theme = theme
        self.apply_theme()

    def apply_theme(self):
        if self.theme == "light":
            self.root.configure(bg="white")
            self.source_dir_label.configure(background="white", foreground="black")
            self.build_dir_label.configure(background="white", foreground="black")
            self.terminal.configure(background="black", foreground="white")
            self.style.configure("Blue.TButton", background="white", foreground="black")
        elif self.theme == "dark":
            self.root.configure(bg="black")
            self.source_dir_label.configure(background="black", foreground="light blue")
            self.build_dir_label.configure(background="black", foreground="light blue")
            self.terminal.configure(background="black", foreground="light blue")
            self.style.configure("Blue.TButton", background="black", foreground="blue")
        elif self.theme == "meson":
            self.root.configure(bg="dark gray")
            self.source_dir_label.configure(background="dark gray", foreground="black")
            self.build_dir_label.configure(background="dark gray", foreground="black")
            self.terminal.configure(background="black", foreground="white")
            self.style.configure(
                "Blue.TButton", background="#ADD8E6", foreground="black"
            )

    def browse_source_dir(self):
        try:
            directory = tk.filedialog.askdirectory()
            if directory:
                self.source_dir_entry.delete(0, tk.END)
                self.source_dir_entry.insert(0, directory)
                self.build_dir_entry.delete(0, tk.END)
                self.build_dir_entry.insert(0, os.path.join(directory, "builddir"))
                self.meson_build.source_dir = directory
                self.meson_build.build_dir = os.path.join(directory, "builddir")
        except Exception as e:
            tk.messagebox.showerror("Error", str(e))

    def clear_paths(self):
        try:
            self.source_dir_entry.delete(0, tk.END)
            self.build_dir_entry.delete(0, tk.END)
        except Exception as e:
            tk.messagebox.showerror("Error", str(e))

    def validate_directory(self, directory):
        if not os.path.isdir(directory):
            tk.messagebox.showerror("Error", f"Directory '{directory}' does not exist.")
            return False
        return True

    def update_terminal(self, message):
        self.terminal.configure(state=tk.NORMAL)
        self.terminal.insert(tk.END, message, "custom")
        self.terminal.yview(tk.END)
        self.terminal.configure(state=tk.DISABLED)

    def setup_project(self):
        try:
            result = SetupDialog(self.root, self.theme).result
            if result is None:
                return
            build_dir, other_options = result

            if build_dir and self.validate_directory(build_dir):
                threading.Thread(
                    target=self.run_setup_thread, args=(build_dir, other_options)
                ).start()
        except Exception as e:
            tk.messagebox.showerror("Error", str(e))

    def run_setup_thread(self, build_dir, other_options):
        try:
            self.meson_build.build_dir = build_dir
            self.update_terminal(f"Setting up the project in {build_dir}...\n")
            output = self.meson_build.setup(other_options)
            self.update_terminal(output)
        except Exception as e:
            self.update_terminal(f"Error: {str(e)}\n")

    def configure_project(self):
        try:
            result = ConfigureDialog(self.root, self.theme).result
            if result is None:
                return
            build_dir, other_options = result

            if build_dir and self.validate_directory(build_dir):
                threading.Thread(
                    target=self.run_configure_thread, args=(build_dir, other_options)
                ).start()
        except Exception as e:
            tk.messagebox.showerror("Error", str(e))

    def run_configure_thread(self, build_dir, other_options):
        try:
            self.meson_build.build_dir = build_dir
            self.update_terminal(f"Configuring the project in {build_dir}...\n")
            output = self.meson_build.configure(other_options)
            self.update_terminal(output)
        except Exception as e:
            self.update_terminal(f"Error: {str(e)}\n")

    def compile_project(self):
        try:
            build_dir = self.build_dir_entry.get()
            if self.validate_directory(build_dir):
                threading.Thread(target=self.run_compile_thread).start()
        except Exception as e:
            tk.messagebox.showerror("Error", str(e))

    def run_compile_thread(self):
        try:
            build_dir = self.build_dir_entry.get()
            self.meson_build.build_dir = build_dir
            self.update_terminal(f"Compiling the project in {build_dir}...\n")
            output = self.meson_build.compile()
            self.update_terminal(output)
        except Exception as e:
            self.update_terminal(f"Error: {str(e)}\n")

    def test_project(self):
        try:
            build_dir = self.build_dir_entry.get()
            if self.validate_directory(build_dir):
                threading.Thread(target=self.run_test_thread).start()
        except Exception as e:
            tk.messagebox.showerror("Error", str(e))

    def run_test_thread(self):
        try:
            build_dir = self.build_dir_entry.get()
            self.meson_build.build_dir = build_dir
            self.update_terminal(f"Testing the project in {build_dir}...\n")
            output = self.meson_build.test()
            self.update_terminal(output)
        except Exception as e:
            self.update_terminal(f"Error: {str(e)}\n")

    def install_project(self):
        try:
            build_dir = self.build_dir_entry.get()
            if self.validate_directory(build_dir):
                threading.Thread(target=self.run_install_thread).start()
        except Exception as e:
            tk.messagebox.showerror("Error", str(e))

    def run_install_thread(self):
        try:
            build_dir = self.build_dir_entry.get()
            self.meson_build.build_dir = build_dir
            self.update_terminal(f"Installing the project in {build_dir}...\n")
            output = self.meson_build.install()
            self.update_terminal(output)
        except Exception as e:
            self.update_terminal(f"Error: {str(e)}\n")

    def show_version(self):
        try:
            threading.Thread(target=self.run_version_thread).start()
        except Exception as e:
            tk.messagebox.showerror("Error", str(e))

    def run_version_thread(self):
        try:
            self.update_terminal("Meson Version:\n")
            output = self.meson_build.run_command(["meson", "--version"])
            self.update_terminal(output)
        except Exception as e:
            self.update_terminal(f"Error: {str(e)}\n")

    def show_introspection(self):
        try:
            threading.Thread(target=self.run_introspection_thread).start()
        except Exception as e:
            tk.messagebox.showerror("Error", str(e))

    def run_introspection_thread(self):
        try:
            build_dir = self.build_dir_entry.get()
            self.meson_build.build_dir = build_dir
            self.update_terminal(f"Introspecting build directory {build_dir}...\n")
            output = self.meson_build.introspect()
            self.update_terminal(output)
        except Exception as e:
            self.update_terminal(f"Error: {str(e)}\n")

    def clear_terminal(self):
        try:
            self.terminal.configure(state=tk.NORMAL)
            self.terminal.delete("1.0", tk.END)
            self.terminal.configure(state=tk.DISABLED)
        except Exception as e:
            tk.messagebox.showerror("Error", str(e))

    def get_tool_info(self):
        try:
            threading.Thread(target=self.run_tool_info_thread).start()
        except Exception as e:
            tk.messagebox.showerror("Error", str(e))

    def run_tool_info_thread(self):
        try:
            self.update_terminal("Meson Build GUI Information:\n")
            self.update_terminal(
                "This tool assists in building Meson projects using a graphical user interface.\n"
            )
            self.update_terminal(
                "It provides options to set up, compile, test, install, and get information about the Meson project.\n\n"
            )
            self.update_terminal(
                "Created by Dreamer, lead developer at Fossil Logic.\n"
            )
        except Exception as e:
            self.update_terminal(f"Error: {str(e)}\n")

    def show_tutorial(self):
        try:
            TutorialDialog(self.root, self.theme)
        except Exception as e:
            tk.messagebox.showerror("Error", str(e))


if __name__ == "__main__":
    root = tk.Tk()
    app = MesonBuildGUI(root)
    root.mainloop()
