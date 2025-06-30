import os
from flask import Flask, request, render_template, send_file
import subprocess
import uuid

app = Flask(__name__)

DOWNLOAD_DIR = "downloads"

# Ensure the downloads folder exists
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        url = request.form["url"]

        # 1️⃣ Get cookies from environment
        cookies = os.getenv("INSTAGRAM_COOKIES")

        if not cookies:
            return "❌ ERROR: No Instagram cookies found. Please set the INSTAGRAM_COOKIES environment variable."

        # 2️⃣ Format cookies (replace \n with actual newlines)
        cookies = cookies.replace("\\n", "\n")

        # 3️⃣ Write cookies.txt for yt-dlp
        cookies_file = "cookies.txt"
        with open(cookies_file, "w") as f:
            f.write(cookies)

        # 4️⃣ Generate a unique output file name
        output_file = os.path.join(DOWNLOAD_DIR, f"{uuid.uuid4()}.mp4")

        # 5️⃣ Build yt-dlp command
        command = [
            "yt-dlp",
            "--cookies", cookies_file,
            "-f", "best",
            "-o", output_file,
            url
        ]

        # 6️⃣ Run yt-dlp
        try:
            subprocess.run(command, check=True)
        except subprocess.CalledProcessError as e:
            return f"❌ ERROR: yt-dlp failed: {str(e)}"

        # 7️⃣ Serve the downloaded file
        return send_file(output_file, as_attachment=True)

    return render_template("index.html")
