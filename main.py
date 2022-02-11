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
    log_filename = "app_log/app_log_" + timestr
    os.makedirs(os.path.dirname(log_filename), exist_ok=True)
    logging.basicConfig(filename=log_filename,
                        filemode='a',
                        format='%(asctime)s %(name)s %(levelname)s %(message)s',
                        datefmt="%Y-%m-%d %H:%M:%S")

    logger = logging.getLogger("yolo_app")

    file_handler = logging.FileHandler(log_filename, mode="a", encoding=None, delay=False)
    file_handler.setLevel(level=logging.DEBUG)

    logger.addHandler(file_handler)

    logger.info("%i - %s - %.2f" % (person_count, image_name, image_size))


@app.route("/log", methods=['POST'])
def get_log():
    log_file_path = 'app_log/app_log_' + time.strftime("%Y%m%d")
    if os.path.isfile(log_file_path):
        with app.open_resource(log_file_path) as f:
            contents = f.read()
    else:
        contents = "No log for today"
    return contents


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9999, debug=True)
