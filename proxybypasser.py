from flask import Flask, request, jsonify, render_template
from os.path import isfile, join
from os import listdir
import base64
import io
import zipfile
import argparse

app = Flask(__name__)

conf = {
    'path': '',
    'host': '',
    'port': '',
}


@app.route('/')
def index():
    files = listdir(conf['path'])
    return render_template('filelist.html', filelist=files)


def makezip(filename, filedata):
    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, "a", zipfile.ZIP_DEFLATED, False) as zip_file:
        zip_file.writestr(filename, filedata)
    zip_buffer.seek(0)
    return zip_buffer.read()


@app.route('/download/<filename>')
def download(filename):
    p = join(conf['path'], filename)
    data = None
    with open(p, "rb") as file:
        data = file.read()

    data = makezip(filename, data)
    filecontent = base64.b64encode(data).decode("utf-8")
    return render_template('download.html', 
        filename=filename + ".zip", filecontent=filecontent)


def run_server():
    app.run(conf['host'], conf['port'])


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--port", help="Port to listen on", default="8081")
    parser.add_argument("--host", help="Host to listen on", default="0.0.0.0")
    parser.add_argument("--path", help="Path to serve", required=True)
    args = parser.parse_args()

    conf['host'] = args.host
    conf['port'] = args.port
    conf['path'] = args.path

    run_server()
