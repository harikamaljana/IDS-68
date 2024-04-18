from flask import Flask, render_template, jsonify, request, send_file
import subprocess
import os
import base64
import firebase_admin
from firebase_admin import credentials, firestore
import json

# Initialize Firebase Admin SDK
cred = firebase_admin.credentials.Certificate("./idst68-firebase-adminsdk-zynhs-075a598f91.json")
firebase_admin.initialize_app(cred)

db = firebase_admin.firestore.client()

def encode_png_to_base64(file_path):
    with open(file_path, 'rb') as file:
        png_data = file.read()
        return base64.b64encode(png_data).decode('utf-8')

def decode_base64_to_png(base64_data, output_path):
    png_data = base64.b64decode(base64_data.encode('utf-8'))
    with open(output_path, 'wb') as file:
        file.write(png_data)

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('frontend.html')

@app.route('/run-model', methods=['POST'])
def run_model():
    try:
        # Execute the Python script
        result = subprocess.run(['python', 'LCCDE_IDS_GlobeCom22.py'], capture_output=True, text=True)

        if result.returncode == 0:
            # Script executed successfully
            print("script runs")
            output = result.stdout

            # JSONify output and images
            output_data = {'output': output, 'images': {}}

            
            
            # Load and encode images under the heatmaps directory
            heatmaps_dir = 'heatmaps'  # Update this to your actual directory
            for filename in os.listdir(heatmaps_dir):
                if filename.endswith('.png'):
                    output_data['images'][filename] = f"/get_heatmap/{filename}"  # Adjust the URL as needed
                    
            store_heatmap()
            
            # Return JSON response with output and images
            return jsonify(output_data), 200
        else:
            # Error occurred while executing the script
            error = result.stderr
            return jsonify({'error': error}), 500
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/get_heatmap/<path:filename>', methods=['GET'])
def get_heatmap(filename):
    return send_file(os.path.join('heatmaps', filename), mimetype='image/png')

# @app.route('/store_heatmap/<path:filename>', methods=['GET'])
def store_heatmap():
    # Example usage
    catboost_png_file_path = './heatmaps/CatBoost.png';
    lightgbm_png_file_path = './heatmaps/lightGBM.png';
    xgboost_png_file_path = './heatmaps/XGBoost.png';
    # json_file_path = './json_outputs/lccde_images.json';

    # Encode PNG file to base64 and store in JSON format
    catboost_png_base64_data = encode_png_to_base64(catboost_png_file_path)
    lightgbm_png_base64_data = encode_png_to_base64(lightgbm_png_file_path)
    xgboost_png_base64_data = encode_png_to_base64(xgboost_png_file_path)
        
    images_ref = db.collection('images')
    
    images_ref.add({
        'catboost_png': catboost_png_base64_data,
        'lightgbm_png': lightgbm_png_base64_data,
        'xgboost_png': xgboost_png_base64_data
    })
    # return "Images stored in Firestore"


if __name__ == '__main__':
    app.run(debug=True)
