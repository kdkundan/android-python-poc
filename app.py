from flask import Flask, jsonify, request, send_file
from flask_cors import CORS
import os
from utils.video_processor import handle_video_upload, process_video_to_grayscale
from utils.system_info import get_system_info

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Configure upload folder
UPLOAD_FOLDER = 'uploads'
PROCESSED_FOLDER = 'processed'

# Create directories if they don't exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(PROCESSED_FOLDER, exist_ok=True)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['PROCESSED_FOLDER'] = PROCESSED_FOLDER

@app.route('/', methods=['GET'])
def health_check():
    return jsonify({
        "success": True,
        "message": "API is working"
    })

@app.route('/process-video', methods=['POST'])
def process_video():
    # Check if video file is present in request
    if 'video' not in request.files:
        return jsonify({
            'success': False,
            'message': 'No video file provided'
        }), 400
    
    video_file = request.files['video']
    
    # Handle video upload and validation
    success, message, input_path, output_path = handle_video_upload(video_file, app.config)
    if not success:
        return jsonify({
            'success': False,
            'message': message
        }), 400
    
    try:
        # Save the uploaded file
        video_file.save(input_path)
        
        # Process the video
        success, message = process_video_to_grayscale(input_path, output_path)
        
        # Clean up the input file
        os.remove(input_path)
        
        if not success:
            return jsonify({
                'success': False,
                'message': f'Error processing video: {message}'
            }), 500
        
        # Return the processed file
        return send_file(
            output_path,
            as_attachment=True,
            download_name=os.path.basename(output_path),
            mimetype='video/mp4'
        )
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error: {str(e)}'
        }), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)