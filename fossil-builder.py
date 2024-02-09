import sys
import os
import unittest

# Add the root directory to the Python path so you can import project modules.
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

if __name__ == "__main__":
    if len(sys.argv) == 1:
        # If no command-line arguments provided, run the main program (main.py).
        from code.main import main
        main()
    elif sys.argv[1] == "test":
        # If the argument "test" is provided, run the test suite.
        from test import test_cases
        suite = unittest.TestLoader().loadTestsFromModule(test_cases)
        unittest.TextTestRunner(verbosity=2).run(suite)
    else:
        print("Usage: python run_project.py [test]")
