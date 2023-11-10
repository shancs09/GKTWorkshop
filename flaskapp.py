import os
from flask import Flask, request, jsonify
from llmservice_cloud_wx import generate_campaign
from ibm_cloud_wd import query_discovery
from ibm_cloud_wa import chat_with_assistant
app = Flask(__name__)

@app.route('/generate_campaign', methods=['POST'])
def generate_campaign_route():
    try:
        data = request.get_json()
        print(data)
        doc_text = data.get("text")
        if "temp" in data:
            temp=data.get("temp")
        else:
            temp=0
    except Exception as e:
        print("Error decoding JSON:", str(e))
    print(doc_text)
    print(temp)
    result = generate_campaign(doc_text,temp)
    return jsonify({'result': result})


@app.route('/query_discovery', methods=['POST'])
def query_discover_1():
    try:
        data = request.get_json()
        print(data)
        doc_text = data.get("text")
    except Exception as e:
        print("Error decoding JSON:", str(e))
    print(doc_text)
    result = query_discovery(doc_text)
    # return result
    return jsonify({'result': result})


@app.route('/chat_assistant', methods=['POST'])
def chat_assistant():
    try:
        data = request.get_json()
        print(data)
        doc_text = data.get("text")
    except Exception as e:
        print("Error decoding JSON:", str(e))
    print(doc_text)
    result = chat_with_assistant(doc_text)
    # return result
    return result


if __name__ == '__main__':
    # Get the port from the PORT environment variable or use a default value of 8080
    port = int(os.environ.get('PORT', 8080))
    # Run the Flask application with the specified port
    app.run(debug=True, host='0.0.0.0', port=port)
