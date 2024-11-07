import importlib
from backend.logger_config import setup_logger

# Create a logger for grading
grading_logger = setup_logger()

def dynamic_import_and_test(solution_file, intern_id, assignment, test_case_folder):
    # Construct module paths
    solution_module_name = f"Input.{assignment}.{intern_id}.{solution_file}"
    test_case_module_name = f"Input.{assignment}.{test_case_folder}.{solution_file}"

    grading_logger.info(f"\n-------------------------run_test_cases.py-------------\nRunning Test Cases For\nAssignment: {assignment}\nIntern: {intern_id}")
    try:
        # Dynamically import solution and test_case modules
        solution_module = importlib.import_module(solution_module_name)
        test_case_module = importlib.import_module(test_case_module_name)
       
        # Get the solution function and test_solution function
        solution_function = getattr(solution_module, 'solution', None)
        test_solution = getattr(test_case_module, 'test_solution', None)
        
        if not callable(solution_function):
            grading_logger.error(f"'solution' function not found in {solution_module_name}")
        if not callable(test_solution):
            grading_logger.error(f"'test_solution' function not found in {test_case_module_name}")
        
        # Run the tests
        passed, not_passed = test_solution(solution_function)

        if len(passed) + len(not_passed) == 0:
            grading_logger.error(f"No Test Cases were Run!")
        else:
            grading_logger.info(f"Test Cases Passed {len(passed)}, Out of {len(not_passed) + len(passed)}")

        score = (len(passed) / (len(passed) + len(not_passed))) * 100
        
    except ModuleNotFoundError as e:
        grading_logger.error(f"Error: Module not found - {e}")
        return 0, []
    except AttributeError as e:
        grading_logger.error(f"Error: {e}")
        return 0, []
    except ValueError as e:
        grading_logger.error(f"Error: {e}")
        return 0, []
    except Exception as e:
        grading_logger.error(f"Unexpected error: {e}")
        return 0, []
   
    return score, not_passed

if __name__ == '__main__':
    dynamic_import_and_test(1, 1, 'AssignmentID', 'Test Cases')