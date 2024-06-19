
from flask import Flask, request, jsonify
from spleeter.separator import Separator
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)

@app.route('/separate_audio', methods=['POST'])
def separate_audio():
    if 'audio_file' not in request.files:
        return jsonify({'error': 'No audio file uploaded'}), 400

    audio_file = request.files['audio_file']
    try:
        # Initializing the separator with 2 stems (vocals and accompaniment)
        separator = Separator('spleeter:2stems')

        #filename in upload directory
        filename = secure_filename(audio_file.filename).replace('uploads_', 'uploads/')
        file_extension = os.path.splitext(filename)[1].replace('.','')
        print(file_extension)

        # Separate the audio file        
        separator.separate_to_file(filename, 'outputs', codec=file_extension)

        # Create a directory based on the filename without extension
        directory_name = os.path.splitext(os.path.basename(filename))[0]        
        target_dir = "outputs"

        # Construct the trackFilePath
        trackFilePath = os.path.join(target_dir, directory_name, f'accompaniment.{file_extension}')

        return jsonify({'status': 1, 'outputPath': trackFilePath})

    except Exception as e:
        return jsonify({'error': str(e)})

if __name__ == '__main__':
    app.run(debug=True)

