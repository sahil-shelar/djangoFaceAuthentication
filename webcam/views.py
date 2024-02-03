# views.py
import os
import datetime
import cv2
import face_recognition
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings

registered_data = {}

def index(request):
    return render(request, 'index.html')

@csrf_exempt
def register(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        photo = request.FILES['photo']

        uploads_folder = os.path.join(settings.BASE_DIR, 'static', 'uploads')
        if not os.path.exists(uploads_folder):
            os.makedirs(uploads_folder)

        photo_path = os.path.join(uploads_folder, f'{datetime.date.today()}_{name}.jpg')
        with open(photo_path, 'wb') as destination:
            for chunk in photo.chunks():
                destination.write(chunk)

        registered_data[name] = f'{datetime.date.today()}_{name}.jpg'

        response = {'success': True, 'name': name}
        return JsonResponse(response)

@csrf_exempt
def login(request):
    if request.method == 'POST':
        photo = request.FILES['photo']

        uploads_folder = os.path.join(settings.BASE_DIR, 'static', 'uploads')
        if not os.path.exists(uploads_folder):
            os.makedirs(uploads_folder)

        login_filename = os.path.join(uploads_folder, 'login_face.jpg')
        with open(login_filename, 'wb') as destination:
            for chunk in photo.chunks():
                destination.write(chunk)

        login_image = cv2.imread(login_filename)
        gray_image = cv2.cvtColor(login_image, cv2.COLOR_BGR2GRAY)

        face_cascade = cv2.CascadeClassifier(os.path.join(settings.BASE_DIR, 'Haarcascades/haarcascade_frontalface_default.xml'))
        faces = face_cascade.detectMultiScale(gray_image, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

        if len(faces) == 0:
            response = {'success': False}
            return JsonResponse(response)

        login_image = face_recognition.load_image_file(login_filename)
        login_face_encodings = face_recognition.face_encodings(login_image)

        for name, filename in registered_data.items():
            registered_photo = os.path.join(uploads_folder, filename)
            registered_image = face_recognition.load_image_file(registered_photo)
            registered_face_encodings = face_recognition.face_encodings(registered_image)

            if len(registered_face_encodings) > 0 and len(login_face_encodings) > 0:
                matches = face_recognition.compare_faces(registered_face_encodings, login_face_encodings[0])

                if any(matches):
                    response = {'success': True, 'name': name}
                    return JsonResponse(response)

        response = {'success': False}
        return JsonResponse(response)

def success(request):
    user_name = request.GET.get('user_name')
    return render(request, 'success.html', {'user_name': user_name})
