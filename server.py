from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
import os
from bot_querry_engine import *

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

UPLOAD_FOLDER = 'data'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/',methods = ['GET'])
@cross_origin()
def hello():
    return 'Hello World!'

@app.route('/pdfQuestions', methods=['POST'])
@cross_origin()
def pdfQuestions():
    
    data = request.json
    reload = data.get('reload')
    prompt = data.get('prompt')
    chat_history = data.get('chat_history')


    if not prompt:
        return jsonify({"error": "No prompt provided"}), 400

    
    response = get_pdf_answers(reload, prompt, chat_history)
    return jsonify({"response": response})

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    file_path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(file_path)
    querry_eingine_upload_file(file_path)
    return jsonify({'success': 'File uploaded successfully'}), 200


if __name__ == '__main__':
    app.run(debug=True)