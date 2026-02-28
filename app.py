import os
import time
from flask import Flask, request, jsonify
import google.generativeai as genai
from google import genai

app = Flask(__name__)

client = genai.Client(api_key="YOUR_API_KEY")

response = client.models.generate_content(
    model="gemini-1.5-flash",
    contents="Hello"
)

print(response.text)

@app.route("/")
def home():
    return "App is running ✅"

@app.route('/')
def index():
    return
    if __name__ == "__main__":

port = int(os.environ.get("PORT", 10000))
app.run(host="0.0.0.0", port=port)
Deploy karo.

'''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Handwriting Reader</title>
    <style>
        * { margin:0; padding:0; box-sizing:border-box; }
        body {
            font-family: 'Segoe UI', Arial, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
            padding: 20px;
        }
        .container {
            background: white;
            border-radius: 20px;
            padding: 40px;
            max-width: 600px;
            width: 100%;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
            text-align: center;
        }
        h1 { color:#333; margin-bottom:8px; font-size:32px; }
        .subtitle { color:#888; margin-bottom:30px; font-size:16px; }
        .upload-area {
            border: 3px dashed #667eea;
            border-radius: 15px;
            padding: 40px 20px;
            cursor: pointer;
            transition: all 0.3s;
            margin-bottom: 20px;
            background: #fafafe;
        }
        .upload-area:hover { background:#f0f0ff; border-color:#764ba2; }
        .upload-icon { font-size:50px; margin-bottom:10px; }
        .upload-area p { color:#667eea; font-size:16px; }
        .upload-area .small { color:#aaa; font-size:13px; margin-top:5px; }
        #preview {
            max-width: 100%; max-height: 300px;
            border-radius: 10px; display: none;
            margin: 15px auto;
            box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        }
        .file-name { color:#333; font-size:14px; margin-bottom:10px; display:none; }
        button {
            width: 100%; padding: 16px;
            background: linear-gradient(135deg, #667eea, #764ba2);
            color: white; border: none; border-radius: 12px;
            font-size: 18px; font-weight: bold;
            cursor: pointer; transition: all 0.3s;
        }
        button:hover {
            transform: translateY(-2px);
            box-shadow: 0 8px 25px rgba(102,126,234,0.4);
        }
        button:disabled { opacity:0.5; cursor:not-allowed; transform:none; box-shadow:none; }
        .loading { display:none; margin-top:25px; padding:20px; }
        .spinner {
            width:40px; height:40px;
            border: 4px solid #e0e0e0;
            border-top: 4px solid #667eea;
            border-radius: 50%;
            animation: spin 1s linear infinite;
            margin: 0 auto 15px;
        }
        @keyframes spin { to { transform: rotate(360deg); } }
        .loading p { color:#667eea; font-size:16px; }
        .result {
            margin-top:25px; padding:25px;
            background:#f8f9fa; border-radius:12px;
            border-left: 5px solid #667eea;
            display:none; text-align:left;
        }
        .result h3 { color:#333; margin-bottom:12px; font-size:18px; }
        .result-text {
            color:#555; line-height:1.8; white-space:pre-wrap;
            font-size:15px; background:white; padding:15px;
            border-radius:8px; border:1px solid #e0e0e0;
        }
        .copy-btn {
            width:auto; padding:8px 20px; font-size:14px;
            margin-top:12px; background:#28a745; border-radius:8px;
        }
        .copy-btn:hover { background:#218838; }
        .error-text { color:#dc3545; }
        .footer { margin-top:25px; color:#aaa; font-size:13px; }
    </style>
</head>
<body>
    <div class="container">
        <h1>Handwriting Reader</h1>
        <p class="subtitle">Upload a handwritten image and AI will read it</p>
        <div class="upload-area" onclick="document.getElementById('fileInput').click()">
            <div class="upload-icon">📷</div>
            <p>Click here to upload image</p>
            <p class="small">Supports JPG, PNG, JPEG</p>
            <input type="file" id="fileInput" accept="image/*"
                   style="display:none" onchange="previewImage(this)">
            <img id="preview" src="" alt="Preview">
        </div>
        <p class="file-name" id="fileName"></p>
        <button id="analyzeBtn" onclick="analyzeImage()" disabled>
            Read Handwriting
        </button>
        <div class="loading" id="loading">
            <div class="spinner"></div>
            <p>AI is reading your handwriting... please wait</p>
        </div>
        <div class="result" id="result">
            <h3>Extracted Text:</h3>
            <div class="result-text" id="resultText"></div>
            <button class="copy-btn" onclick="copyText()">Copy Text</button>
        </div>
        <p class="footer">Powered by Google Gemini AI</p>
    </div>
    <script>
        function previewImage(input) {
            const file = input.files[0];
            if (file) {
                const reader = new FileReader();
                reader.onload = function(e) {
                    document.getElementById('preview').src = e.target.result;
                    document.getElementById('preview').style.display = 'block';
                    document.getElementById('analyzeBtn').disabled = false;
                    document.getElementById('fileName').textContent = file.name;
                    document.getElementById('fileName').style.display = 'block';
                    document.getElementById('result').style.display = 'none';
                }
                reader.readAsDataURL(file);
            }
        }
        async function analyzeImage() {
            const fileInput = document.getElementById('fileInput');
            const file = fileInput.files[0];
            if (!file) { alert('Upload image first!'); return; }
            const formData = new FormData();
            formData.append('image', file);
            document.getElementById('loading').style.display = 'block';
            document.getElementById('result').style.display = 'none';
            document.getElementById('analyzeBtn').disabled = true;
            try {
                const response = await fetch('/analyze', {
                    method: 'POST',
                    body: formData
                });
                const data = await response.json();
                if (data.error) {
                    document.getElementById('resultText').innerHTML =
                        '<span class="error-text">Error: ' + data.error + '</span>';
                } else {
                    document.getElementById('resultText').textContent = data.text;
                }
                document.getElementById('result').style.display = 'block';
            } catch (error) {
                document.getElementById('resultText').innerHTML =
                    '<span class="error-text">Error: ' + error.message + '</span>';
                document.getElementById('result').style.display = 'block';
            }
            document.getElementById('loading').style.display = 'none';
            document.getElementById('analyzeBtn').disabled = false;
        }
        function copyText() {
            const text = document.getElementById('resultText').textContent;
            navigator.clipboard.writeText(text).then(function() {
                alert('Text copied!');
            });
        }
    </script>
</body>
</html>
'''

@app.route('/analyze', methods=['POST'])
def analyze():
    if 'image' not in request.files:
        return jsonify({'error': 'No image uploaded'}), 400

    image = request.files['image']
    image_data = image.read()

    # Retry logic — agar quota error aaye toh 3 baar try karega
    max_retries = 3
    for attempt in range(max_retries):
        try:
            response = model.generate_content([
                "Read the handwriting in this image and return the extracted text only.",
                {"mime_type": image.content_type, "data": image_data}
            ])
            return jsonify({'text': response.text})
        except Exception as e:
            error_msg = str(e)
            if '429' in error_msg and attempt < max_retries - 1:
                # Quota error — wait and retry
                time.sleep(5)
                continue
            else:
                return jsonify({'error': error_msg}), 500

    return jsonify({'error': 'API quota exceeded. Please try again later.'}), 429

if __name__ == '__main__':
    app.run(debug=True)
