#import flask
import os
import time
from flask import Response, Flask, request, redirect, url_for,render_template
from werkzeug.utils import secure_filename
import subprocess

UPLOAD_FOLDER = 'upload/'
ALLOWED_EXTENSIONS = set(['jpg'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Create the application.
#APP = flask.Flask(__name__)
@app.route('/predict')
def get_data():
    """
    Return a string that is the output from subprocess
    """

    # There is a link above on how to do this, but here's my attempt
    # I think this will work for your Python 2.6
    #p = subprocess.Popen(['python label_image.py']) 
    #p = subprocess.call("python label_image.py upload/test.jpg", shell=True)
    def inner():
        proc = subprocess.Popen(
            ['python label_image.py upload/test.jpg'],             #call something with a lot of output so we can see it
            shell=True,
            stdout=subprocess.PIPE
        )
        printCount=0
        for line in iter(proc.stdout.readline,''):
            time.sleep(1)                           # Don't need this just shows the text streaming
            yield line.rstrip() + '<br/>\n'
            printCount=printCount+1
            if printCount==4:
               break
    return Response(inner(), mimetype='text/html')  # 
    #out, err = p.communicate()
    #p.communicate()
    #return "running"

@app.route('/')
def index():
    """ Displays the index page accessible at '/'
    """
    return render_template('index.html')

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = 'test.jpg'
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect('/predict')
    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form method=post enctype=multipart/form-data>
      <p><input type=file name=file>
         <input type=submit value=Upload>
    </form>
    '''

if __name__ == '__main__':
    app.debug=True
    app.run(host = '0.0.0.0')

