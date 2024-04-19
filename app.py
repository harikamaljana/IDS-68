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

@app.route('/run-model/<model>', methods=['POST'])
def run_model(model):
    try:
        print('updated with the right model' + model)
        req = request.json
        print('PICKED with the right model' + json.dumps(req, indent=4))
        # Execute the Python script
        if model=='lccde':
            modelFile='LCCDE_IDS_GlobeCom22.py'
        else:
            modelFile='Tree-based_IDS_GlobeCom19.py'
        
        heatmaps_dir = './heatmaps/'  # Update this to your actual directory
        
        # Load and encode images under the heatmaps directory
        if os.listdir(heatmaps_dir):
            for filename in os.listdir(heatmaps_dir):
                os.remove(heatmaps_dir+filename)
            
        result = subprocess.run(['python', modelFile], capture_output=True, text=True)

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
                    
            store_heatmap(model, req)
            
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

def store_heatmap(model, req):
    print('getting json data')
    
    storage_id = model + "." + req['dc']['algorithm_name'] + "." + req['dc']['epochs']
    
    print('SID: \t' + storage_id)
    
    if (model == 'lccde'):
        filenames = ['CatBoost.png', 'lightGBM.png', 'XGBoost.png']
    elif (model == 'tree'):
        filenames = ['TB_DecisionTree.png', 'TB_ExtraTrees.png', 'TB_FS_DecisionTree.png', 'TB_FS_ExtraTrees.png', 'TB_FS_RandomForest.png', 'TB_FS_StackModel.png', 'TB_FS_XGB.png', 'TB_RandomForest.png', 'TB_StackModel.png', 'TB_XGB.png']
    else:
        filenames = []
        
    files_directory = './heatmaps/'
    file_list = os.listdir(files_directory)
    base64dataImagesJson = {}
    
    print('WORKING - WITH UPDATES TO BASE')
    
    # for name in filenames:
    for f in file_list:
        if f in filenames:
            base64dataImagesJson[f] = encode_png_to_base64(files_directory+f)
        
    images_ref = db.collection('Algorithm').document(storage_id)
    
    images_ref.update({
        'images': base64dataImagesJson
        
    })
    
    print('done working')

if __name__ == '__main__':
    app.run(debug=True)
