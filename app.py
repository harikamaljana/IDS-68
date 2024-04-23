from flask import Flask, render_template, jsonify, request, send_file
import subprocess
import os
import base64
import firebase_admin
from firebase_admin import credentials, firestore
import json
from datetime import datetime
from google.cloud import firestore

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

@app.route('/fetch-data/<model>', methods=['GET'])
def fetch_data(model):
    algorithm_table_ref = db.collection(model)
    
    model_docs = algorithm_table_ref.get()
    
    model_data_list = []
    
    for doc in model_docs:
        model_data_list.append(doc.to_dict())
        
    return {model: model_data_list}
    

@app.route('/run-model/<model>', methods=['POST'])
def run_model(model):
    try:
        time = datetime.now()
        print('updated with the right model' + model)
        req = request.json
        # print('PICKED with the right model' + json.dumps(req, indent=4))
        # Execute the Python script
        if model=='lccde':
            modelFile='LCCDE_IDS_GlobeCom22.py'
        elif model=='tree':
            modelFile='Tree-based_IDS_GlobeCom19.py'
        else:
            modelFile='Tree-based_IDS_GlobeCom19.py'
        
        heatmaps_dir = './heatmaps/'  # Update this to your actual directory
        print('correct modelfile is selected' + model)
        # Load and encode images under the heatmaps directory
        if os.listdir(heatmaps_dir):
            for filename in os.listdir(heatmaps_dir):
                os.remove(heatmaps_dir+filename)
                
        # print('removed all existing files')
            
        result = subprocess.run(['python', modelFile], capture_output=True, text=True)
        
        print('running model file using subprocess' + model)

        if result.returncode == 0:
            # Script executed successfully
            output = result.stdout
            print("script runs")
            
            # JSONify output and images
            output_data = {'output': output, 'images': {}} # change to this when running actual
            # output_data = {'output': 'myouptut', 'images': {}}

            # Load and encode images under the heatmaps directory
            heatmaps_dir = 'heatmaps'  # Update this to your actual directory
            for filename in os.listdir(heatmaps_dir):
                if filename.endswith('.png'):
                    output_data['images'][filename] = f"/get_heatmap/{filename}"  # Adjust the URL as needed
                    
            store_heatmap(model, req, time)
            
            # Return JSON response with output and images
            return jsonify(output_data), 200
        else:
            # Error occurred while executing the script
            print('error not 0')
            error = result.stderr
            print('error not 0' + error)
            return jsonify({'error': error}), 500
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
@app.route('/get_heatmap/<path:filename>', methods=['GET'])
def get_heatmap(filename):
    return send_file(os.path.join('heatmaps', filename), mimetype='image/png')

def store_heatmap(model, req, time):
    print('getting json data')
    
    # old_id = model + "." + 'timeafterexecution'
    storage_id = model + "." + time.strftime("%Y-%m-%d_%H:%M:%S")
    # old_doc_ref = db.collection(model).document(old_id)
    # old_doc_data = old_doc_ref.get().to_dict()
    
    # Delete the old document
    # old_doc_ref.delete()
    
    # Create a new document with the updated data and the new ID
    # new_doc_ref = db.collection(model).document(new_id)
    # new_doc_ref.set(old_doc_data)

    # print('SID: \t' + storage_id)
    
    if (model == 'lccde'):
        filenames = ['CatBoost.png', 'lightGBM.png', 'XGBoost.png']
    elif (model == 'tree'):
        filenames = ['TB_DecisionTree.png', 'TB_ExtraTrees.png', 'TB_FS_DecisionTree.png', 'TB_FS_ExtraTrees.png', 'TB_FS_RandomForest.png', 'TB_FS_StackModel.png', 'TB_FS_XGB.png', 'TB_RandomForest.png', 'TB_StackModel.png', 'TB_XGB.png']
    else:
        filenames = []
    
    print('trying os gets')    
    files_directory = './heatmaps/'
    file_list = os.listdir(files_directory)
    print('finishing os gets')    
    base64dataImagesJson = {}
    
    print('WORKING - WITH UPDATES TO BASE')
    
    # for name in filenames:
    for f in file_list:
        if f in filenames:
            base64dataImagesJson[f] = encode_png_to_base64(files_directory+f)
    print('files are encoded')
    images_ref = db.collection(model).document(storage_id)
    print('files are decoded')
    
    req['images'] = base64dataImagesJson
    print('updated files')
    print(json.dumps(req))
    # exit()
    images_ref.set(req)
    
    print('done working')

if __name__ == '__main__':
    app.run(debug=True)
