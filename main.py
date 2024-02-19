from flask import Flask, request, render_template, url_for, redirect, request
from werkzeug.utils import secure_filename
from colorthief import ColorThief
# from PIL import Image
import os

# Initialize the app
app = Flask(__name__)

UPLOAD_FOLDER = "static/img"
ALLOWED_EXTENSTION = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}


def allowed_file(filename):
    print(filename)
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSTION


@app.route("/", methods=["GET", "POST"])
def upload():
    print("Enter")
    if request.method == "POST":
        if "file" not in request.files:
            return "No File Found"
        # to get the selected file(Image)
        file = request.files.get("file")
        if file.filename == "":
            return redirect(url_for("upload"))
        if file and allowed_file(file.filename):
            print(file.filename)
            filename = secure_filename(file.filename)  # return a secure version from the uploaded file
            file.save(os.path.join(UPLOAD_FOLDER, filename))
            return render_template("index.html", filename=file.filename)

    return render_template("index.html")


@app.route("/extract")
def extract_color():
    image_path = request.args.get("path", "")
    print(image_path)
    color_thief = ColorThief(f"static/img/{image_path}")
    dominant_palette = color_thief.get_palette(color_count=10)
    hex_colors = ['#' + ''.join(f'{int(c):02x}' for c in color) for color in dominant_palette]
    return render_template("index.html", filename=image_path, colors=hex_colors)


if __name__ == "__main__":
    app.run(debug=True)
