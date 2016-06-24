# Import modules
import os
import flask.views
import pdfkit
from flask import Flask, render_template, request, redirect, url_for, send_from_directory, send_file
from werkzeug import secure_filename
#from flask_weasyprint import HTML, render_pdf
#from weasyprint import HTML
from nlq import clem_lda

# Initialize the Flask application
app = Flask(__name__, static_url_path = "", static_folder='static')
app.secret_key = "bacon"

# Set the path to the upload directory
app.config['UPLOAD_FOLDER'] = 'uploads/'

# Set extension that we are accepting to be uploaded
app.config['ALLOWED_EXTENSIONS'] = set(['txt', 'csv'])

# For a given file, return whether it's an allowed type or not
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in app.config['ALLOWED_EXTENSIONS']

# Define routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/nlq')
def nlq():
    return render_template('index.html')

@app.route('/tutorial')
def tutorial():
    return render_template('tutorial.html')

@app.route('/projects')
def projects():
    return render_template('projects.html')

@app.route('/thanks')
def thanks():
    return render_template('thanks.html')

@app.route('/education')
def education():
    return render_template('education.html')



@app.route('/predict', methods=['POST'])
def predcit():
    file_name = request.form['file_name']
    files = os.listdir('uploads')
    if file_name not in files:
        return 'File does not exist. Did you type the extension .csv?'

    a = ('uploads/{}'.format(file_name))

    z,text_name,f_name = clem_lda(a)


    
    return render_template('prediction.html', topics = z, title = text_name, f_name = f_name) 



#@app.route('/print_pdf')
#def print_pdf():
#    # Render pdf
#    return render_pdf('/education') -->


# Route that will process the file upload
@app.route('/upload', methods=['POST'])
def upload():
    # Get the name of the uploaded file
    file = request.files['file']
    # Check if the file is one of the allowed types/extensions
    if file and allowed_file(file.filename):
        # Make the filename safe, remove unsupported chars
        filename = secure_filename(file.filename)
        # Move the file form the temporal folder to
        # the upload folder we setup
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        # Redirect the user to the uploaded_file route, which
        # will basicaly show on the browser the uploaded file
        #return 1
        #redirect(url_for('uploaded_file', filename=filename))
        return redirect("/")


# This route is expecting a parameter containing the name
# of a file. Then it will locate that file on the upload
# directory and show it on the browser, so if the user uploads
# an image, that image is going to be show after the upload
@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'],
                               filename)


### Projetcts routes ###
# projects_names = ['NSF_Chem_2013']

# for name in projects_names:
#     predict_name = 'predict_{}'.format(name)

#     @app.route('/predict_{}'.format(name), methods=['POST'])
#     def predict_name():
#         fixed_file_name = '{}.csv'.format(name)
#         files = os.listdir('data')
#         a = ('data/{}'.format(fixed_file_name))
#         z,text_name,f_name = clem_lda(a)
#         return render_template('prediction.html', topics = z, title = text_name, f_name = f_name)

#     return_name = 'return_{}'.format(name)
#     @app.route('/return_{}'.format(name))
#     def return_name():
#         return send_file(a, as_attachment = True, attachment_filename = 'NSF_Chem_2013')

@app.route('/predict_NSF_Chem_2013', methods=['POST'])
def predcit_NSF_Chem_2013():
    fixed_file_name = 'NSF_Chem_2013.csv'
    files = os.listdir('data')
    a = ('data/{}'.format(fixed_file_name))
    z,text_name,f_name = clem_lda(a)
    return render_template('prediction.html', topics = z, title = text_name, f_name = f_name)

@app.route('/return_NSF_Chem_2013/')
def return_NSF_Chem_2013():
    return send_file('data/NSF_Chem_2013.csv', as_attachment = True, attachment_filename = 'NSF_Chem_2013')


@app.route('/predict_NSF_Bio_2015', methods=['POST'])
def predcit_NSF_Bio_2015():
    fixed_file_name = 'NSF_Bio_2015.csv'
    files = os.listdir('data')
    a = ('data/{}'.format(fixed_file_name))
    z,text_name,f_name = clem_lda(a)
    return render_template('prediction.html', topics = z, title = text_name, f_name = f_name)

@app.route('/return_NSF_Bio_2015/')
def return_NSF_Bio_2015():
    return send_file('data/NSF_Bio_2015.csv', as_attachment = True, attachment_filename = 'NSF_Bio_2015')
##############################################

@app.route('/dspipeline')
def dspeipeline():
    return render_template('dspipeline_home.html')

class View(flask.views.MethodView):
    def get(self):
        return flask.render_template('index.html')

    def post(self):
        result = eval(flask.request.form['expression'])
        flask.flash(result)
        return self.get()
    
app.add_url_rule('/', view_func=View.as_view('main'), methods=['GET', 'POST'])

app.debug = True
app.threaded = True
app.run()


