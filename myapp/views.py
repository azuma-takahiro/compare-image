from django.shortcuts import render, redirect
from django.template.context_processors import csrf
from django.conf import settings
from django.http import JsonResponse
from myapp.models import FileModel, ThemeModel, ItemModel
from pprint import pprint

import sys
import os
import random
import string
import cv2

UPLOADE_DIR = os.path.dirname(os.path.abspath(__file__)) + '/static/files/'
IMG_SIZE = (200, 200)


def home(request):
    return render(request, 'home.html')


def theme_form(request):
    if request.method != 'POST':
        return render(request, 'themes/form.html')

    file = request.FILES['file']
    ext = os.path.splitext(file.name)[1]
    filename = random_string(32) + ext
    path = os.path.join(UPLOADE_DIR, filename)
    destination = open(path, 'wb')

    for chunk in file.chunks():
        destination.write(chunk)

    files = FileModel(file_name=filename, original_name=file.name)
    files.save()

    file_id = files.pk

    themes = ThemeModel(file_id=file_id, title=request.POST.get('title', None),
                        comments=request.POST.get('comments', None))
    themes.save()

    return redirect('theme_complete')


def random_string(length, seq=string.digits + string.ascii_lowercase):
    sr = random.SystemRandom()
    return ''.join([sr.choice(seq) for i in range(length)])


def theme_complete(request):
    return render(request, 'themes/complete.html')


def theme_index(request):
    themes = {
        'themes': ThemeModel.objects.all().select_related()
    }
    return render(request, 'themes/index.html', themes)


def upload_file(request):
    if request.method == 'POST':
        file = request.FILES['file']
        ext = os.path.splitext(file.name)[1]
        filename = random_string(32) + ext
        path = os.path.join(UPLOADE_DIR, filename)
        destination = open(path, 'wb')

        for chunk in file.chunks():
            destination.write(chunk)

        files = FileModel(file_name=filename, original_name=file.name)
        files.save()

        return JsonResponse({"file_id": files.pk})


def compare(request, id):
    if request.method == 'GET':
        theme = ThemeModel.objects.all().select_related().filter(id=id).first()
        items = {
            'theme': theme
        }
        return render(request, 'compare/form.html', items)

    elif request.method == 'POST':
        theme = ThemeModel.objects.all().select_related().filter(id=id).first()

        files = FileModel.objects.all().filter(id=request.POST.get('file_id')).first()

        try:
            target_img_path = UPLOADE_DIR + theme.file.file_name
            target_img = cv2.imread(target_img_path)
            target_img = cv2.resize(target_img, IMG_SIZE)

            target_hist = cv2.calcHist(
                [target_img], [0], None, [256], [0, 256])
            bf = cv2.BFMatcher(cv2.NORM_HAMMING)
            detector = cv2.ORB_create()
            (target_kp, target_des) = detector.detectAndCompute(target_img, None)

            comparing_img_path = UPLOADE_DIR + files.file_name
            comparing_img = cv2.imread(comparing_img_path)

            comparing_img = cv2.resize(comparing_img, IMG_SIZE)
            comparing_hist = cv2.calcHist(
                [comparing_img], [0], None, [256], [0, 256])
            (comparing_kp, comparing_des) = detector.detectAndCompute(
                comparing_img, None)
            matches = bf.match(target_des, comparing_des)
            dist = [m.distance for m in matches]
            match = sum(dist) / len(dist)

            hist = cv2.compareHist(target_hist, comparing_hist, 0)

        except cv2.error:
            return render(request, 'errors/error.html')

        items = {
            "ret": round(calcHistTo50(hist) + calcMatchTo50(match), 2),
            "theme_id": id,
            "file_id": files.id
        }

        return render(request, 'compare/compare.html', items)


def calcHistTo50(hist):
    if hist < 0:
        hist = 0
    return round(hist * 50, 2)


def calcMatchTo50(match):
    if match > 100:
        match = 100
    return round(50 - (match / 2), 2)


def theme_delete(request, id):
    ThemeModel.objects.filter(id=id).delete()
    return redirect('theme_index')


def entry(request, id):
    if request.method == "POST":
        file_id = request.POST.get('file_id')
        point = request.POST.get('point')
        name = request.POST.get('name')

        item = ItemModel(file_id=file_id, theme_id=id, point=point, name=name)
        item.save()
        return redirect('ranking', id)
    else:
        return render(request, 'errors/error.html')


def ranking(request, theme_id):
    items = ItemModel.objects.all().select_related().filter(
        theme_id=theme_id).order_by('point').reverse()
    theme = ThemeModel.objects.all().filter(id=theme_id).first()
    return render(request, 'themes/ranking.html', {'items': items, 'theme': theme})


def file_index(request):
    files = FileModel.objects.raw(
        'SELECT f.*, i.name name, i.point point, t.title title, t.comments comments FROM myapp_filemodel as f LEFT JOIN myapp_itemmodel i ON f.id = i.file_id LEFT JOIN myapp_thememodel t ON f.id = t.file_id')

    return render(request, 'files/index.html', {"files": files})


def file_delete(request, id):
    file = FileModel.objects.all().filter(id=id).first()
    path = os.path.join(UPLOADE_DIR, file.file_name)
    if os.path.exists(path):
        os.remove(path)
    FileModel.objects.filter(id=id).delete()
    return redirect('file_index')
