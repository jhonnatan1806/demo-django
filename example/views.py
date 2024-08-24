from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import CV, JobResult
from django.http import JsonResponse
from .utils import preprocess_text  # Importa la función desde utils.py
from .webscrapping import JobScraper
from .utils import compare_cv_with_jobs

def index(request):
    cvs = CV.objects.all()  # Obtener todos los CVs guardados
    job_results = []  # Inicializar una lista para almacenar los resultados de trabajos
    best_matches = []  # Inicializar una lista para los mejores resultados de similitud

    if request.method == 'POST':
        if 'compare' in request.POST:
            # Si se ha enviado la solicitud de comparación
            selected_cv_id = request.POST.get('selected_cv')
            best_matches = compare_cv_with_jobs(selected_cv_id)[:3]  # Obtener los 3 mejores resultados

        else:
            # Obtener los datos del formulario para scraping
            selected_pages = request.POST.getlist('pages')
            search_term = request.POST.get('search_term')

            if not selected_pages or not search_term:
                messages.error(request, "Debes seleccionar al menos una página y proporcionar un término de búsqueda.")
                return redirect('index')

            # Ejecutar el scraping
            scraper = JobScraper()
            for page in selected_pages:
                if page == 'indeed':
                    scraper.scrape_indeed(search_term)
                # Aquí puedes agregar lógica para otras plataformas (LinkedIn, Glassdoor, etc.)

            scraper.close_driver()

            # Obtener los resultados del scraping desde la base de datos
            job_results = JobResult.objects.all()

    return render(request, 'index.html', {'cvs': cvs, 'job_results': job_results, 'best_matches': best_matches})

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
    


