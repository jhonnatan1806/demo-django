from django.db import models
from .utils import preprocess_text  # Importa la función de preprocesamiento

class CV(models.Model):
    name = models.CharField(max_length=255, verbose_name="Nombre del archivo")
    file = models.FileField(upload_to='cvs/', verbose_name="Archivo PDF")
    upload_date = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de subida")
    extracted_text = models.TextField(blank=True, null=True, verbose_name="Texto extraído")
    preprocessed_text = models.TextField(blank=True, null=True, verbose_name="Texto preprocesado")

    def __str__(self):
        return self.name
    
    class Meta:
        db_table = 'example_cv'

    def save(self, *args, **kwargs):
        # Sobrescribir el método save para extraer el texto del PDF cuando se sube el archivo
        if self.file and not self.extracted_text:
            from PyPDF2 import PdfReader
            pdf_reader = PdfReader(self.file)
            text = ""
            for page in pdf_reader.pages:
                text += page.extract_text() or ""
            self.extracted_text = text

            # Preprocesar el texto extraído
            self.preprocessed_text = preprocess_text(text)
        
        super().save(*args, **kwargs)

class ScrapeResult(models.Model):
    source = models.CharField(max_length=255, verbose_name="Fuente")
    link = models.URLField(verbose_name="Enlace")
    raw_text = models.TextField(verbose_name="Texto Original")
    preprocessed_text = models.TextField(blank=True, null=True, verbose_name="Texto Preprocesado")

    def __str__(self):
        return f"{self.source} - {self.link}"
    
    class Meta:
        db_table = 'scrape_results'
    
    def save(self, *args, **kwargs):
        # Preprocesar el texto scrapeado
        if self.raw_text and not self.preprocessed_text:
            self.preprocessed_text = preprocess_text(self.raw_text)
        
        super().save(*args, **kwargs)