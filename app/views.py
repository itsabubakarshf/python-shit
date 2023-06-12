import base64
import io
from PIL import Image
import numpy as np
import tensorflow as tf
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.core.files.storage import default_storage
from django.middleware.csrf import get_token
import os
from django.conf import settings


model_path = os.path.join(settings.BASE_DIR, 'static', 'model', 'model.h5')
print(f"Model path: {model_path}")
model = tf.keras.models.load_model(model_path)


def get_csrf_token(request):
    return JsonResponse({'csrfToken': get_token(request)})

def preprocess_image(image):
    image = image.resize((224, 224))  # Resize the image to match the model input size
    image = np.array(image) / 255.0  # Normalize pixel values between 0 and 1
    image = np.expand_dims(image, axis=0)  # Add a batch dimension
    return image

@csrf_exempt
def predict(request):
    if request.method == 'POST':
        if request.FILES['image']:
            # Get the image from the incoming POST request
            image_file = request.FILES['image']
            # Save the file locally temporarily
            file_name = 'temp.jpg'
            file_path = os.path.join(settings.BASE_DIR, file_name)
            with open(file_path, 'wb') as f:
                for chunk in image_file.chunks():
                    f.write(chunk)
            # Open the image file
            image = Image.open(file_path)
            # Preprocess the image
            image = preprocess_image(image)
            # Make a prediction
            prediction = model.predict(image)
            # Calculate the probabilities
            probabilities = prediction.tolist()[0]
            max_probability = max(probabilities)
            # Remove the temporary image file
            os.remove(file_path)
            # Respond with prediction result and probabilities
            response = {
                'prediction': prediction.tolist(),
                'probabilities': probabilities,
                'max_probability': max_probability
            }
            return JsonResponse(response)
        else:
            return JsonResponse({'error': 'No image file provided'}, status=400)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=400)
