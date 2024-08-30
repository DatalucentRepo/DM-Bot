from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/your-endpoint', methods=['POST'])
def receive_data():
    data = request.json
    print("Received data:", data)
    
    # Construct the response in the format required by ManyChat
    response = {
        "version": "v2",
        "content": {
            "messages": [
                {
                    "type": "text",
                    "text": "Thank you, we received your message!"
                }
            ],
            "actions": [
                {
                    "action": "add_tag",
                    "tag_name": "giveaway code"
                }
            ]
        }
    }
    
    return jsonify(response), 200

if __name__ == '__main__':
    app.run(debug=True, port=5000)
