import os
import cv2
import glob
from flask import Flask, render_template, redirect, url_for, request, send_from_directory
from werkzeug.utils import secure_filename

"""import facenet as fn"""
"""from facenet_et import *"""

UPLOAD_FOLDER = r"C:\Users\oboro\PycharmProjects\Union\proc_img"
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])


app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'],
                               filename)


@app.route('/', methods=['GET'])
def hello_world():
    return render_template('index.html')


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


@app.route('/', methods=['GET', 'POST'])
def get_img():
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            savename = "file." + str(filename).split(".")[1]
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], savename))

    return render_template('index.html')


@app.route('/runFN', methods=['GET'])
def run_proc():
    print("run_proc")

    if (os.path.exists(r"C:\Users\oboro\PycharmProjects\Union\proc_img\file.png")):
        print("true")
        import facenet_et as fn
        print("import")
        #fn.FRmodel.compile(optimizer='adam', loss=fn.triplet_loss, metrics=['accuracy'])
        #fn.load_weights_from_FaceNet(fn.FRmodel)

        #database = fn.prepare_database()

        fn.procFile()

        print("end of if")
        mas = fn.mas_of_dist
        mas_k = mas.keys()
        print(mas)
    else:
        print("false")
        import facenet_et as fn
        print("import")
        #fn.FRmodel.compile(optimizer='adam', loss=fn.triplet_loss, metrics=['accuracy'])
        #fn.load_weights_from_FaceNet(fn.FRmodel)
        #database = fn.prepare_database()

        fn.procWeb()
        print("end of else")
        mas = fn.mas_of_dist
        mas_k = mas.keys()
        print(mas)
        #fn.do_code()

    files = glob.glob(r"C:\Users\oboro\PycharmProjects\Union\proc_img\*")
    for f in files:
        os.remove(f)
    return render_template('index.html', data = mas)






if __name__ == "__main__":
        app.run()
