from django.shortcuts import render,HttpResponse
import cv2
from mtcnn import MTCNN
import numpy as np

# Create your views here.
recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.read('./jupyter/dataset3.yml')

# Load the MTCNN face detector
detector = MTCNN()
label_dict = {0:"sahil",1:"sans",2:"rut",3:"vaishnavi"}

def register(request):
    return render(request, "main.html")


def authenticate(request):
    if request.method == "POST" and request.FILES['image']:
        name = request.POST.get("name")
        uploaded_image = request.FILES["image"]

        image = cv2.imdecode(np.frombuffer(uploaded_image.read(), np.uint8), cv2.IMREAD_COLOR)
        resize = cv2.resize(image,(500,500))
        faces = detector.detect_faces(resize)
        for face in faces:
            x,y,w,h = face["box"]
            face = image[y:y+h,x:x+w]
            face = cv2.cvtColor(resize, cv2.COLOR_BGR2GRAY)
            face = cv2.cvtColor(resize, cv2.COLOR_BGR2GRAY)
            label,confidence = recognizer.predict(face)
            pname = label_dict.get(label,"unknown")

            if confidence <= 100:
               return HttpResponse (f"{pname} with a confidence of {confidence}")
            else:
                return HttpResponse("unknown")
