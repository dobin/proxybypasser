from flask import Flask, request, jsonify, render_template
from os.path import isfile, join
from os import listdir
import base64
import io
import zipfile

app = Flask(__name__)

path = '/'

@app.route('/')
def index():
    files = listdir(path)
    print(str(files))

    return render_template('filelist.html', filelist=files)


def makezip(filename, filedata):
    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, "a", zipfile.ZIP_DEFLATED, False) as zip_file:
        zip_file.writestr(filename, filedata)
    zip_buffer.seek(0)
    return zip_buffer.read()


@app.route('/download/<filename>')
def download(filename):
    p = join(path, filename)
    data = None
    with open(p, "rb") as file:
        data = file.read()

    data = makezip(filename, data)
    filecontent = base64.b64encode(data).decode("utf-8")
    print(str(filecontent))
    return render_template('download.html', 
        filename=filename + ".zip", filecontent=filecontent)

def run_server():
    app.run("0.0.0.0", "8081")


if __name__ == "__main__":
    run_server()
