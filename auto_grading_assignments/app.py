import os
import json
import pathlib
import logging
from flask import Flask, render_template, session, request, redirect, flash, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, EmailField, SubmitField
from wtforms.validators import DataRequired, Email
from werkzeug.utils import secure_filename
from database.DataBase import Connect_DB
import add_assignment
import re

# Configure logging
logging.basicConfig(filename='teachers.log',level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

app_logger = logging.getLogger('app_logger')
app_handler = logging.FileHandler('app.log')
app_handler.setLevel(logging.INFO)
app_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
app_handler.setFormatter(app_formatter)
app_logger.addHandler(app_handler)
app_logger.propagate = False

# Flask Forms
class StudentLoginForm(FlaskForm):
    student_name = StringField('Student Name', validators=[DataRequired()])
    student_email = EmailField('Student Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Login')

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Replace with a strong secret key

# Silence Flask's built-in logging
log_handler = logging.getLogger('werkzeug')  # Get the werkzeug logger
log_handler.setLevel(logging.ERROR)         # Adjust the level you want to log

@app.before_request
def log_request_info():
    app_logger.info('Request Path: %s, Method: %s, Args: %s, User: %s', 
                    request.path, request.method, request.args,
                    session.get('student_email'))

@app.route('/')
def welcome():
    app_logger.info("Accessed welcome page.")
    return render_template('welcome.html')


@app.route('/teacher_login')
def teacher_login():
    try:
        app_logger.info("Accessed teacher login page.")
        return render_template('teacher_login.html')
    except Exception as e:
        app_logger.error(f"Error accessing teacher login page: {e}")
        return "An error occurred", 500


@app.route('/teacher_dashboard', methods=['GET', 'POST'])
def teacher_dashboard():
    if request.method == 'POST':
        app_logger.info("Teacher dashboard accessed with POST method.")
    else:
        app_logger.info("Teacher dashboard accessed with GET method.")
    
    flash("Welcome to the Teacher Dashboard!", "info")
    return render_template('teacher_dashboard.html')


def create_assignment_folder(assignment_name):
    """Helper function to create an assignment folder and log the operation."""
    assignment_folder = f"Input/{assignment_name.replace(' ', '_')}"
    try:
        os.makedirs(f"{assignment_folder}/Questions", exist_ok=True)
        app_logger.info("Successfully created folder structure for assignment: %s", assignment_folder)
        return assignment_folder
    except Exception as e:
        app_logger.error("Failed to create folder for assignment '%s'. Error: %s", assignment_name, e)
        raise

def write_config_file(assignment_folder, config):
    """Helper function to write the config file and log the operation."""
    config_file_path=f"{assignment_folder}/config.json"
    try:
        with open(config_file_path, 'w') as config_file:
            json.dump(config, config_file, indent=4)
        app_logger.info("Successfully created configuration file for assignment '%s'.", config.get("assignment_topic", "Unknown"))
    except Exception as e:
        app_logger.error("Failed to write config file for assignment '%s'. Error: %s", config.get("assignment_topic", "Unknown"), str(e))
        raise

@app.route('/create_assignment', methods=['GET', 'POST'])
def create_assignment():
    if request.method == 'POST':
        app_logger.debug("Received POST request to create assignment with form data: %s", request.form)

        assignment_name = request.form['assignment_name']
        subject = request.form['subject']
        total_marks = request.form['total_marks']
        start_date = request.form['start_date']
        deadline_date = request.form['deadline_date']
        batch_number = request.form.get('batch_number')
        questions = request.form.getlist('questions')

        if not assignment_name or any(not q for q in questions):
            flash("Please fill out all fields.", "danger")
            app_logger.warning("Assignment creation failed for '%s'. Missing fields.", assignment_name)
            return redirect(url_for('create_assignment'))

        try:
            assignment_folder = create_assignment_folder(assignment_name)

            config = {
                "assignment_topic": assignment_name,
                "total_score": total_marks,
                "subject_name": subject,
                "batch_number": batch_number,
                "start_date": start_date,
                "deadline_date": deadline_date,
                "n": len(questions)
            }

            write_config_file(assignment_folder, config)

            for i, question in enumerate(questions, start=1):
                with open(f"{assignment_folder}/Questions/{i}.txt", 'w') as f:
                    f.write(question)
                    app_logger.info("Wrote question #%d for assignment '%s'.", i, assignment_name)

            os.system(f'python add_assignment.py {assignment_name}')
            
            flash("Assignment created successfully!", "success")
            app_logger.info("Assignment '%s' created successfully.", assignment_name)
            return redirect(url_for('edit_test_cases', assignment_name=assignment_name.replace(' ', '_')))
        except Exception as e:
            flash("An error occurred while creating the assignment. Please try again.", "danger")
            app_logger.exception("Error occurred while creating assignment '%s': %s", assignment_name, str(e))
            return redirect(url_for('create_assignment'))

    return render_template('create_assignment.html')

@app.route('/edit_test_cases/<assignment_name>', methods=['GET', 'POST'])
def edit_test_cases(assignment_name):
    assignment_folder = f"Input/{assignment_name}"
    test_cases_path = os.path.join(assignment_folder, "test_cases.json")

    app_logger.debug("Editing test cases for assignment '%s' with folder path '%s'", assignment_name, assignment_folder)

    if request.method == 'POST':
        app_logger.debug("Received POST request to update test cases for assignment '%s'", assignment_name)

        if os.path.exists(test_cases_path):
            try:
                with open(test_cases_path, 'r') as f:
                    test_cases = json.load(f)
                app_logger.info("Loaded existing test cases from '%s' for assignment '%s'.", test_cases_path, assignment_name)
            except Exception as e:
                app_logger.error("Failed to read existing test cases for assignment '%s'. Error: %s", assignment_name, str(e))
                return redirect(url_for('edit_test_cases', assignment_name=assignment_name))
        else:
            test_cases = {}
            app_logger.info("No existing test cases found. Initializing new test cases for assignment '%s'.", assignment_name)

        try:
            new_test_cases = {key.split('_')[2]: re.sub(r'\r\n', r'\n',value) for key, value in request.form.items() if key.startswith('test_case_')}
            app_logger.debug("New test cases to update: %s", new_test_cases)

            test_cases.update(new_test_cases)
            app_logger.info("Updated test cases for assignment '%s'.", assignment_name)

            with open(test_cases_path, 'w') as f:
                json.dump(test_cases, f, indent=4)
            app_logger.info("Successfully wrote updated test cases to '%s' for assignment '%s'.", test_cases_path, assignment_name)
        
            for file_name, test_case in new_test_cases.items():
                add_assignment.write_description(description=test_case, dir=assignment_folder, file_name=file_name, write_json=False)
                app_logger.info("Saved test case description for file '%s' in assignment '%s'.", file_name, assignment_name)

            flash("Test cases updated successfully.", "success")
            app_logger.info("Test cases for assignment '%s' updated.", assignment_name)
            return redirect(url_for('teacher_dashboard'))
        
        except Exception as e:
            app_logger.exception("Error occurred while updating test cases for assignment '%s': %s", assignment_name, str(e))
            return redirect(url_for('edit_test_cases', assignment_name=assignment_name))
        

    test_cases_dict = {}
    if os.path.exists(test_cases_path):
        try:
            with open(test_cases_path, 'r') as f:
                test_cases_dict = json.load(f)
            app_logger.info("Loaded test cases for display in form for assignment '%s'.", assignment_name)
        except Exception as e:
            app_logger.error("Failed to load test cases for display for assignment '%s'. Error: %s", assignment_name, str(e))

    return render_template('edit_test_cases.html', test_cases_dict=test_cases_dict, assignment_name=assignment_name)

@app.route('/student_login', methods=['GET', 'POST'])
def student_login():
    form = StudentLoginForm()
    if form.validate_on_submit():
        student_name = form.student_name.data
        student_email = form.student_email.data
        app_logger.info("Student '%s' logged in.", student_name)
        
        session['student_name'] = student_name
        session['student_email'] = student_email
        flash(f"Welcome, {student_name}!", "success")
        return redirect('/student_dashboard')

    return render_template('student_login.html', form=form)

@app.route('/student_dashboard', methods=['GET', 'POST'])
def student_dashboard():
    assignments = [d for d in os.listdir('Input') if os.path.isdir(os.path.join('Input', d))]
    app_logger.info("Accessed student dashboard. Available assignments: %s", assignments)
    return render_template('student_dashboard.html', assignments=assignments)

@app.route('/view_assignment/<assignment_name>')
def view_assignment(assignment_name):
    questions = []
    assignment_path = os.path.join("Input", assignment_name, "Questions")

    try:
        if os.path.exists(assignment_path):
            question_files = sorted(os.listdir(assignment_path))
            for question_file in question_files:
                with open(os.path.join(assignment_path, question_file)) as f:
                    questions.append(f.read())
        app_logger.info("Viewing assignment '%s'. Number of questions: %d", assignment_name, len(questions))
    except Exception as e:
        app_logger.exception("Error while viewing assignment '%s': %s", assignment_name, e)

    return render_template('view_assignment.html', assignment_name=assignment_name, questions=questions, student_name=session.get('student_name'))

@app.route('/upload_solutions/<assignment_name>', methods=['POST'])
def upload_solutions(assignment_name):
    student_name = session.get('student_name')
    student_email = session.get('student_email')
    
    if not student_name or not student_email:
        flash("Session expired or invalid. Please log in again.", "danger")
        app_logger.warning("Upload failed for assignment '%s'. Invalid session detected.", assignment_name)
        return redirect(url_for('student_login'))

    try:
        db = Connect_DB(pathlib.Path('database', 'data.db'))
        student_id = db.get_intern_id(email=student_email)
        db.close_connection()
    except Exception as e:
        app_logger.error("Error connecting to database: %s", e)
        flash("An error occurred while accessing the database. Please try again.", "danger")
        return redirect(url_for('student_login'))

    student_folder_path = os.path.join('Input', assignment_name, str(student_id))
    os.makedirs(student_folder_path, exist_ok=True)

    for question_number, solution in request.files.items():
        if solution and solution.filename.endswith('.py'):
            question_num = question_number.split('_')[1]
            filename = secure_filename(f"{question_num}.py")
            solution.save(os.path.join(student_folder_path, filename))
            app_logger.info("Uploaded solution for question #%s by student '%s'.", question_num, student_name)

    flash("All solutions uploaded successfully!", "success")
    os.system(f'python grade_scheduler.py {assignment_name} {student_email}')
    app_logger.info("Grading scheduled for assignment '%s' for student '%s'.", assignment_name, student_email)

    return redirect(url_for('view_assignment', assignment_name=assignment_name))

if __name__ == '__main__':
    app_logger.info("Starting Flask app...")
    app.run(debug=True)