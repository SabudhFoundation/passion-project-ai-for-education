from gpt4all import GPT4All
import re, math
import json
from collections import deque
from .embedder import make_a_rag
import os
import time
from openai import OpenAI

class AIbot:
    def __init__(self, system_prompt, model):
        with open(os.path.join("keys", "bot-token.txt")) as file:
            token = file.readlines()[0].strip()
        self.endpoint = "https://models.inference.ai.azure.com"
        self.model_name = model
        self.system_prompt = system_prompt

        self.client = OpenAI(
            base_url=self.endpoint,
            api_key=token,
        )

    def generate(self, prompt, output_tokens):
        response = self.client.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": f"{self.system_prompt}",
            },
            {
                "role": "user",
                "content": prompt,
            }
        ],
        temperature=0.5,
        top_p=1.0,
        max_tokens=output_tokens,
        model=self.model_name
        )
        time.sleep(5)

        return response.choices[0].message.content




class ChatBot:
    def __init__(self, model_name, subject, topic, limit, online=False):
        """
        Initialize the chatbot model.

        Args:
            model_name (str): The name of the model to use.
            limit (int): The character limit for the conversation history.
        """
        if online:
            system_prompt = (f"You are a helpful mentor who is teaching a student the concepts of {topic} and {subject}."
            "When student asks a question. Teach him in simple and easily understoofd language, at last, also list key points discussed and termonolgy used and their definitions")
            self.model = AIbot(system_prompt=system_prompt, model="gpt-4o-mini")
        else:
            self.model = GPT4All(model_name, device="cpu")  # Assumes a predefined model class.
        self.online = online
        self.history = deque()  # Use deque for efficient history management.
        self.limit = limit  # Maximum allowed history size in characters.
        self.history_size = 0  # Current size of the conversation history.
        self.topic = topic
        self.subject = subject
        self.rag = make_a_rag(subject, topic)

    def _update_history(self, text, agent=True, student_name=None):
        """
        Add a message to the conversation history and maintain the size limit.

        Args:
            text (str): The message to add.
            agent (bool): Whether the message is from the chatbot (True) or the student (False).
            student_name (str): The name of the student (used if `agent` is False).
        """
        # Format message based on the sender.
        if agent:
            message = f"Chatbot: {text}"
        else:
            message = f"{student_name}: {text}"

        # Add the message to history and update the size.
        self.history.append(message)
        self.history_size += len(message)

        # Remove the oldest messages if history exceeds the limit.
        while self.history_size > self.limit:
            removed_message = self.history.popleft()
            self.history_size -= len(removed_message)

    def _construct_prompt(self, text):
        """
        Construct the full prompt for the model.

        Args:
            text (str): The latest query or message from the user.

        Returns:
            str: The complete prompt including the history.
        """
        # Combine history and current text into a single prompt.
        return " ".join(self.history) + " " + text

    def start(self, student_name):
        """
        Start the conversation by introducing the topic and subject.

        Args:
            student_name (str): The student's name.
            topic (str): The topic to revise.
            subject (str): The subject of the topic.

        Returns:
            str: The chatbot's response.
        """
        initial_message = (
            f"Hello! My name is {student_name}. Please help me revise the topic '{self.topic}' in the subject '{self.subject}'. I will give you context along with queries and you answer."
        )
        self._update_history(initial_message, agent=False, student_name=student_name)
        return self.generate(initial_message, agent=False, student_name=student_name)
    
    def generate(self, text, agent=True, student_name=None):
        """
        Generate a response from the model based on the provided text and context.

        Args:
            text (str): The latest query or message.
            agent (bool): Whether the message is from the chatbot (True) or the student (False).
            student_name (str): The name of the student (used if `agent` is False).

        Returns:
            str: The generated response from the model.
        """
        try:
            # Construct the full prompt and get the response.
            prompt = self._construct_prompt(text)
            if self.online:
                response = self.model.generate(prompt, 2048)
            else: 
                with self.model.chat_session():
                    response = self.model.generate(prompt, max_tokens=512)
                # Add the response to the history.
                self._update_history(response, agent=agent, student_name=student_name)
            print(response)
            return response
        except Exception as e:
            # Handle errors gracefully and return an error message.
            return f"An error occurred while generating a response: {e}"

    def ask(self, text, student_name):
        """
        Ask the chatbot a question.

        Args:
            text (str): The student's query or input.
            student_name (str): The name of the student.

        Returns:
            str: The chatbot's response.
        """
        self._update_history(text, False, student_name)
        rag_retrieved = self.rag.advanced_retrieval(text)
        context = f"Context: {" ".join(t['chunk'] for t in rag_retrieved)}"
        return self.generate(context+"/n"+text, agent=False, student_name=student_name)


class QuizGenerator:
    def __init__(self):
        """
        Initialize QuizGenerator with AIbot.
        """
        system_prompt = "You are a quiz generator that will take context and generate Multiple Choice Questions in the given format."
        self.model = AIbot(system_prompt=system_prompt, model="gpt-4o-mini")
        self.questions = []

    def generate_quiz_question(self, chunk):
        """
        Generate a multiple-choice question from a given text chunk.

        Args:
            chunk (str): The text chunk to base the question on.

        Returns:
            dict: A dictionary containing the question, choices, and the correct answer.
        """
        # Improved prompt for question generation
        prompt = (
            f"Generate a multiple-choice question from the following text:\n"
            f"\"\"\"\n{chunk}\n\"\"\"\n\n"
            f"The question should be based on a key concept discussed in the text.\n"
            f"Format your response as follows:\n"
            f"QUESTION: <Write the question here>\n"
            f"CHOICES: <Provide 4 options>\n"
            f"ANSWER: <Provide the correct option number (1, 2, 3, or 4)>\n\n"
            f"Example:\n"
            f"QUESTION: What does Newton's first law state?\n"
            f"CHOICES:\n"
            f"1. An object will remain in rest unless acted upon by an external force.\n"
            f"2. Energy cannot be created or destroyed.\n"
            f"3. The acceleration of an object is proportional to the net force applied.\n"
            f"4. Every action has an equal and opposite reaction.\n"
            f"ANSWER: 1"
        )

        if self.questions:
            prompt += "\n The question generated should be different from the following questions.\n"
        for question in self.questions:
            prompt += f"\n{question}"

        # Generate the response using AIbot
        quiz = self.model.generate(prompt, output_tokens=512)

        # Parse the output
        question_match = re.search(r"QUESTION:\s*(.+)", quiz, re.IGNORECASE)
        choices_match = re.findall(r"\d\.\s*(.+)", quiz, re.IGNORECASE)
        answer_match = re.search(r"ANSWER:\s*(\d+)", quiz, re.IGNORECASE)

        # Extract components with validation
        question = question_match.group(1).strip() if question_match else "No question generated"
        choices = [choice.strip() for choice in choices_match] if choices_match else []
        answer = int(answer_match.group(1)) if answer_match else None

        # Validate completeness
        if not question or len(choices) != 4 or answer not in range(1, 5):
            return {"error": "Incomplete or invalid quiz generated"}

        # Append valid question to history
        self.questions.append(question)

        return {
            "question": question,
            "choices": choices,
            "answer": answer,
        }

    def make_n_questions(self, n, text_path, output_path):
        """
        Generate N questions from a text file and save to a JSON file.

        Args:
            n (int): Number of questions to generate.
            text_path (str): Path to the input text file.
            output_path (str): Path to the output JSON file.

        Returns:
            list: List of generated questions.
        """
        # Load text from file
        print("Text Reading")
        try:
            with open(text_path, 'r') as file:
                print("Text Read")
                full_text = file.read()
                print(full_text[:10])
        except Exception as e:
            return {"error": f"Failed to load text file: {str(e)}"}

        # Calculate chunk size
        total_length = len(full_text)
        chunk_size = math.ceil(total_length / n)
        
        # Split text into chunks
        chunks = [full_text[i:i + chunk_size] for i in range(0, total_length, chunk_size)]

        # Generate quiz for each chunk
        quizzes = []
        for i, chunk in enumerate(chunks[:n]):
            quiz = self.generate_quiz_question(chunk)
            print(quiz)
            if "error" in quiz:
                print(f"Error in generating question {i+1}: {quiz['error']}")
            else:
                quizzes.append(quiz)
        
        # Save quizzes to JSON file
        try:
            with open(output_path, 'w', encoding='utf-8') as json_file:
                json.dump(quizzes, json_file, indent=4, ensure_ascii=False)
            print(f"Quizzes successfully saved to {output_path}")
        except Exception as e:
            return {"error": f"Failed to save quizzes to file: {str(e)}"}
        
        return quizzes

        

def generate_quiz(subject="Natural Language Processing", topic="Vectorization"):
    bot = QuizGenerator()
    text_path = os.path.join("src", "data", "raw", subject, topic, "transcription_text.txt")
    output_path = os.path.join("src", "data", "raw", subject, topic, "quiz.json")
    print(bot.make_n_questions(n=10, text_path=text_path, output_path=output_path))
    
if __name__ == "__main__":
    #bot = ChatBot("Meta-Llama-3-8B-Instruct.Q4_0.gguf", "Natural Language Processing", "Vectorization", 10000)
    # bot = ChatBot(model_name=None, subject="Natural Language Processing", topic="Vectorization", limit=10000, online=True)
    # bot.start("Sumit")
    # while True:
    #     query = input("User: ")
    #     bot.ask(query, "Sumit")
    generate_quiz()


