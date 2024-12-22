import os
import sys, logging
import importlib.util
from backend.logger_config import setup_logger


def concatenate_and_run_tests(solution_file, intern_id, assignment, test_case_folder):
    testcase_logger = setup_logger("testcase")
    try:
        if isinstance(intern_id, int):
            intern_id = f"{intern_id}"
        if isinstance(solution_file, int) or not solution_file.endswith(".py"):
            solution_file = f"{solution_file}.py"
        # Construct full paths
        base_path = os.path.join('Input', assignment, intern_id)
        test_case_path = os.path.join('Input', assignment, test_case_folder)
        
        # Full file paths
        solution_file_path = os.path.join(base_path, solution_file)
        test_case_file_path = os.path.join(test_case_path, solution_file)
        
        # Log start of testing
        testcase_logger.info(f"\n-------------------------run_test_cases.py-------------\n"
                             f"Running Test Cases For\n"
                             f"Assignment: {assignment}\n"
                             f"Intern: {intern_id}\n"
                             f"Solution: {solution_file}")
        
        # Read solution and test case files
        with open(solution_file_path, 'r') as sol_file:
            solution_code = sol_file.read()
        
        with open(test_case_file_path, 'r') as test_file:
            test_code = test_file.read()
        
        # Concatenate the files
        combined_code = solution_code + '\n' + test_code
        
        # Create a temporary file with combined code
        temp_file_path = os.path.join(base_path, f'temp_{solution_file}')
        with open(temp_file_path, 'w') as temp_file:
            temp_file.write(combined_code)
        
        # Dynamically execute the combined file
        spec = importlib.util.spec_from_file_location("combined_module", temp_file_path)
        module = importlib.util.module_from_spec(spec)
        sys.path.insert(0, base_path)
        spec.loader.exec_module(module)
        
        # Get the solution and test_solution functions
        solution_function = getattr(module, 'solution', None)
        test_solution = getattr(module, 'test_solution', None)
        
        # Validate functions
        if not callable(solution_function):
            testcase_logger.error(f"'solution' function not found in {solution_file}")
            print(f"'solution' function not found in {solution_file}")
            return 0, []
        
        if not callable(test_solution):
            testcase_logger.error(f"'test_solution' function not found in {solution_file}")
            print(f"'test_solution' function not found in {solution_file}")
            return 0, []
        
        print("both found")

        # Run the tests
        passed, not_passed = test_solution(solution_function)
        
        if len(passed) + len(not_passed) == 0:
            testcase_logger.error("No Test Cases were Run!")
            print("No Test Cases were Run!")
            return 0, []
        
        # Calculate score
        score = (len(passed) / (len(passed) + len(not_passed))) * 100
        testcase_logger.info(f"Test Cases Passed {len(passed)}, Out of {len(not_passed) + len(passed)}")
        print(f"Test Cases Passed {len(passed)}, Out of {len(not_passed) + len(passed)}")
        
        # Clean up temporary file
        os.remove(temp_file_path)
        
        return score, not_passed
    
    except FileNotFoundError as e:
        testcase_logger.error(f"Error: File not found - {e}")
        print(f"Error: File not found - {e}")
        return 0, []
    except Exception as e:
        testcase_logger.error(f"Unexpected error: {e}")
        print(f"Unexpected error: {e}")
        return 0, []

if __name__ == '__main__':
    concatenate_and_run_tests('1.py', '3', 'Python_DSA_2', 'Test Cases')