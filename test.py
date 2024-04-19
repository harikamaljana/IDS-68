import json
import os
import base64
# if (model == 'lccde'):
#     filenames = ['CatBoost.png', 'lightGBM.png', 'XGBoost.png']
# elif (model == 'tree'):
filenames = ['TB_DecisionTree.png', 'TB_ExtraTrees.png', 'TB_FS_DecisionTree.png', 'TB_FS_ExtraTrees.png', 'TB_FS_RandomForest.png', 'TB_FS_StackModel.png', 'TB_FS_XGB.png', 'TB_RandomForest.png', 'TB_StackModel.png', 'TB_XGB.png']
# else:
#     filenames = []
    
files_directory = './heatmaps/'
file_list = os.listdir(files_directory)
base64dataImagesJson = {}

print('WORKING - WITH UPDATES TO BASE')

def encode_png_to_base64(file_path):
    with open(file_path, 'rb') as file:
        png_data = file.read()
        return base64.b64encode(png_data).decode('utf-8')

# for name in filenames:
for f in file_list:
    if f in filenames:
        # base64dataImagesJson = json.loads(base64dataImagesJson)
        base64dataImagesJson[f] = encode_png_to_base64(files_directory+f)
        # base64dataImagesJson = json.dumps(base64dataImagesJson)
        if os.path.isfile(files_directory+f):
            os.remove(files_directory+f)
        
# # Example usage
# catboost_png_file_path = './heatmaps/CatBoost.png';
# lightgbm_png_file_path = './heatmaps/lightGBM.png';
# xgboost_png_file_path = './heatmaps/XGBoost.png';
# # json_file_path = './json_outputs/lccde_images.json';

# # Encode PNG file to base64 and store in JSON format
# catboost_png_base64_data = encode_png_to_base64(catboost_png_file_path)
# lightgbm_png_base64_data = encode_png_to_base64(lightgbm_png_file_path)
# xgboost_png_base64_data = encode_png_to_base64(xgboost_png_file_path)
    
# images_ref = db.collection('Algorithm').document(storage_id)

# # # for f in file_list:
# # #     file_path = os.path.join(files_directory, f)
# # #     if os.path.isfile(file_path):
# # #         os.remove(file_path)
        
# images_ref.update({
#     'images': outputJson
#     # {
#     #     'catboost_png': catboost_png_base64_data,
#     #     'lightgbm_png': lightgbm_png_base64_data,
#     #     'xgboost_png': xgboost_png_base64_data
#     # }
# })

print('done working' + json.dumps(base64dataImagesJson))

# if __name__ == '__main__':
# app.run(debug=True)
