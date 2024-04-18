import json
import base64

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
json_file_path = './lccde_images.json';

# Encode PNG file to base64 and store in JSON format
png_base64_data = encode_png_to_base64(png_file_path)
json_data = {'png_data': png_base64_data}
with open(json_file_path, 'w') as json_file:
    json.dump(json_data, json_file)

# Retrieve PNG file from JSON and save it
with open(json_file_path, 'r') as json_file:
    retrieved_data = json.load(json_file)
retrieved_base64_data = retrieved_data['png_data']
output_png_file_path = 'retrieved.png'
decode_base64_to_png(retrieved_base64_data, output_png_file_path)
