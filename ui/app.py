import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from flask import Flask, render_template, request, jsonify
import requests
from pipeline.ingest import process_uploaded_file

app = Flask(__name__)

API_URL = "http://127.0.0.1:8000/ask"

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/ask", methods=["POST"])
def ask():
    try:
        data = request.get_json()
        question = data.get("question")

        response = requests.post(API_URL, json={"question": question})
        result = response.json()

        return jsonify(result)

    except Exception:
        return jsonify({
            "answer": "Error connecting to AI backend.",
            "sources": []
        })
        
@app.route("/upload", methods=["POST"])
def upload():
    try:
        uploaded_files = request.files.getlist("files")  # multiple files
        if not uploaded_files:
            return jsonify({"message": "No files uploaded"})

        for file in uploaded_files:
            filepath = os.path.join(UPLOAD_FOLDER, file.filename)
            file.save(filepath)
            process_uploaded_file(filepath)  # process each file

        return jsonify({"message": f"{len(uploaded_files)} file(s) uploaded and processed!"})

    except Exception as e:
        print("ERROR:", str(e))
        import traceback
        traceback.print_exc()
        return jsonify({"message": f"Upload failed: {str(e)}"})
    
    
if __name__ == "__main__":
    app.run(debug=True)