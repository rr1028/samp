from flask import Flask, render_template, request, redirect, url_for
from werkzeug.utils import secure_filename
import os
from pypdf import PdfReader
import re

app = Flask(__name__)

# Set folder for uploaded files
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Define medical keywords and patterns
medical_keywords = {
    'Blood Pressure': r'\d+/\d+\s*mmHg',  
    'Heart Rate': r'\d+\s*bpm',           
    'Temperature': r'\d+\.?\d*\s*[CF]',   
    'Oxygen Saturation': r'\d+%\s*SpO2',  
    'Cholesterol': r'\d+\s*mg/dL',        
    'Glucose': r'\d+\s*mg/dL',            
    'BMI': r'\d+\.?\d*',                  
    'Weight': r'\d+\.?\d*\s*kg',          
    'Height': r'\d+\.?\d*\s*cm',          
    'Respiratory Rate': r'\d+\s*breaths/min'  
}

# Function to extract medical data from text
def extract_medical_data(text):
    extracted_data = {}
    
    for keyword, pattern in medical_keywords.items():
        full_pattern = rf"{keyword}\s*[:\-]?\s*({pattern})"
        match = re.search(full_pattern, text, re.IGNORECASE)
        if match:
            extracted_data[keyword] = match.group(1)
    
    return extracted_data

# Route for home page
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Check if the post request has the file part
        if 'pdf_file' not in request.files:
            return redirect(request.url)

        pdf_file = request.files['pdf_file']

        if pdf_file.filename == '':
            return redirect(request.url)

        if pdf_file:
            # Save the uploaded file
            filename = secure_filename(pdf_file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            pdf_file.save(filepath)

            # Extract text from the uploaded PDF
            reader = PdfReader(filepath)
            all_extracted_data = {}

            for page_num in range(len(reader.pages)):
                page = reader.pages[page_num]
                text = page.extract_text()
                page_data = extract_medical_data(text)
                all_extracted_data[f'Page {page_num + 1}'] = page_data

            # Pass the extracted data to the template to display
            return render_template('index.html', extracted_data=all_extracted_data)
    
    return render_template('index.html', extracted_data=None)

# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True)
