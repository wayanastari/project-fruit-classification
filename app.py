from flask import flask, request, render_template, jsonify
from keras.models import load_model
from keras.preprocessing.image import img_to_array, load_img
import numpy as np
from PIL import Image

app = Flask(__name__)

# Load model
try:
    model = load_model('model/Fruit.h5')
    print("Model loaded successfully.")
except Exception as e:
    print("Error loading model:", e)
    model = None

class_names = ['apple',
                'avocado',
                'banana',
                'bearberry',
                'bilimbi',
                'blackberry',
                'blueberry',
                'carambola',
                'cempedak',
                'cherry',
                'chico',
                'coconut',
                'dragonfruit',
                'durian',
                'grape',
                'kiwi',
                'lemon',
                'papaya',
                'rambutan',
                'strawberry']

def preprocess_image(image, target_size=(256, 256)):
    try:
        image = image.resize(target_size)
        image = img_to_array(image) / 255.0
        image = np.expand_dims(image, axis=0)
        return image
    except Exception as e:
        print("Error preprocessing image:", e)
        return None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    try:
        file = request.files['file']
        if not file:
            return jsonify({"error": "No file provided"}), 400

        img = Image.open(file.stream)
        image_array = preprocess_image(img)

        if model is None:
            return jsonify({"error": "Model not loaded"}), 500

        predictions = model.predict(image_array)
        confidence = float(np.max(predictions))  # Ini seharusnya antara 0 dan 1
        predicted_class = class_names[np.argmax(predictions)]

        return jsonify({
            "class": predicted_class,
            "confidence": round(confidence, 2)  # Kalikan dengan 100 untuk mendapatkan persentase
        })

    except Exception as e:
        print(f"Error during prediction: {e}")
        return jsonify({"error": "Error during prediction"}), 500



if __name__ == '__main__':
    app.run(debug=True)
