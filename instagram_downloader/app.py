from flask import Flask, render_template, request
import instaloader
import os
from urllib.parse import urlparse

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    message = ""
    if request.method == "POST":
        url = request.form.get("insta_url")
        if not url:
            message = "Please enter a valid Instagram URL."
        else:
            try:
                L = instaloader.Instaloader()

                # Optional: Uncomment and use your login for private posts
                # L.login('YOUR_USERNAME', 'YOUR_PASSWORD')

                # Extract shortcode
                path_parts = urlparse(url).path.strip("/").split("/")
                if "p" in path_parts or "reel" in path_parts:
                    shortcode = path_parts[-1] if path_parts[-1] else path_parts[-2]
                else:
                    return "Invalid Instagram URL."

                post = instaloader.Post.from_shortcode(L.context, shortcode)

                os.makedirs("downloads", exist_ok=True)
                L.download_post(post, target="downloads")

                message = "✅ Download complete! Check the server's downloads folder."

            except Exception as e:
                message = f"❌ Error: {e}"

    return render_template("index.html", message=message)

if __name__ == "__main__":
    app.run(debug=True)
