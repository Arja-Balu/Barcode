from flask import Flask, request, jsonify
from pyzbar.pyzbar import decode
from PIL import Image
import io
from flask_cors import CORS  # Import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

@app.route('/scan-barcode', methods=['POST'])
def scan_barcode():
    if 'file' not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files['file']
    image = Image.open(io.BytesIO(file.read()))
    barcodes = decode(image)

    if not barcodes:
        return jsonify({"message": "No barcode detected"}), 404

    result = []
    for barcode in barcodes:
        result.append({
            "data": barcode.data.decode("utf-8"),
            "type": barcode.type
        })

    return jsonify({"barcodes": result})

if __name__ == '__main__':
    app.run(debug=True)
