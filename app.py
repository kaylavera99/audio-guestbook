from flask import Flask, render_template, request, jsonify
import boto3
import os
import uuid
from datetime import datetime
app = Flask(__name__)

s3 = boto3.client('s3')

BUCKET_NAME = "kayla-audio-guestbook"

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/save", methods=["POST"])
def save():
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    unique_id = uuid.uuid4().hex[:6]
    file = request.files['audio_data']
    filename =  f"guest_message_{timestamp}_{unique_id}.wav"
    local_path = os.path.join(UPLOAD_FOLDER, filename)
    file.save(local_path)


    try:
        s3.upload_file(local_path, BUCKET_NAME, filename)
        s3_url = f"https://{BUCKET_NAME}.s3.amazonaws.com/{filename}"
        return jsonify({"message": "File uploaded successfully", "url": s3_url}), 200
    except Exception as e:
        return jsonify({"error":str(e)}), 500

    


if __name__ == "__main__":
    app.run(debug=True, port = 5000, host="0.0.0.0")
