from flask import Flask, request, jsonify, render_template, send_file
from ultralytics import YOLO
import os
from werkzeug.utils import secure_filename

# Flask app setup
app = Flask(__name__)

# Folder configuration
UPLOAD_FOLDER = 'uploads'
RESULT_FOLDER = 'results'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(RESULT_FOLDER, exist_ok=True)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Load YOLO model (path to your trained model)
model = YOLO('weights/best.pt')

@app.route('/')
def index():
    """Render the main HTML page."""
    return render_template('index.html')

@app.route('/analyze_image', methods=['POST'])
def analyze_image():
    """Endpoint to analyze an uploaded image."""
    file = request.files.get('image')
    if not file:
        return jsonify({'error': 'No image file provided'}), 400

    filename = secure_filename(file.filename)
    filepath = os.path.join(UPLOAD_FOLDER, filename)
    file.save(filepath)

    # Analyze the image with YOLO
    results = model(filepath)
    annotated_image_path = os.path.join(RESULT_FOLDER, f"annotated_{filename}")
    results[0].save(annotated_image_path)  # Saves annotated image automatically

    # Extract counts
    class_counts = {
        'WBC': sum(1 for box in results[0].boxes if box.cls == 1),
        'parasites': sum(1 for box in results[0].boxes if box.cls == 2),
    }

    return jsonify({
        'message': 'Image analyzed successfully.',
        'annotated_image_url': f'/result_image/{os.path.basename(annotated_image_path)}',
        'counts': class_counts
    })


@app.route('/result_image/<filename>')
def result_image(filename):
    """Serve annotated images."""
    return send_file(os.path.join(RESULT_FOLDER, filename))


if __name__ == '__main__':
    app.run(debug=True)