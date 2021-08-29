from flask import Flask
from os import environ
from utils.functions import recived_files, create_path, get_files, get_files_by_type, single_file_download, zip_file_download

app = Flask(__name__)

create_path()

MAX_CONTENT = environ.get('MAX_CONTENT_LENGTH')
app.config['MAX_CONTENT_LENGTH'] = 1000000

@app.route('/upload', methods=['POST'])
def upload_files_list():

    return recived_files()
    

@app.route('/files', methods=['GET'])
def show_files():
    
    return get_files()


@app.route('/files/<string:type>', methods=['GET'])
def show_filtered_files(type: str):
    
    return get_files_by_type(type)


@app.route('/download/<string:file_name>', methods=['GET'])
def download_file(file_name: str):
    
   return single_file_download(file_name)


@app.route('/download-zip', methods=['GET'])
def download_zip():
    
    return zip_file_download()

