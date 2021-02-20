from django.shortcuts import render
from django.http import HttpResponse, HttpResponseForbidden
from django.core.files.storage import FileSystemStorage
from .predict import model, predict, df, augment_image


def index(req):
    return render(req, "ai/detect.html")
    
def prediction(req):
    img = req.FILES["filepath"]
    fs = FileSystemStorage()
    f = fs.save(img.name, img)
    imglo = fs.url(f)
    prediction = predict(df, imglo)
    print(prediction)
    return render(req, 'ai/detected.html', {'filepath': imglo, "name" : prediction[0], "symptom" : prediction[1], "remedy" : prediction[2]})
