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


from flask import Flask, render_template, jsonify, request
import subprocess

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
            return jsonify({'output': output}), 200
        else:
            # Error occurred while executing the script
            error = result.stderr
            return jsonify({'error': error}), 500
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)