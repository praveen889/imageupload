from flask import Flask, request, jsonify, send_file
import os
from firebase_admin import initialize_app, credentials, storage

app = Flask(__name__)

# Initialize Firebase
cred = credentials.Certificate("serviceAccountKey.json")
firebase_app = initialize_app(cred, {"storageBucket": "upload-image-ecdc0.appspot.com"})

@app.route("/upload", methods=["POST"])
def upload_file():
    if "file" not in request.files:
        return jsonify({"error": "No file part"})

    file = request.files["file"]
    if file.filename == "":
        return jsonify({"error": "No selected file"})

    blob = storage.bucket().blob(file.filename)
    blob.upload_from_string(file.read(), content_type=file.content_type)

    return jsonify({"message": "File uploaded successfully"})

@app.route("/download/<filename>")
def download_file(filename):
    blob = storage.bucket().blob(filename)

    if not blob.exists():
        return jsonify({"error": "File not found"})

    blob.download_to_filename(filename)
    return send_file(filename)

if __name__ == "__main__":
    app.run(debug=True)
