import subprocess
from io import BytesIO

from flask import Flask, render_template, request
from flask_cors import CORS, cross_origin
import colorama
import os
import logging
import time

app = Flask(__name__)

app.logger.disabled = True
log = logging.getLogger('werkzeug')
log.disabled = True

app.config['UPLOAD_FOLDER'] = "static"

@app.route("/", methods = ['POST', 'GET'])
def home():
    if request.method == "GET":
        return render_template("index.html")
    else:
        image_file = request.files['image']

        path_to_save = os.path.join("data", image_file.filename)
        image_file.save(path_to_save)
        image_size = os.stat(path_to_save).st_size

        config = "cfg/yolov4.cfg yolov4.weights " + path_to_save

        subprocess_out = subprocess.Popen("./darknet detect " + config, shell=True, stdout=subprocess.PIPE)
        subprocess_return = subprocess_out.stdout.read()
        path_to_display = os.path.join("../static", image_file.filename)

        subprocess_out.wait()

        os.replace("predictions.jpg", os.path.join("static", image_file.filename))

        count_of_person = str(subprocess_return).count("\\nperson")
        app_logger(count_of_person, image_file.filename, image_size)

        return render_template("index.html", user_image=path_to_display, exe_output=count_of_person)


def app_logger(person_count, image_name, image_size):
    timestr = time.strftime("%Y%m%d")
    logging.basicConfig(filename="app_log/app_log_" + timestr,
                        filemode='a',
                        format='%(asctime)s %(name)s %(levelname)s %(message)s',
                        datefmt="%Y-%m-%d %H:%M:%S",
                        level=logging.INFO)

    logger = logging.getLogger("yolo_app")

    logger.info("%i - %s - %.2f" % (person_count, image_name, image_size))


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9999, debug=True)
