import streamlit as st
from keras.models import load_model
from keras.preprocessing.image import img_to_array
import numpy as np
from PIL import Image

# Load model
try:
    model = load_model('model/Fruit.h5')
    st.success("Model loaded successfully.")
except Exception as e:
    st.error(f"Error loading model: {e}")
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
        st.error(f"Error preprocessing image: {e}")
        return None

st.title("Fruit Classification")
uploaded_file = st.file_uploader("Choose an image...", type="jpg")

if uploaded_file is not None:
    img = Image.open(uploaded_file)
    st.image(img, caption='Uploaded Image.', use_column_width=True)
    st.write("")
    st.write("Classifying...")
    image_array = preprocess_image(img)

    if model is not None and image_array is not None:
        predictions = model.predict(image_array)
        confidence = float(np.max(predictions))  # Confidence should be between 0 and 1
        predicted_class = class_names[np.argmax(predictions)]
        st.write(f"Prediction: {predicted_class}")
        st.write(f"Confidence: {round(confidence*100, 2)}%")
