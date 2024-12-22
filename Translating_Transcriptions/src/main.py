import streamlit as st
import os
import json
import webvtt
from models.generation import ChatBot

def request_subtitle(to_lang):
    # Request Translation
    ...

def preprocess_video(video_path):
    st.info(f"Preprocessing video at: {video_path}")
    # Video2Audio
    # Transcribe in English
    # Make Vector Database or Append to Vector Database
    # Quiz Generation
    ...

# Function to initialize session state variables
def initialize_session_state():
    if 'student_name' not in st.session_state:
        st.session_state.student_name = None
    if 'selected_category' not in st.session_state:
        st.session_state.selected_category = None
    if 'selected_lecture' not in st.session_state:
        st.session_state.selected_lecture = None
    if 'quiz_started' not in st.session_state:
        st.session_state.quiz_started = False
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []
    if 'current_video_time' not in st.session_state:
        st.session_state.current_video_time = 0

initialize_session_state()

def sign_in():
    st.title("Student Sign-In")
    name = st.text_input("Please enter your name:")

    if st.button("Sign In"):
        if name:
            st.session_state.student_name = name
            st.success(f"Signed in as {name}")
        else:
            st.error("Name cannot be empty!")

def list_categories(base_path=os.path.join('src','data','raw')):
    try:
        categories = [name for name in os.listdir(base_path) if os.path.isdir(os.path.join(base_path, name))]
    except Exception as e:
        st.error(f"Error accessing categories: {e}")
        categories = []
    return categories

def show_dashboard():
    st.title("Dashboard")
    st.subheader("Select a Category")

    categories = list_categories()

    if categories:
        selected_category = st.selectbox("Categories", categories)
        if st.button("Open"):
            st.session_state.selected_category = selected_category
            st.rerun()
    else:
        st.warning("No categories found")

def list_lectures(category_path):
    try:
        lectures = [name for name in os.listdir(category_path) if os.path.isdir(os.path.join(category_path, name))]
    except Exception as e:
        st.error(f"Error accessing lectures: {e}")
        lectures = []
    return lectures

def show_lectures():
    category_path = os.path.join('src','data','raw', st.session_state.selected_category)
    lectures = list_lectures(category_path)

    st.title(f"Lectures in {st.session_state.selected_category}")
    if lectures:
        selected_lecture = st.selectbox("Lectures", lectures)
        if st.button("Open Lecture"):
            st.session_state.selected_lecture = selected_lecture
            st.rerun()
    else:
        st.warning("No lectures found")

def list_subtitles(subtitles_path):
    try:
        subtitles = [name for name in os.listdir(subtitles_path) if name.endswith('.vtt')]
    except Exception as e:
        st.error(f"Error accessing subtitles: {e}")
        subtitles = []
    return subtitles

def parse_vtt_to_dict(vtt_file_path):
    subtitles = []
    for caption in webvtt.read(vtt_file_path):
        start_secs = sum(x * int(float(t)) for x, t in zip([3600, 60, 1], caption.start.split(":")))
        end_secs = sum(x * int(float(t)) for x, t in zip([3600, 60, 1], caption.end.split(":")))
        subtitles.append({
            "start_secs": start_secs,
            "end_secs": end_secs,
            "text": caption.text
        })
    return subtitles

def display_dynamic_subtitles(subtitles):
    current_time = st.session_state.get('current_video_time', 0)
    for subtitle in subtitles:
        if subtitle['start_secs'] <= current_time <= subtitle['end_secs']:
            st.text(f"Subtitle: {subtitle['text']}")
            break

def show_lecture_page():
    st.title(f"Lecture: {st.session_state.selected_lecture}")
    category_path = os.path.join('src','data', 'raw', st.session_state.selected_category)
    lecture_path = os.path.join(category_path, st.session_state.selected_lecture)
    video_path = os.path.join(lecture_path, 'video', 'video.mp4')
    subtitles_path = os.path.join(lecture_path, 'subtitles')
    
    # Video and Subtitles Section
    if not os.path.exists(video_path):
        st.error("Video file not found.")
    else:
        st.video(video_path)
    
    subtitles = list_subtitles(subtitles_path)
    subtitle_choice = st.radio("Select Subtitle:", ['None'] + subtitles)
    if subtitle_choice != 'None':
        selected_subtitle_path = os.path.join(subtitles_path, subtitle_choice)
        parsed_subtitles = parse_vtt_to_dict(selected_subtitle_path)
       
        # Create a scrollable text area with all subtitles
        subtitle_text = "\n".join([f"[{subtitle['start_secs']}s - {subtitle['end_secs']}s] {subtitle['text']}" for subtitle in parsed_subtitles])
        st.text_area("Subtitles", value=subtitle_text, height=300)
    
    # Subtitle Request Section
    language = st.text_input("Enter desired language for subtitle request:")
    if st.button("Request Subtitle"):
        request_subtitle(language)
    
    # Chatbot Interface Section
    st.subheader("AI Lecture Assistant")
    
    # Initialize chatbot if not already initialized
    if 'chatbot' not in st.session_state:
        try:
            st.session_state.chatbot = ChatBot(
                model_name=None, 
                subject=st.session_state.selected_category, 
                topic=st.session_state.selected_lecture, 
                limit=10000, 
                online=True
            )
            r = st.session_state.chatbot.start(student_name=st.session_state.student_name)
            if 'chat_history' not in st.session_state:
                st.session_state.chat_history = [text for text in st.session_state.chatbot.history]
        except Exception as e:
            st.error(f"Failed to initialize chatbot: {e}")
            return
    
    # Display chat history
    chat_container = st.container()
    with chat_container:
        for sender, message in st.session_state.chat_history:
            if sender == "You":
                st.chat_message("user").write(message)
            else:
                st.chat_message("assistant").write(message)
    
    # Chat input
    user_input = st.chat_input("Ask a question about the lecture")
    
    # Process user input
    if user_input:
        try:
            # Add user message to chat history
            st.session_state.chat_history.append(("You", user_input))
            
            # Generate AI response using the custom chatbot
            ai_response = st.session_state.chatbot.ask(user_input, st.session_state.student_name)
            st.session_state.chat_history.append(("AI", ai_response))
            
            # Rerun to update the chat interface
            st.rerun()
        except Exception as e:
            st.error(f"Sorry, I couldn't process that query: {str(e)}")
    
    # Quiz Section
    if st.button("Start Quiz"):
        st.session_state.quiz_started = True
        st.rerun()


def load_quiz_questions(quiz_file='quiz.json'):
    """
    Load quiz questions from a JSON file.
    
    Args:
        quiz_file (str, optional): Name of the quiz file. Defaults to 'quiz.json'.
    
    Returns:
        list: List of quiz questions or an empty list if loading fails.
    """
    # Construct the full path to the quiz file
    quiz_path = os.path.join(
        "src", 
        "data", 
        "raw", 
        st.session_state.selected_category, 
        st.session_state.selected_lecture, 
        quiz_file
    )
    
    # Check if the file exists
    if not os.path.exists(quiz_path):
        st.error("Quiz file not found.")
        return []
    
    # Attempt to load and parse the JSON file
    try:
        with open(quiz_path, 'r') as file:
            questions = json.load(file)
        return questions
    except json.JSONDecodeError as e:
        st.error(f"Error loading quiz questions: {e}")
        return []

def evaluate_quiz_response(questions, responses):
    """
    Evaluate the user's quiz responses and calculate the score.
    
    Args:
        questions (list): List of quiz questions.
        responses (list): List of user's selected responses.
    
    Returns:
        int: Total score achieved by the user.
    """
    score = 0
    for i, response in enumerate(responses):
        question = questions[i]
        # Check if the selected choice is correct by comparing its index with the answer index
        if question['choices'].index(response) + 1 == question['answer']:
            score += 1
    return score

def show_quiz():
    """
    Display the quiz interface in Streamlit.
    Loads questions, presents them to the user, and shows the final score.
    """
    # Load quiz questions
    questions = load_quiz_questions()
    
    if not questions:
        st.warning("No questions found. Unable to start the quiz.")
        return
    
    # Set up the quiz interface
    st.title("Quiz")
    
    # Initialize a list to store user responses
    responses = []
    
    # Display each question
    for i, question in enumerate(questions):
        st.subheader(f"Question {i + 1}: {question['question']}")
        
        # Create a radio button group for answer choices
        choice = st.radio(
            "Options", 
            question['choices'], 
            key=f"question_{i}"
        )
        
        # Store the selected response
        responses.append(choice)
    
    # Add a button to submit the quiz
    if st.button("Finish Quiz"):
        # Evaluate the quiz and calculate the score
        score = evaluate_quiz_response(questions, responses)
        
        # Display the result
        st.success(f"You scored {score} out of {len(questions)}")
        
        # Reset session state variables
        st.session_state.quiz_started = False
        st.session_state.selected_lecture = None


def upload_lecture():
    st.sidebar.title("Upload Lecture")

    category = st.sidebar.text_input("Category Name")
    lecture_name = st.sidebar.text_input("Lecture Topic Name")
    video_file = st.sidebar.file_uploader("Upload Video File (mp4)", type=["mp4"])

    if st.sidebar.button("Upload"):
        if category and lecture_name and video_file:
            category_path = os.path.join('data', 'raw', category)

            # Create directories if they do not exist
            if not os.path.exists(category_path):
                os.makedirs(category_path)

            lecture_path = os.path.join(category_path, lecture_name)
            if not os.path.exists(lecture_path):
                os.makedirs(lecture_path)

            # Save video file
            video_folder = os.path.join(lecture_path, 'video')
            os.makedirs(video_folder, exist_ok=True)
            video_path = os.path.join(video_folder, 'video.mp4')
            with open(video_path, "wb") as f:
                f.write(video_file.getbuffer())

            st.sidebar.success("Lecture successfully uploaded!")
            
            # Call the preprocess_video function
            preprocess_video(video_path)

            # Possibly refresh the page to reflect the new lecture
            st.rerun()
        else:
            st.sidebar.error("Please fill in all fields and upload a video.")

# def show_chatbot(student_name, subject, lecture):
#     """
#     Streamlit chatbot interface integrated with the custom ChatBot
    
#     Args:
#         lecture_path (str): Path to the current lecture
#         student_name (str): Name of the current student
#     """
#     st.sidebar.title("AI Lecture Assistant")

#     # Initialize chatbot if not already initialized
#     if 'chatbot' not in st.session_state:
#         try:
#             # Use a default model or allow model selection
#             st.session_state.chatbot = ChatBot(model_name=None, subject=subject, topic=lecture, limit=10000, online=True)
#             r = st.session_state.chatbot.start(student_name=student_name)
#             if 'chat_history' not in st.session_state:
#                 st.session_state.chat_history = [text for text in st.session_state.chatbot.history]
#                 st.rerun()
#         except Exception as e:
#             st.sidebar.error(f"Failed to initialize chatbot: {e}")
#             return


#     # Chatbot interface
#     user_input = st.sidebar.text_input("Ask a question about the lecture:", key="chat_input")
#     # Display chat history in the sidebar
#     for sender, message in st.session_state.chat_history:
#         st.sidebar.write(f"{sender}: {message}")


#     if st.sidebar.button("Send"):
#         if user_input.strip():
#             try:
#                 # Add user message to chat history
#                 st.session_state.chat_history.append(("You", user_input))
                
#                 # Generate AI response using the custom chatbot
#                 ai_response = st.session_state.chatbot.ask(user_input, student_name)
#                 st.session_state.chat_history.append(("AI", ai_response))
#             except Exception as e:
#                 st.session_state.chat_history.append(("AI", f"Sorry, I couldn't process that query: {str(e)}"))
            
#             st.rerun()
# Modify main function to pass student name
def main():

    if st.session_state.student_name is None:
        sign_in()
    else:
        upload_lecture()  # Ensure the upload section is available on every page
        if st.session_state.quiz_started:
            show_quiz()
        elif st.session_state.selected_category is None:
            show_dashboard()
        elif st.session_state.selected_lecture is None:
            show_lectures()
        else:
            # lecture_path = os.path.join('src','data', 'raw', st.session_state.selected_category, st.session_state.selected_lecture)
            show_lecture_page()
            #show_chatbot(st.session_state.student_name, st.session_state.selected_category, st.session_state.selected_lecture)

if __name__ == "__main__":
    main()