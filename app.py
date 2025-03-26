from flask import Flask, request, jsonify
import time

app = Flask(__name__)

@app.route('/process', methods=['POST'])
def process_data():
    start_time = time.time()
    
    data = request.get_json()
    # Simulated processing
    result = {"status": "processed", "data": data}
    
    end_time = time.time()
    response_time = end_time - start_time
    
    return jsonify({"response_time": response_time, "result": result})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
