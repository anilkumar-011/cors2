from flask import Flask, request, jsonify, render_template
from flask_cors import CORS

app = Flask(__name__)
# CORS(app, origins=["http://localhost:3000"], methods=["GET", "POST", "DELETE","PUT"], allow_headers=["*"])

# flask_cors.cross_origin(
#     origins="http://127.0.0.1:9000/",
#     methods=["GET", "HEAD", "POST", "OPTIONS", "PUT"],
#     headers=None,
#     supports_credentials=False,
#     max_age=None,
#     send_wildcard=True,
#     always_send=True,
#     automatic_options=False,
# )


@app.after_request
def after_request(response):
    # Add custom headers to the response
    response.headers["access-control-allow-methods"] = "DELETE, GET, POST, PUT"
    response.headers["access-control-allow-origin"] = "*"
    response.headers["access-control-allow-headers"] = "Content-Type, Authorization, Anil"
    return response

@app.route("/")
def home():
    return render_template('index.html')

@app.route("/api/data", methods=['GET', 'POST', 'PUT'])
def api_data():
    if request.method == 'GET':
        data = {"message": "Hello, this is your data!", "status": "success"}
        return jsonify(data)

    elif request.method == 'POST':
        incoming_data = request.json
        message = incoming_data.get('message', 'No message received')
        
        response_data = {
            "message": f"Received: {message}",
            "status": "success"
        }
        return jsonify(response_data)

    elif request.method == 'PUT':
        incoming_data = request.json
        message = incoming_data.get('message', 'No message received')
        
        response_data = {
            "message": f"Updated: {message}",
            "status": "success"
        }
        return jsonify(response_data)

@app.route('/api/delete', methods=['DELETE', 'OPTIONS'])
def delete():
    response_data = {
        "message": "Data deleted successfully",
        "status": "success"
    }
    return jsonify(response_data)


if __name__ == "__main__":
    app.run(debug=True)
