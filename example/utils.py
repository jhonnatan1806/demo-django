import spacy
import nltk
import unicodedata
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np



# Descargar stopwords y modelos necesarios
nltk.download('stopwords')
nlp = spacy.load('es_core_news_sm')

# Cargar las stopwords en español de NLTK
stop_words = set(stopwords.words('spanish'))

def preprocess_text(text):
    # 1. Convertir a minúsculas
    text = text.lower()
    
    # 2. Eliminar tildes y acentos
    text = ''.join(
        (c for c in unicodedata.normalize('NFD', text) if unicodedata.category(c) != 'Mn')
    )

    # puede que aca valla el eliminar saltos de linea

    # 3. Tokenizar y lematizar el texto usando spaCy
    doc = nlp(text)
    tokens = []
    
    for token in doc:
        # 4. Eliminar stopwords y caracteres de puntuación
        if token.text not in stop_words and not token.is_punct:
            # 5. Lematizar la palabra
            lemma = token.lemma_
            tokens.append(lemma)
    
    # 6. Combinar el texto resultante
    processed_text = ' '.join(tokens)
    processed_text = processed_text.replace('\n', '')  # Eliminar saltos de línea

    # 7. Dividir el texto en palabras y eliminar cualquier palabra vacía
    split_text = processed_text.split(' ')
    split_text = [word for word in split_text if word != '']
    
    # 8. Reconstruir el texto limpio
    processed_text = ' '.join(split_text)
    
    return processed_text



# Funcion que realiza la similitud de cosenos entre un texto y una lista de textos
def compare_cv_with_jobs(cv_id):
    from .models import CV , JobResult
    try:
        # Obtener el CV específico de la base de datos
        cv = CV.objects.get(id=cv_id)

        # Obtener todos los JobResults de la base de datos
        job_results = JobResult.objects.all()

        # Preparar la lista de descripciones preprocesadas de los trabajos
        job_descriptions = [job.preprocessed_description for job in job_results]

        # Verificar que tanto el CV como las descripciones de trabajos tienen texto preprocesado
        if not cv.preprocessed_text or not any(job_descriptions):
            raise ValueError("Falta texto preprocesado en el CV o en los resultados de trabajos.")

        # Inicializar el vectorizador TF-IDF
        vectorizer = TfidfVectorizer()

        # Ajustar y transformar el texto del CV y los textos de trabajos
        tfidf_texts = vectorizer.fit_transform([cv.preprocessed_text] + job_descriptions)

        # Calcular la similitud de coseno
        cosine_similarities = cosine_similarity(tfidf_texts[0:1], tfidf_texts[1:]).flatten()

        # Asociar cada similitud con su respectivo JobResult
        similarities_with_jobs = list(zip(cosine_similarities, job_results))

        # Ordenar los resultados por mayor similitud
        sorted_similarities = sorted(similarities_with_jobs, key=lambda x: x[0], reverse=True)

        # Devolver los resultados ordenados
        for similarity, job in sorted_similarities:
            print(f"Título: {job.title}, Ubicación: {job.location}, Similitud: {similarity:.2f}")

        return sorted_similarities

    except CV.DoesNotExist:
        print("El CV no existe.")
        return None