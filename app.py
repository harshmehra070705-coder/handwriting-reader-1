import os
import base64
from flask import Flask, request, render_template_string
from google import genai
from google.genai import types

app = Flask(__name__)

API_KEY = os.environ.get("GOOGLE_API_KEY")

if not API_KEY:
    raise ValueError("GOOGLE_API_KEY not set")

client = genai.Client(api_key=API_KEY)

HTML_PAGE = """
<!DOCTYPE html>
<html>
<head>
    <title>Cursive Handwriting Reader</title>
    <style>
        body { font-family: Arial; background:#f4f6f9; text-align:center; padding:40px; }
        .box { background:white; padding:30px; border-radius:10px; width:60%; margin:auto; box-shadow:0 4px 10px rgba(0,0,0,0.1); }
        button { padding:10px 20px; background:#4CAF50; color:white; border:none; border-radius:5px; cursor:pointer; }
        button:hover { background:#45a049; }
        textarea { width:100%; height:200px; margin-top:20px; padding:10px; }
        img { margin-top:20px; max-width:300px; border-radius:8px; }
    </style>
</head>
<body>

<div class="box">
    <h2>✍️ Cursive Handwriting Reader</h2>

    <form method="POST" action="/extract" enctype="multipart/form-data">
        <input type="file" name="image" required>
        <br><br>
        <button type="submit">Convert to Text</button>
    </form>

    {% if image_preview %}
        <h3>Uploaded Image:</h3>
        <img src="data:image/jpeg;base64,{{ image_preview }}">
    {% endif %}

    {% if result %}
        <h3>Converted Text:</h3>
        <textarea readonly>{{ result }}</textarea>
    {% endif %}
</div>

</body>
</html>
"""

@app.route("/")
def home():
    return render_template_string(HTML_PAGE)


@app.route("/extract", methods=["POST"])
def extract():
    try:
        image = request.files["image"]
        image_bytes = image.read()

        image_base64 = base64.b64encode(image_bytes).decode("utf-8")

        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=[
                "You are an expert handwriting reader. Read the cursive handwritten text carefully and convert it into clean, properly formatted, easy-to-understand typed text. Only return the cleaned text.",
                types.Part.from_bytes(
                    data=image_bytes,
                    mime_type=image.mimetype,
                ),
            ],
        )

        return render_template_string(
            HTML_PAGE,
            result=response.text,
            image_preview=image_base64
        )

    except Exception as e:
        return f"<h3>Error:</h3> {str(e)}"


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
