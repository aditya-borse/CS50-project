from flask import Flask, render_template, request, redirect, session, url_for, send_file
from helpers import PayTrackr, allowed_file
import os, tempfile, shutil
from threading import Timer
from werkzeug.utils import secure_filename

# Create a new instance of the Flask class called "app"
app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 100 * 1024 * 1024
app.secret_key = os.urandom(24)

# A list of files to delete
files_to_delete = []

@app.route('/')
def index():
    return redirect(url_for('upload_file'))


@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    # Handling the file
    if request.method == 'POST':
        if 'file' not in request.files:
            return redirect(url_for('apology', message='No file provided'))
        file = request.files['file']
        if file.filename == '':
            return redirect(url_for('apology', message='No file provided'))
        if not allowed_file(file.filename):
            return redirect(url_for('apology', message='Invalid file type'))
    
        # Storing the file in a temporary directory
        filename = secure_filename(file.filename)
        temp_dir = tempfile.gettempdir()
        file_path = os.path.join(temp_dir, filename)
        file.save(file_path)

        # Processing the file
        results, total_spent, csv_filename = PayTrackr(file_path)

        # Delete the temporary file
        os.remove(file_path)

        #Store the CSV file in the session
        session['csv_filename'] = csv_filename

        # Pass the results to the results page and render it
        return render_template('result.html', results=results, total_spent=total_spent)
    
    return render_template('upload.html')


@app.route('/download')
def download_file():
    filename = session.get('csv_filename')
    if not filename:
        return "File not found", 404
    
    original_file_path = filename

    temp_dir = tempfile.mkdtemp()
    temp_file_path = os.path.join(temp_dir, os.path.basename(filename))
    shutil.copy2(original_file_path, temp_file_path)

    files_to_delete.append(original_file_path)
    Timer(10, delete_file, args=[files_to_delete, temp_dir, 'transaction_files']).start()
    
    response = send_file(temp_file_path, as_attachment=True)
    session.clear()
    return response


def delete_file(files, temp_dir, directory_to_delete):
    try:
        for file_to_delete in files:
            os.remove(file_to_delete)
        shutil.rmtree(temp_dir)
        shutil.rmtree(directory_to_delete)
    except Exception as error:
        app.logger.error("Error removing or closing downloaded file handle", error)


@app.route('/apology')
def apology():
    message = request.args.get('message', 'Sorry, something went wrong.')
    return render_template('apology.html', message=message)


if __name__ == '__main__':
    app.run(debug=True)