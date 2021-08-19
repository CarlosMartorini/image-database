from flask import Flask, request, safe_join, jsonify
import os
from datetime import datetime
from flask.helpers import send_from_directory
from werkzeug.utils import secure_filename
import zipfile

app = Flask(__name__)

FILES_DIRECTORY = './uploads'

if not os.path.exists(FILES_DIRECTORY):
    
    os.makedirs(FILES_DIRECTORY)

CHARACTERS_TO_REPLACE = [' ', ':', '-']


def get_extension(item):
        
        return item.split('.')[-1]


@app.route('/upload', methods=['POST'])
def upload_files_list():
    
    MAX_CONTENT_LENGTH = 1024
    
    files_list = list(request.files)

    if len(files_list) == 0:
        
        return {'msg': 'Send at least one file'}, 406

    upload_files_list = []

    for file in files_list:

        files_received = request.files[file]
        
        file_name = secure_filename(files_received.filename)

        if get_extension(file_name) == 'png' or get_extension(file_name) == 'jpg' or get_extension(file_name) == 'gif':
            
            file_path = safe_join(FILES_DIRECTORY, file_name)
            
            files_received.save(file_path)
            
            upload_files_list.append({'file': f'{file_name}'})
        
        else:

            return {'msg': 'One of the files is different from the supported format'}, 415 

    return jsonify(upload_files_list), 201


@app.route('/files', methods=['GET'])
def show_files():
    
    files = []
    
    directory = os.listdir(FILES_DIRECTORY)
    
    for file in directory:
            files.append(file)
        
    if files == []:
        return {'msg':'This list is empty'}
    else:
        return jsonify(files)


@app.route('/files/<string:type>', methods=['GET'])
def show_filtered_files(type: str):
    
    files = []
    
    directory = os.listdir(FILES_DIRECTORY)

    for file in directory:
        
        if get_extension(file) == type:
            
            files.append(file)
        
        elif files == []:
        
            return {'msg': 'No file founded!'}
    
    return jsonify(files)


@app.route('/download/<string:file_name>', methods=['GET'])
def download_file(file_name: str):
    
    try:

        return send_from_directory(
            directory='../uploads',
            path=f'{file_name}',
            as_attachment=True
        )

    except:

        return {'msg': 'File not found!'}, 404


@app.route('/download-zip', methods=['GET'])
def download_zip():
    
    directory = os.listdir(FILES_DIRECTORY)
    
    file_type = request.args.get('file_type')

    with zipfile.ZipFile('../../.asdf/tmp/zipped_files.zip', 'w') as new_zip:

        for file in directory:

            if get_extension(file) == file_type:

                new_zip.write(f'./uploads/{file}', compress_type=zipfile.ZIP_DEFLATED)

        if new_zip.namelist() == '':
            
            return {'msg': 'Empty folder'}, 404
        
        else:
            
            return send_from_directory(
                directory='../../../.asdf/tmp',
                path='zipped_files.zip',
                as_attachment=True
            ), 200

