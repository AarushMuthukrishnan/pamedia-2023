from flask import Flask, render_template, request
import spacy
import pytextrank
import speech_recognition as sr

app = Flask(__name__)

r = sr.Recognizer()
nlp = spacy.load("en_core_web_lg")
nlp.add_pipe("textrank")

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/listen", methods=["GET", "POST"])
def listen_and_summarize():
    if request.method == "POST":
        with sr.Microphone() as source:
            audio = r.listen(source)

            try:
                text = r.recognize_google(audio)
                doc = nlp(text)

                summary = [i for i in doc._.textrank.summary(limit_sentences=2)]
                return render_template("result.html", summary=summary)
            except:
                return "Sorry, could not recognize your voice."
    return "Error in processing the request."

if __name__ == "__main__":
    app.run(debug=True)
