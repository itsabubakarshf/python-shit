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


@csrf_exempt
def predict(request):
    if request.method == 'POST':
        if request.FILES.get('file'):
            # Get the image from the incoming POST request
            # image_file = request.FILES['file']
            # data = request.data
            # kind = data['kind']

            # if kind == 'upload':
            image_file = request.FILES.get('file')  # Access the uploaded file
            # kind = request.POST.get('kind')  # Access the 'kind' field
            file_name = 'temp.jpg'
            file_path = os.path.join(settings.STATIC_ROOT, file_name)
            
            with open(file_path, 'wb') as f:
                for chunk in image_file.chunks():
                    f.write(chunk)

            # else:
            #     print('camera inside')
            #     format, imgstr = image_file.split(';base64,') 
            #     ext = format.split('/')[-1] 
            #     data = base64.b64decode(imgstr)

            #     filename = os.path.join(settings.STATIC_ROOT, 'temp.' + ext)
            #     with open(filename, 'wb') as f:
            #         f.write(data)

            # Open the image file
            image = Image.open(file_path)
            # Preprocess the image
            image = preprocess_image(image)
            # Make a prediction
            prediction = model.predict(image)


            predicted_class_indices = np.argmax(prediction, axis=1)

            index = ['0.5', 'Healthy', '0.10', 'Healthy','0.52', 'Healthy','0.65', 'Healthy', '0.89', 'Healthy','0.99', 'Healthy','1.2', 'Healthy','1.5', 'Healthy','1.66', 'Healthy','1.76', 'Healthy','2', 'Healthy' ]

            sorted_indices = np.argsort(prediction[0])[::-1] 

            new_index = index[sorted_indices[predicted_class_indices[0]]]
            healthy_or_deficiency = 'Healthy'
            deficiency_percent = 0.0
            if new_index != 'Healthy':
                healthy_or_deficiency = 'Deficiency'
                deficiency_percent = new_index

            os.remove(file_path)

            response = {
                'healthy_or_deficiency': healthy_or_deficiency,
                'deficiency_percent': float(deficiency_percent),
                'file_path': file_path
            }

            return JsonResponse(response, safe=False)
        
        else:
            return JsonResponse({'error': 'No image file provided'}, status=400)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=400)
