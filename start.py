import os
import cv2
import glob
from flask import Flask, render_template, redirect, url_for, request, send_from_directory
from werkzeug.utils import secure_filename


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

        fn.procFile()
        print("end of if")

    else:
        print("false")
        import facenet_et as fn
        print("import")

        fn.procWeb()
        print("end of else")

    mas = fn.mas_of_dist
    mas_k = mas.keys()

    print(mas)
    print("*")
    maspl, masmi = choose(mas)
    print("**")
    factor_mas = create_factor_mas(maspl, masmi)
    print("\n", factor_mas)

    files = glob.glob(r"C:\Users\oboro\PycharmProjects\Union\proc_img\*")
    for f in files:
        os.remove(f)
    return render_template('index.html', data = mas)


def f_max(tmp):
    max_e = 0.
    max_k = None
    for k in tmp:
        if tmp[k] > max_e:
            max_e = tmp[k]
            max_k = k
    return max_k


def f_min(tmp):
    min_e = 2.
    min_k = None
    for k in tmp:
        if tmp[k] < min_e:
            min_e = tmp[k]
            min_k = k
    return min_k


def choose(mas):
    maspl = []
    masmi = []
    l_keys = list(mas.keys())
    i = 0
    while i <= 5:
        tmp = {}
        l_k = []
        for k in range(i * 8, i * 8 + 8):
            l_k.append(l_keys[k])

        for key in l_k:
            tmp[key] = mas[key]


        p = f_max(tmp)
        maspl.append(p.split("_")[1])
        tmp.pop(p)
        p = f_max(tmp)
        maspl.append(p.split("_")[1])
        tmp.pop(p)
        p = f_min(tmp)
        masmi.append(p.split("_")[1])
        tmp.pop(p)
        p = f_min(tmp)
        masmi.append(p.split("_")[1])
        tmp.pop(p)
        i = i + 1

    print("maspl = ")
    print(maspl)
    print("masmi = ")
    print(masmi)

    return maspl, masmi


def create_factor_mas(maspl, masmi):
    factor_mas = {'h': [], 's': [], 'e': [], 'hy': [], 'k': [],
                  'p': [], 'd': [], 'm': []}
    for i in maspl:
        factor_mas[i].append('+')

    for i in masmi:
        factor_mas[i].append('-')
    return factor_mas


if __name__ == "__main__":
        app.run()
