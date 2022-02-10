from flask import Flask, render_template, request
from flask_cors import CORS, cross_origin
import colorama
import os

app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = "static"

@app.route("/", methods = ['POST', 'GET'])
def home():
    if request.method == "GET":
        return render_template("index.html")
    else:
        image_file = request.files['image']
        path_to_save = os.path.join(app.config['UPLOAD_FOLDER'], image_file.filename)
        image_file.save(path_to_save)
        prediction_img = "/darknet/predictions.jpg"
        return render_template("index.html", user_image = path_to_save)

if __name__ == '__main__':
    app.run(host = '0.0.0.0', port=9999, debug=True)
