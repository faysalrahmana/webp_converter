from flask import Flask, render_template, request, redirect, url_for, send_file
from PIL import Image
import os

# ... the rest of the code ...


app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def convert_to_webp(input_image_path, output_image_path, quality=80):
    try:
        # Open the input image
        img = Image.open(input_image_path)

        # Convert to WebP format and save with specified quality
        img.save(output_image_path, format='WebP', quality=quality, method=6)
        return True
    except Exception as e:
        print(f"Error occurred: {e}")
        return False

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'image' not in request.files:
            return redirect(request.url)

        image = request.files['image']
        if image.filename == '':
            return redirect(request.url)

        if image:
            image_path = os.path.join(app.config['UPLOAD_FOLDER'], image.filename)
            image.save(image_path)

            webp_image_path = os.path.join(app.config['UPLOAD_FOLDER'], 'converted.webp')
            success = convert_to_webp(image_path, webp_image_path)

            if success:
                return render_template('result.html', image_path=webp_image_path)

    return render_template('index.html')

@app.route('/download/<filename>', methods=['GET'])
def download(filename):
    return send_file(os.path.join(app.config['UPLOAD_FOLDER'], filename), as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
