import os
from flask import Flask, request, render_template_string
import google.generativeai as genai

app = Flask(__name__)

# ✅ API Key
API_KEY = os.environ.get("GOOGLE_API_KEY")
genai.configure(api_key=API_KEY)

model = genai.GenerativeModel("gemini-1.5-flash")

# ✅ Simple HTML Template
HTML_PAGE = """
<!DOCTYPE html>
<html>
<head>
    <title>Cursive Handwriting Reader</title>
</head>
<body style="font-family: Arial; text-align: center; margin-top: 50px;">

    <h2>Cursive Handwriting Reader ✍️</h2>

    <form method="POST" action="/extract-text" enctype="multipart/form-data">
        <input type="file" name="image" required>
        <br><br>
        <button type="submit">Convert to Text</button>
    </form>

    {% if result %}
        <h3>Converted Text:</h3>
        <div style="width:60%; margin:auto; padding:15px; border:1px solid #ccc;">
            {{ result }}
        </div>
    {% endif %}

</body>
</html>
"""

@app.route("/", methods=["GET"])
def home():
    return render_template_string(HTML_PAGE)


@app.route("/extract-text", methods=["POST"])
def extract_text():
    try:
        image = request.files["image"]
        image_bytes = image.read()

        response = model.generate_content(
            [
                """You are an expert handwriting reader.
                The image contains cursive or unclear handwritten text.
                Carefully read it and convert it into clean,
                properly formatted, easy-to-understand typed text.
                Only return the cleaned text.""",
                {
                    "mime_type": image.mimetype,
                    "data": image_bytes
                }
            ]
        )

        return render_template_string(HTML_PAGE, result=response.text)

    except Exception as e:
        return f"Error: {str(e)}"


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
