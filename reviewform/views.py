from PIL import UnidentifiedImageError
from django.shortcuts import render, redirect

from reviewform.forms import *
from reviewform.models import *


def add_problem(request):
    if request.method == 'POST':
        form = AddProblemForm(request.POST, request.FILES)
        if form.is_valid():
            problem = form.save()
            images = form.cleaned_data["image_field"]
            try:
                for image in images:
                    Image.objects.create(problem=problem, image=image)
                return redirect('success')
            except UnidentifiedImageError:
                form.add_error('image_field', 'Ошибка добавления фото')
    else:
        form = AddProblemForm()

    context = {
        'title': 'Описание проблемы',
        'form': form,
    }

    return render(request, 'reviewform/add_problem.html', context)


def success(request):
    return render(request, 'reviewform/success.html')
