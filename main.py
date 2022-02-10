import subprocess

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
        image_file_name = request.files['image'].filename
        # path_to_save = os.path.join(app.config['UPLOAD_FOLDER'], image_file_name)
        path_to_save = os.path.join("../data", image_file_name)
        config = "cfg/yolov4.cfg yolov4.weights " + path_to_save
        # subprocess.call("../darknet detect -config " + config)
        subprocess_out = subprocess.Popen("./darknet detect -config " + config, shell=True, stdout=subprocess.PIPE)
        subprocess_return = subprocess_out.stdout.read()
        print(subprocess_return)

        subprocess_out.wait()

        os.replace("../predictions.jpg", path_to_save)

        return render_template("index.html", user_image=path_to_save, exe_output=subprocess_return)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9999, debug=True)
