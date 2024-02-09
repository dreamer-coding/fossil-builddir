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
import unittest
from unittest.mock import patch, MagicMock
from tkinter import Tk
from code.app import MesonBuildGUI, SetupDialog

class TestMesonBuildGUI(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.root = Tk()
        cls.app = MesonBuildGUI(cls.root)

    @classmethod
    def tearDownClass(cls):
        cls.root.destroy()

    def setUp(self):
        # Mock the terminal's insert method
        self.app.update_terminal = MagicMock()

    def test_run_setup_thread(self):
        with patch('subprocess.Popen') as mock_popen:
            # Mock the subprocess.Popen object
            mock_process = MagicMock()
            mock_process.stdout.readline.return_value = "Mock Output"
            mock_process.communicate.return_value = ("", "")
            mock_popen.return_value = mock_process

            # Run the setup thread
            self.app.run_setup_thread("build_dir", "--option=value")

            # Assertions
            mock_popen.assert_called_once_with(["meson", "setup", "build_dir", "--option=value"], cwd="source_dir")
            self.app.update_terminal.assert_called_with("Mock Output")

    def test_run_compile_thread(self):
        with patch('subprocess.Popen') as mock_popen:
            # Mock the subprocess.Popen object
            mock_process = MagicMock()
            mock_process.stdout.readline.return_value = "Mock Output"
            mock_process.communicate.return_value = ("", "")
            mock_popen.return_value = mock_process

            # Run the compile thread
            self.app.run_compile_thread()

            # Assertions
            mock_popen.assert_called_once_with(["ninja", "-C", "build_dir"], cwd="build_dir")
            self.app.update_terminal.assert_called_with("Mock Output")

    def test_run_test_thread(self):
        with patch('subprocess.Popen') as mock_popen:
            # Mock the subprocess.Popen object
            mock_process = MagicMock()
            mock_process.stdout.readline.return_value = "Mock Output"
            mock_process.communicate.return_value = ("", "")
            mock_popen.return_value = mock_process

            # Run the test thread
            self.app.run_test_thread()

            # Assertions
            mock_popen.assert_called_once_with(["ninja", "-C", "build_dir", "test"], cwd="build_dir")
            self.app.update_terminal.assert_called_with("Mock Output")

    def test_run_install_thread(self):
        with patch('subprocess.Popen') as mock_popen:
            # Mock the subprocess.Popen object
            mock_process = MagicMock()
            mock_process.stdout.readline.return_value = "Mock Output"
            mock_process.communicate.return_value = ("", "")
            mock_popen.return_value = mock_process

            # Run the install thread
            self.app.run_install_thread()

            # Assertions
            mock_popen.assert_called_once_with(["ninja", "-C", "build_dir", "install"], cwd="build_dir")
            self.app.update_terminal.assert_called_with("Mock Output")

if __name__ == '__main__':
    unittest.main()
