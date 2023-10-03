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
import json


model_path = os.path.join(settings.BASE_DIR, 'static', 'model', 'model.h5')
print(f"Model path: {model_path}")
model = tf.keras.models.load_model(model_path)
# model = None

def get_csrf_token(request):
    return JsonResponse({'csrfToken': get_token(request)})

def preprocess_image(image):
    image = image.resize((224, 224))  # Resize the image to match the model input size
    image = np.array(image) / 255.0  # Normalize pixel values between 0 and 1
    image = np.expand_dims(image, axis=0)  # Add a batch dimension
    return image

import base64


from PIL import Image

@csrf_exempt
def predict(request):
    try:
        if request.method == 'POST':
            if request.FILES.get('file'):
                print("Received an image for prediction")
                
                image_file = request.FILES.get('file')
                file_name = 'temp.jpg'
                file_path = os.path.join(settings.STATIC_ROOT, file_name)

                # Check if the image is not a JPG and convert if needed
                im = Image.open(image_file)
                if im.format != "JPEG":
                    print(f"Image format is {im.format}. Converting to JPG.")
                    im = im.convert('RGB')  # Ensure image has 3 channels
                    im.save(file_path, "JPEG")
                else:
                    with open(file_path, 'wb') as f:
                        for chunk in image_file.chunks():
                            f.write(chunk)
                
                print("Saved image to:", file_path)

                image = Image.open(file_path)
                image = preprocess_image(image)
                print("Preprocessed the image")

                prediction = model.predict(image)
                print("Prediction completed")
                
                predicted_class_indices = np.argmax(prediction, axis=1)
                index = ['0.5', 'Healthy', '0.10', 'Healthy', '0.52', 'Healthy', '0.65', 'Healthy', '0.89', 'Healthy', '0.99', 'Healthy', '1.2', 'Healthy', '1.5', 'Healthy', '1.66', 'Healthy', '1.76', 'Healthy', '2', 'Healthy']
                
                sorted_indices = np.argsort(prediction[0])[::-1]
                new_index = index[sorted_indices[predicted_class_indices[0]]]
                
                healthy_or_deficiency = 'Healthy'
                deficiency_percent = 0.0
                if new_index != 'Healthy':
                    healthy_or_deficiency = 'Deficiency'
                    deficiency_percent = new_index

                os.remove(file_path)
                print("Temp image file removed")

                response = {
                    'healthy_or_deficiency': healthy_or_deficiency,
                    'deficiency_percent': float(deficiency_percent),
                    'file_path': file_path
                }

                print("Sending response:", response)
                return JsonResponse(response, safe=False)
            
            else:
                print("Error: No image file provided")
                return JsonResponse({'error': 'No image file provided'}, status=400)
        
        else:
            print("Error: Invalid request method")
            return JsonResponse({'error': 'Invalid request method'}, status=400)
    
    except Exception as e:
        print("Exception encountered:", e)
        return JsonResponse({'error': 'Server Error'}, status=500)
