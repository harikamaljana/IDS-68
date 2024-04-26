from flask import Flask, render_template, jsonify, request, send_file
import subprocess
import os
import base64
import firebase_admin
from firebase_admin import credentials, firestore
import json
from datetime import datetime
from google.cloud import firestore
import pytz

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

@app.route('/fetch-timestamps/<model>', methods=['GET'])
def fetch_timestamps(model):
    timestamps = []
    algorithm_table_ref = db.collection(model)
    model_docs = algorithm_table_ref.order_by('timestamp', direction=firestore.Query.DESCENDING).limit(10).get()
    
    for doc in model_docs:
        # print(doc.to_dict()['timestamp'].astimezone(pytz.timezone('US/Central')))
        timestamps.append(doc.to_dict()['timestamp'])   
    return {'timestamps': timestamps}

@app.route('/fetch-data/<model>', methods=['GET'])
def fetch_data(model):
    algorithm_table_ref = db.collection(model)
    
    model_docs = algorithm_table_ref.order_by('timestamp', direction=firestore.Query.DESCENDING).limit(1).get()
    
    # Check if any documents were found
    if not model_docs:
        return jsonify({model: "No documents found"})
    
    # Get the first document from the query snapshot
    first_doc = model_docs[0]
    
    first_doc = first_doc.to_dict()
    # first_doc['timestamp'] = first_doc['timestamp'].isoformat()
        
    print(first_doc)
        
    return json.dumps(first_doc)
    

@app.route('/fetch-output-data/<model>/<id>', methods=['GET'])
def fetch_output_data(model, id):
    print('timestamp' + id)
    doc_ref = db.collection(model).document(id)
    # Get the document
    doc = doc_ref.get()
    # Assuming 'timestamps' is the collection and 'timestamp_doc' is the document
    doc_ref = db.collection(model).document(model+'.'+id)
    if doc.exists:
        # Document exists, access its data
        data = doc.to_dict()
        print(id + "Document data:", data)
        return data
    else:
        # Document does not exist
        print(id + "Document does not exist")
        return {'timestamp': 'NOT FOUND'}
    

@app.route('/run-model/<model>', methods=['POST'])
def run_model(model):
    try:
        time = datetime.now(pytz.utc).astimezone(pytz.timezone('US/Central')).timestamp()
        print(time)
        print('updated with the right model' + model + 'with time: ' + str(int(time*1000000)))
        req = request.json
        # print('PICKED with the right model' + json.dumps(req, indent=4))
        # Execute the Python script
        if model=='lccde':
            modelFile='LCCDE_IDS_GlobeCom22.py'
        elif model=='tree':
            modelFile='Tree-based_IDS_GlobeCom19.py'
        else:
            modelFile='MTH_IDS_IoTJ.py'
        
        import os

        # Specify the directory path you want to create
        heatmaps_dir = './heatmaps/'  # Update this to your actual directory

        # Check if the directory already exists
        if not os.path.exists(heatmaps_dir):
            # Create the directory if it doesn't exist
            os.makedirs(heatmaps_dir)
            print("Directory created successfully.")
        else:
            print("Directory already exists.")
        
        
        print('correct modelfile is selected' + model)
        # Load and encode images under the heatmaps directory
        if os.listdir(heatmaps_dir):
            for filename in os.listdir(heatmaps_dir):
                os.remove(heatmaps_dir+filename)
                
        # print('removed all existing files')
        store_data(model, req, time)
        result = subprocess.run(['python', modelFile], capture_output=True, text=True)
        
        print('running model file using subprocess' + model)

        if result.returncode == 0:
            # Script executed successfully
            output = result.stdout
            print("script runs")

            print(f'raw output: {output}')
            
            # JSONify output and images
            output_data = {'output': output, 'images': {}} # change to this when running actual
            # output_data = {'output': 'myouptut', 'images': {}}
            store_output(model, req, time, output)

            # Load and encode images under the heatmaps directory
            heatmaps_dir = 'heatmaps'  # Update this to your actual directory
            for filename in os.listdir(heatmaps_dir):
                if filename.endswith('.png'):
                    output_data['images'][filename] = f"/get_heatmap/{filename}"  # Adjust the URL as needed
            print('images OUTPUTTED')
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

# def get_data(model, id):
    
    

def store_data(model, req, time):
    print('malone')
    storage_id = model + "." + str(int(time*1000000))
    req['timestamp'] = time
    data_store = db.collection(model).document(storage_id)
    data_store.set(req)
    print('data stored')
    # return

def store_output(model, req, time, output):
    storage_id = model + "." + str(int(time*1000000))
    req['output'] = output
    data_store = db.collection(model).document(storage_id)
    data_store.set(req)
    print('output stored')

def store_heatmap(model, req, time):
    print('getting json data')
    
    # old_id = model + "." + 'timeafterexecution'
    storage_id = model + "." + str(int(time*1000000))
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
        filenames = ['MTH_DecisionTree.png', 'MTH_ExtraTree.png', 'MTH_hyperopt_et.png', 'MTH_hyperopt_dt.png', 'MTH_hyperopt_rf.png', 'MTH_hyperopt_xgb.png', 'MTH_RandomForest.png', 'MTH_stacking_hyperopt_xgb.png', 'MTH_stacking_xgb.png', 'MTH_XGBoost.png']
    
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
    req = {'images': base64dataImagesJson}
    print(list(req.keys()))
    print('updated files')
    # print(json.dumps(req))
    # exit()
    images_ref.update(req)
    
    print('done working')

if __name__ == '__main__':
    app.run(debug=True)
