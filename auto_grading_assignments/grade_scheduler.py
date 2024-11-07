import sys
import json
import datetime
import heapq
import pathlib
import os

from backend.logger_config import setup_logger

# Create a logger for grading
grading_logger = setup_logger()

class GradeScheduler:
    """
    Schedules Requests for Grading Assignments as per request limits and requests left for API
    """
    def __init__(self, file_path=pathlib.Path('Keys', 'grading_schedules.json')):
        grading_logger.info('Initializing GradeScheduler.')
        grading_logger.info('Loading grading request queue from json.')

        if not os.path.exists(file_path):
            grading_logger.info(f"{file_path} not found. Creating a new file.")
            with open(file_path, 'w') as file:
                json.dump({}, file)

        try:
            with open(file_path) as file:
                self.data = json.load(file)
        except json.JSONDecodeError as e:
            grading_logger.error(f"Error decoding JSON from {file_path}: {e}")
            self.data = {}

        self.priority_queue = []
        self.make_priority_queue()

        try:
            with open(pathlib.Path('Keys', 'autograder_config.json')) as file:
                config = json.load(file)
        except FileNotFoundError:
            grading_logger.error("Config file not found. Please make sure autograder_config.json exists.")
            exit()
        except json.JSONDecodeError as e:
            grading_logger.error(f"Error decoding JSON from autograder_config.json: {e}")
            exit()

        if config['last_used'] != str(datetime.datetime.now().date()):
            config['requests_left'] = config['requests_limit']
            config['last_used'] = str(datetime.datetime.now().date())
            with open(pathlib.Path('Keys', 'autograder_config.json'), 'w') as config_file:
                json.dump(config, config_file, indent=4)
        
        self.requests_left = config['requests_left']
        grading_logger.info(f"Requests left initialized to {self.requests_left}.")

        self.start()

    def make_priority_queue(self):
        for assignment_folder, students in self.data.items():
            for student_email, question_numbers in students.items():
                heapq.heappush(self.priority_queue, (int(question_numbers), assignment_folder, student_email))
        grading_logger.debug(f"Priority queue created with {len(self.priority_queue)} items.")

    def start(self):
        done = []  # tuples ("Assignment_Folder", "Student_email")
        grading_logger.info("Starting grading process.")
        
        while self.priority_queue:
            req = self.pop_min_request()
            if req is None:  # Check if there's an issue with the request
                grading_logger.warning("No valid request to process.")
                break
            
            if req[0] > self.requests_left:
                self.add_to_queue(assignment_folder=req[1], student_email=req[2])
                grading_logger.warning(f"Grading stopped due to insufficient requests left: {self.requests_left}.")
                break
            else:
                self.requests_left -= int(req[0])
                grading_logger.info(f"Grading {req[1]} for {req[2]} with {req[0]} requests.")
                os.system(f'python grade_once.py {req[1]} {req[2]}')
                done.append((req[1], req[2]))

        self.stop(done)

    def add_to_queue(self, student_email, assignment_folder):
        question_numbers = self.how_many_requests_for(assignment_folder)
        if assignment_folder in self.data:
            if student_email in self.data[assignment_folder]:
                grading_logger.debug(f"Resuming grading for {assignment_folder} {student_email}.")
                self.start()
            else:
                self.data[assignment_folder][student_email] = question_numbers
                heapq.heappush(self.priority_queue, (question_numbers, assignment_folder, student_email))
                grading_logger.debug(f"Added to queue: {assignment_folder} {student_email}.")
                self.start()
        else:
            self.data[assignment_folder] = {student_email: question_numbers}
            heapq.heappush(self.priority_queue, (question_numbers, assignment_folder, student_email))
            grading_logger.debug(f"New Assignment task added to queue: {assignment_folder} {student_email}.")
            self.start()

    def stop(self, done):
        grading_logger.info("Stopping Grader!!")
        for assignment_folder, student_email in done:
            del self.data[assignment_folder][student_email]
        with open(pathlib.Path('Keys', 'grading_schedules.json'), "w") as file:
            json.dump(self.data, file, indent=4)
        with open(pathlib.Path('Keys', 'autograder_config.json')) as file:
            config = json.load(file)
            config['requests_left'] = self.requests_left
            with open(pathlib.Path('Keys', 'autograder_config.json'), "w") as file:
                json.dump(config, file, indent=4)
        grading_logger.info(f"Grading stopped! Assignments remaining in queue: {len(self.priority_queue)}.")

    def pop_min_request(self):
        if self.priority_queue:
            return heapq.heappop(self.priority_queue)
        else:
            grading_logger.error("Attempted to pop from an empty priority queue.")
            return None

    @staticmethod
    def how_many_requests_for(folder):
        with open(pathlib.Path('Input', folder, 'config.json')) as file:
            requests = int(json.load(file)['n'])
            grading_logger.debug(f"Requests needed for {folder}: {requests}")
            return requests

if __name__ == '__main__':
    if len(sys.argv) == 3:
        scheduler = GradeScheduler()
        scheduler.add_to_queue(assignment_folder=sys.argv[1], student_email=sys.argv[2])
    else:
        grading_logger.error("Invalid arguments. Usage: python grade_scheduler.py <assignment_folder> <student_email>")