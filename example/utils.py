import spacy
import nltk
import unicodedata
from nltk.corpus import stopwords

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
