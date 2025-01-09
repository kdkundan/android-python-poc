import cv2
import os
from werkzeug.utils import secure_filename

ALLOWED_EXTENSIONS = {'mp4', 'avi', 'mov', 'mkv'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def process_video_to_grayscale(input_path, output_path):
    try:
        # Open the video file
        cap = cv2.VideoCapture(input_path)
        if not cap.isOpened():
            return False, "Error opening video file"

        # Get video properties
        frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        fps = int(cap.get(cv2.CAP_PROP_FPS))
        
        # Create VideoWriter object
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        out = cv2.VideoWriter(output_path, fourcc, fps, (frame_width, frame_height), False)
        
        while True:
            ret, frame = cap.read()
            if not ret:
                break
                
            # Convert frame to grayscale
            gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            
            # Write the grayscale frame
            out.write(gray_frame)
        
        # Release everything
        cap.release()
        out.release()
        
        return True, "Video processed successfully"
    except Exception as e:
        return False, str(e)

def handle_video_upload(video_file, app_config):
    if video_file.filename == '':
        return False, 'No video file selected', None, None
    
    if not allowed_file(video_file.filename):
        return False, f'File type not allowed. Allowed types: {", ".join(ALLOWED_EXTENSIONS)}', None, None
    
    filename = secure_filename(video_file.filename)
    input_path = os.path.join(app_config['UPLOAD_FOLDER'], filename)
    output_filename = f'gray_{filename}'
    output_path = os.path.join(app_config['PROCESSED_FOLDER'], output_filename)
    
    return True, 'File is valid', input_path, output_path 