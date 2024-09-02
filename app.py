from flask import Flask, render_template, request, redirect, url_for
import easyocr
import pytesseract
import os

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Ensure the upload folder exists
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

def extract_text_easyocr(image_path):
    reader = easyocr.Reader(['en'])
    result = reader.readtext(image_path)
    return " ".join([res[1] for res in result])

def extract_text_tesseract(image_path):
    return pytesseract.image_to_string(image_path)

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['file']
        if file:
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(filepath)

            # Choose OCR method (you can add more methods)
            method = request.form.get('method', 'easyocr')
            if method == 'tesseract':
                extracted_text = extract_text_tesseract(filepath)
            else:
                extracted_text = extract_text_easyocr(filepath)

            return render_template('result.html', text=extracted_text)

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
