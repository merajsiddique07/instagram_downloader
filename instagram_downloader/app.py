from flask import Flask, render_template, request, send_file
import yt_dlp
import os

@app.route("/", methods=["GET", "POST"])
def index():
    message = ""
    if request.method == "POST":
        url = request.form.get("insta_url")
        if not url:
            message = "Please enter a valid Instagram URL."
        else:
            try:
                os.makedirs("downloads/instagram", exist_ok=True)

                ydl_opts = {
                    'outtmpl': 'downloads/instagram/%(title)s.%(ext)s',
                    'merge_output_format': 'mp4'
                }

                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    info_dict = ydl.extract_info(url, download=True)
                    filename = ydl.prepare_filename(info_dict)

                message = f"✅ Download complete! Check the downloads folder."

            except Exception as e:
                message = f"❌ Error: {e}"

    return render_template("index.html", message=message)
