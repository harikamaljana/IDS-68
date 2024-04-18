# from flask import Flask, render_template, jsonify, request
# import subprocess

# app = Flask(__name__)

# @app.route('/')
# def home():
#     return render_template('frontend.html')

# @app.route('/run-model', methods=['POST'])
# def run_model():
#     try:
#         print('running script hehe')
#         # Execute the Python script
#         result = subprocess.run(['python', 'LCCDE_IDS_GlobeCom22.py'], capture_output=True, text=True)

        

#         if result.returncode == 0:
#             # Script executed successfully
#             print("script runs")
#             output = result.stdout
#             return jsonify({'output': output}), 200
#         else:
#             # Error occurred while executing the script
#             error = result.stderr
#             return jsonify({'error': error}), 500
#     except Exception as e:
#         return jsonify({'error': str(e)}), 500

# if __name__ == '__main__':
#     app.run(debug=True)


from flask import Flask, render_template, jsonify, request, send_file
import subprocess
import os
import base64

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('frontend.html')

@app.route('/run-model', methods=['POST'])
def run_model():
    try:
        # Execute the Python script
        result = subprocess.run(['python3', 'LCCDE_IDS_GlobeCom22.py'], capture_output=True, text=True)

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
    

if __name__ == '__main__':
    app.run(debug=True)
