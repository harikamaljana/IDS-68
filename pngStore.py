import json
import base64
import firebase_admin
from firebase_admin import credentials, firestore

# Initialize Firebase Admin SDK
cred = firebase_admin.credentials.Certificate("./idst68-firebase-adminsdk-zynhs-e4b0582bd5.json")
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



# # Example usage
# catboost_png_file_path = './heatmaps/CatBoost.png';
# lightgbm_png_file_path = './heatmaps/lightGBM.png';
# xgboost_png_file_path = './heatmaps/XGBoost.png';
# json_file_path = './json_outputs/lccde_images.json';

# # Encode PNG file to base64 and store in JSON format
# catboost_png_base64_data = encode_png_to_base64(catboost_png_file_path)
# lightgbm_png_base64_data = encode_png_to_base64(lightgbm_png_file_path)
# xgboost_png_base64_data = encode_png_to_base64(xgboost_png_file_path)
# json_data = {'catboost_png': catboost_png_base64_data, 'lightgbm_png': lightgbm_png_base64_data, 'xgboost_png': xgboost_png_base64_data}
# with open(json_file_path, 'w') as json_file:
#     json.dump(json_data, json_file)

# # # Retrieve PNG file from JSON and save it
# # with open(json_file_path, 'r') as json_file:
# #     retrieved_data = json.load(json_file)
# # catboost_retrieved_base64_data = retrieved_data['catboost_png']
# # lightgbm_retrieved_base64_data = retrieved_data['lightgbm_png']
# # xgboost_retrieved_base64_data = retrieved_data['xgboost_png']
# # catboost_output_png_file_path = './json_outputs/converted_png/catboost_out.png'
# # xgboost_output_png_file_path = './json_outputs/converted_png/xgboost_out.png'
# # lightgbm_output_png_file_path = './json_outputs/converted_png/lightgbm_out.png'
# # decode_base64_to_png(catboost_retrieved_base64_data, catboost_output_png_file_path)
# # decode_base64_to_png(lightgbm_retrieved_base64_data, lightgbm_output_png_file_path)
# # decode_base64_to_png(xgboost_retrieved_base64_data, xgboost_output_png_file_path)
