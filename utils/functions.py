from os import environ
import os
from flask import request, safe_join, jsonify
from werkzeug.utils import secure_filename
from flask.helpers import send_from_directory
import zipfile

FILES_DIRECTORY = environ.get('FILES_DIRECTORY')


def create_path():
    if not os.path.exists(FILES_DIRECTORY):
        
        os.makedirs(FILES_DIRECTORY)


def get_extension(item):
        
        return item.split('.')[-1]


def recived_files():

    files_list = list(request.files)
    upload_files_list = []
    directory = os.listdir(FILES_DIRECTORY)

    try:

        if len(files_list) == 0:
            return {'msg': 'Send at least one file'}, 406

        for file in files_list:

            files_received = request.files[file]
            
            file_name = secure_filename(files_received.filename)

            if get_extension(file_name) == 'png' or get_extension(file_name) == 'jpg' or get_extension(file_name) == 'gif':
                
                file_path = safe_join(FILES_DIRECTORY, file_name)
                
                files_received.save(file_path)
                
                upload_files_list.append({'file': f'{file_name}'})
            
            else:

                return {'msg': 'One of the files is different from the supported format'}, 415 
            
            if file_name in directory:
                return {"msg": "This file name already exists"}, 409
            
        return jsonify(upload_files_list), 201
    
    except TypeError:

        return {"msg": "1MB maximum allowed size exceeded"}, 413


def get_files():

    files = []

    directory = os.listdir(FILES_DIRECTORY)
    
    for file in directory:
            files.append(file)
        
    if files == []:
        return {'msg':'This list is empty'}, 404
    else:
        return jsonify(files)


def get_files_by_type(type):

    files = []
    directory = os.listdir(FILES_DIRECTORY)

    for file in directory:
        
        if get_extension(file) == type:
            
            files.append(file)
        
        elif files == []:
        
            return {'msg': 'No file founded!'}, 404
    
    return jsonify(files)


def single_file_download(file):
    
    try:

        return send_from_directory(
            directory='../uploads',
            path=f'{file}',
            as_attachment=True
        )

    except:

        return {'msg': 'File not found!'}, 404


def zip_file_download():
    directory = os.listdir(FILES_DIRECTORY)
    
    file_type = request.args.get('file_type')

    with zipfile.ZipFile('/tmp/zipped_files.zip', 'w') as new_zip:

        for file in directory:

            if get_extension(file) == file_type:

                new_zip.write(f'./uploads/{file}', compress_type=zipfile.ZIP_DEFLATED)

        if new_zip.namelist() == '':
            
            return {'msg': 'Empty folder'}, 404
        
        else:
            
            return send_from_directory(
                directory='/tmp',
                path='zipped_files.zip',
                as_attachment=True
            ), 200

