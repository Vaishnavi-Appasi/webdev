from pytube import YouTube
from youtube_transcript_api import YouTubeTranscriptApi as yta
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer
from flask import Flask, render_template, request

app = Flask(__name__)

# Load model and tokenizer
MODEL_NAME = "t5-small"  # Consider using a smaller model for faster processing
model = AutoModelForSeq2SeqLM.from_pretrained(MODEL_NAME)
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)

def summarize(transcript, button_value):
    if button_value == 'transcript':
        return render_template('transcript.html', transcript=transcript)
    elif button_value == 'summary':
        input_text = tokenizer.encode(transcript, return_tensors='pt', truncation=True, max_length=512)
        summary_ids = model.generate(input_ids=input_text, max_length=150, num_beams=2, early_stopping=True)
        summary = tokenizer.decode(summary_ids[0], skip_special_tokens=True)
        return render_template('summary.html', summary=summary)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        link = request.form.get('link')
        button_value = request.form.get('button')
        yt = YouTube(link)
        video_id = yt.video_id
        try:
            transcript_data = yta.get_transcript(video_id)
            transcript = " ".join([entry['text'] for entry in transcript_data])
        except Exception as e:
            transcript = "Your connection may be slow or this video does not have a transcript"
        
        return summarize(transcript, button_value)

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=False)  # Set debug=False for production
