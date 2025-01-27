from flask import Flask, request, jsonify, render_template, g
import base64
import secrets, os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = './uploads'  # Define your upload folder

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
    response.headers["access-control-allow-headers"] = "content-type"

    # Generate nonces
    nonce = base64.b64encode(secrets.token_bytes(16)).decode("utf-8")
    css_nonce = base64.b64encode(secrets.token_bytes(16)).decode("utf-8")
    
    # Store nonces in Flask's `g` object for access in templates
    g.script_nonce = nonce
    g.style_nonce = css_nonce

    # Add CSP header
    response.headers["content-security-policy"] = f"script-src 'nonce-{nonce}'; style-src 'nonce-{css_nonce}';"

    return response


@app.route("/")
def home():
    script_nonce = getattr(g, 'script_nonce', '')
    style_nonce = getattr(g, 'style_nonce', '')
    return render_template('index.html', script_nonce=script_nonce, style_nonce=style_nonce)


@app.route("/api/data", methods=['GET', 'POST', 'PUT'])
def api_data():
    if request.method == 'GET':
        data = {"message": "Hello, this is your data!", "status": "success", "requestorigin":request.headers.get('Origin')}
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

@app.route('/multipart')
def index():
    return render_template('form.html')

@app.route('/submit', methods=['POST'])
def submit_form():
    # Get text input
    username = request.form.get('username')
    
    # Get uploaded file
    uploaded_file = request.files.get('file')
    
    if uploaded_file:
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], uploaded_file.filename)
        uploaded_file.save(file_path)
        return f"File uploaded to {file_path}, Username: {username}"
    
    return "No file uploaded or username missing!"

if __name__ == "__main__":
    app.run(debug=True)
