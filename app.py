from flask import Flask, render_template, request, redirect, url_for
from ultralytics import YOLO
import os
import cv2
from werkzeug.utils import secure_filename
from collections import Counter

# Initialize the Flask app
app = Flask(__name__)

# Create a folder named 'static/uploads' to temporarily store uploaded images
UPLOAD_FOLDER = 'static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Load your custom YOLOv8 model weights
model = YOLO("best.pt")

# Define what happens when someone visits the main webpage
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Check if the user actually uploaded a file
        if 'file' not in request.files:
            return redirect(request.url)
        
        file = request.files['file']
        if file.filename == '':
            return redirect(request.url)
            
        if file:
            # Save the uploaded image safely
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            
            # Run the AI model on the uploaded image
            results = model.predict(source=filepath, conf=0.25, save=False)
            
            #Object Counting Logic
            # Get the list of class IDs detected in the image
            detected_classes = results[0].boxes.cls.tolist()
            
            # Count the occurrences of each class ID
            class_counts = Counter(detected_classes)
            
            # Convert class IDs to human-readable names (e.g., 0 -> 'Car', 1 -> 'Bike')
            counts_dict = {}
            for class_id, count in class_counts.items():
                class_name = model.names[int(class_id)].capitalize()
                counts_dict[class_name] = count

            # Draw the bounding boxes on the image
            res_plotted = results[0].plot()
            
            # Save the new image with the bounding boxes drawn on it
            output_filename = 'processed_' + filename
            output_filepath = os.path.join(app.config['UPLOAD_FOLDER'], output_filename)
            cv2.imwrite(output_filepath, res_plotted)
            
            # Generate web links for both the original and processed images
            input_url = url_for('static', filename='uploads/' + filename)
            output_url = url_for('static', filename='uploads/' + output_filename)
            
            # Show the web page template with the images and counts included
            return render_template(
                'index.html', 
                input_image=input_url, 
                output_image=output_url, 
                counts=counts_dict
            )


    return render_template('index.html')

if __name__ == '__main__':
    # Start the local server
    app.run(host='0.0.0.0', port=5000, debug=True)