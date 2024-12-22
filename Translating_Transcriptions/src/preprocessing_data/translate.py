from googletrans import Translator
import time, os, pickle

class Lecture_Translator:
    def __init__(self, from_lang="en", interval=0.5):
        self.translator = Translator()
        self.from_lang = from_lang
        self.interval = interval

    def translate(self, text, to_lang="hi"):
        return self.translator.translate(text, src=self.from_lang, dest=to_lang).text

    def function(self, subtitles, to_lang="hi"):
        for segment in subtitles:
            while:
            segment['text'] = self.translate(segment['text'], to_lang=to_lang)
            time.sleep(self.interval)
        return subtitles

    
if __name__ == "__main__":
    # Load subtitles object
    subject = "NLP"
    lecture_number = 2
    to_lang = "hi"
    subtitles_path = os.path.join("Lectures", subject, f"lecture{lecture_number}", "subtitles-obj.pkl")
    with open(subtitles_path, "rb") as file:
        subtitles = pickle.load(file)
    
    translator = Lecture_Translator()

    subtitles = translator.function(subtitles=subtitles, to_lang=to_lang)

    # Assuming 'subtitles' is your object to be saved
    with open(os.path.join("Lectures", subject, f"lecture{lecture_number}", f"{to_lang}-subtitles-obj.pkl"), "wb") as file:
        pickle.dump(subtitles, file)
