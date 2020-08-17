import datetime
import os
import time

from flask import Flask, render_template, request 
#from PIL import Image
#from werkzeug import secure_filename
from werkzeug.utils import secure_filename
from gen_paintings import run_style_transfer

app = Flask(__name__)


@app.route('/')
def root():
    # For the sake of example, use static information to inflate the template.
    # This will be replaced with real information in later steps.
    dummy_times = [datetime.datetime(2018, 1, 1, 10, 0, 0),
                   datetime.datetime(2018, 1, 2, 10, 30, 0),
                   datetime.datetime(2018, 1, 3, 11, 0, 0),
                   ]

    return render_template('index.html', times=dummy_times)

@app.route('/style')
def style():
    dummy_times = [datetime.datetime(2018, 1, 1, 10, 0, 0),
                   datetime.datetime(2018, 1, 2, 10, 30, 0),
                   datetime.datetime(2018, 1, 3, 11, 0, 0),
                   ]

    return render_template('style.html', times=dummy_times)

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    sfname = 'not yet#'
    if request.method == 'POST':
        f = request.files['photo']
        path = 'static/uploaded/' + time.asctime() 
        sfname = path + "/" + str(secure_filename(f.filename))
        print("deebug: hello")
        try:
            os.makedirs(path)
        except OSError as err:
            print ("deebug: Creation of the directory %s failed:%s" % (path, err))
        else:
            print ("deebug: Creation of the directory %s succeeded" % path)
        f.save(sfname)
        run_style_transfer(sfname)

    return render_template('upload.html', sfname=sfname)

if __name__ == '__main__':
    # This is used when running locally only. When deploying to Google App
    # Engine, a webserver process such as Gunicorn will serve the app. This
    # can be configured by adding an `entrypoint` to app.yaml.
    # Flask's development server will automatically serve static files in
    # the "static" directory. See:
    # http://flask.pocoo.org/docs/1.0/quickstart/#static-files. Once deployed,
    # App Engine itself will serve those files as configured in app.yaml.
    app.run(host='127.0.0.1', port=8080, debug=True)
# [START gae_python37_render_template]
