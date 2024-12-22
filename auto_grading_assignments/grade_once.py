import sys
import json
import os
import pathlib
from backend.api.chatgpt_api import HomeworkGrader
from database.DataBase import Connect_DB
from backend.api.mail import send_feedback, extract_marks_and_feedback
from backend.directory.getinput import GetInputs
from backend.directory.run_test_cases import concatenate_and_run_tests

from backend.logger_config import setup_logger

# Create a logger for grading
grading_logger = setup_logger()
def grade_once(student_email, assignment_folder):
    grading_logger.info("Starting grading process")
    
    # Config files
    try:
        config_path = os.path.join('Keys', 'autograder_config.json')
        with open(config_path) as file:
            config = json.load(file)
            if config is None:
                grading_logger.error("AutoGrader not configured")
                sys.exit("AutoGrader Not Configured")
            from_email_address = config['email']
            password = config['password']
            smtp_address = config['smtp']
    except Exception as e:
        grading_logger.error(f"Failed to load email configuration: {e}")
        sys.exit(1)

    # Assignment Directory
    try:
        assignment_directory = os.path.join('Input', assignment_folder)
        config_path = os.path.join(assignment_directory, 'config.json')
        with open(config_path) as file:
            config = json.load(file)
            if config is None:
                grading_logger.error("No Config File For Assignment Directory")
                sys.exit("No Config File For Assignment Directory")
            assignment_topic = config['assignment_topic']
            total_score = int(config['total_score'])
            subject_name = config['subject_name']
            batch_number = int(config['batch_number'])
    except Exception as e:
        grading_logger.error(f"Failed to load assignment configuration: {e}")
        sys.exit(1)

    # Connect with database
    try:
        db_path = os.path.join('database', 'data.db')
        db = Connect_DB(db_path)

        assignment_id = db.get_assignment_id(assignment_topic=assignment_topic, subject_name=subject_name, batch_number=batch_number)
        student_id = db.get_intern_id(email=student_email)
    except Exception as e:
        grading_logger.error(f"Database connection or query failed: {e}")
        sys.exit(1)

    # Taking Input
    try:
        questions = GetInputs(dir=assignment_directory).questions
    except Exception as e:
        grading_logger.error(f"Error getting questions: {e}")
        sys.exit(1)

    try:
        solutions = GetInputs.for_student(assignment_directory, int(student_id))
    except Exception as e:
        grading_logger.error(f"Error getting solutions: {e}")
        sys.exit(1)

    # Grading
    try:
        with open(pathlib.Path('Keys', 'key.txt')) as file:
            token = file.readline().strip()
        with open(pathlib.Path('Keys', 'autograder_config.json')) as file:
            config = json.load(file)
        endpoint = config['endpoint']
        model_name = config['model_name']
    except Exception as e:
        grading_logger.error(f"Failed to load grading API configuration: {e}")
        sys.exit(1)

    output_tokens = 1200
    autograder = HomeworkGrader(token, endpoint, model_name, output_tokens)

    grades = 0
    feedback_final = ''
    per_score = 0

    for question_id in questions:
        question_score = 100
        per_score += question_score
        question = questions[question_id]
        solution = solutions[question_id]
        
        feedback = f'\nFEEDBACK FOR QUESTION:\n{question}\n'
        
        try:
            test_score, not_passed = concatenate_and_run_tests(solution_file=question_id, intern_id=student_id, assignment=assignment_folder, test_case_folder='Test Cases')
            print(test_score, not_passed)
            if not_passed:
                solution += f'\n\n Test Score:{test_score}\n\n'
                for tc in not_passed:
                    solution += tc
            else:
                solution += f"\n\nALL TEST CASES PASSED FOR THE GIVEN QUESTION\n\n TEST SCORE: {test_score}\n\n"

            feedback += f"ANSWER:\n\n{solution}"
            response = autograder.grade_answer(question, solution, question_score)
            result = extract_marks_and_feedback(response)
            grade = (int(result[0]) + int(test_score)) / 2
            
            feedback += result[1]
            grades += grade

            feedback_final += feedback + '\n- - - - - - - - - - - - - - - - - - - - - - - - - - - - - -\n'
            grading_logger.info(f"Graded question {question_id}: score {grade}")
        except Exception as e:
            grading_logger.error(f"Error grading question {question_id}: {e}")

    # Storing Grades in Database
    try:
        factor = total_score / per_score
        grades *= factor
        db.insert_into_grades(grades, intern_id=student_id, assignment_id=assignment_id)
        grading_logger.info(f"Stored grade: {grades} for student ID {student_id}")
    except Exception as e:
        grading_logger.error(f"Failed to store grades in the database: {e}")
    finally:
        db.close_connection()

    # Send Feedback
    try:
        subject = f'Assessment Feedback For Assignment {assignment_topic}.'
        send_feedback(smtp_address=smtp_address, to_email=student_email, subject=subject, feedback_message=feedback_final,
                      from_email=from_email_address, from_password=password)
        grading_logger.info(f"Feedback sent to {student_email}")
    except Exception as e:
        grading_logger.error(f"Failed to send feedback: {e}")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        grading_logger.error('Please Provide Assignment_Folder_Name and Student_Email as console arguments.')
        sys.exit('Please Provide Assignment_Folder_Name and Student_Email as console arguments.')
    
    grading_logger.info(f'Grade Once For {sys.argv[1]}, {sys.argv[2]}')
    
    assignment_folder = sys.argv[1]
    student_email = sys.argv[2]
    grade_once(student_email, assignment_folder)