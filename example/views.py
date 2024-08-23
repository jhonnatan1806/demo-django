from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import CV
from django.http import JsonResponse
from .utils import preprocess_text  # Importa la función desde utils.py

def index(request):
    cvs = CV.objects.all()  # Obtener todos los CVs guardados
    return render(request, 'index.html', {'cvs': cvs})

def cv(request):
    return render(request, 'cvs.html')

def result(request):
    return render(request, 'results.html')

def upload_cv(request):
    if request.method == 'POST' and 'cv' in request.FILES:
        cv_file = request.FILES['cv']
        
        # Validar tipo de archivo
        if not cv_file.name.endswith('.pdf'):
            messages.error(request, "El archivo debe estar en formato PDF.")
            return redirect('index')

        # Validar tamaño de archivo (por ejemplo, máximo 2MB)
        # if cv_file.size > 2 * 1024 * 1024:  # 2MB
        #     messages.error(request, "El archivo es demasiado grande. El tamaño máximo es de 2MB.")
        #     return redirect('index')

        # Crear una instancia del modelo CV
        cv = CV(name=cv_file.name, file=cv_file)
        cv.save()  # Aquí se guarda el archivo y se extrae el texto automáticamente

        # Redirigir al index con el CV recién subido
        return redirect('index')

    return redirect('index')

def get_cv_text(request, cv_id):
    cv = CV.objects.get(id=cv_id)
    return JsonResponse({'text': cv.preprocessed_text})

def delete_cv(request, cv_id):
    cv = get_object_or_404(CV, id=cv_id)
    if request.method == 'POST':
        cv.delete()
        messages.success(request, f'El archivo {cv.name} ha sido eliminado.')
        return redirect('index')
    


