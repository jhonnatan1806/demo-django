from django.db import models

class CV(models.Model):
    name = models.CharField(max_length=255, verbose_name="Nombre del archivo")
    file = models.FileField(upload_to='cvs/', verbose_name="Archivo PDF")
    upload_date = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de subida")
    extracted_text = models.TextField(blank=True, null=True, verbose_name="Texto extraído")

    def __str__(self):
        return self.name
    
    class Meta:
        db_table = 'example_cv'  # Nombre de la tabla en la base de datos

    def save(self, *args, **kwargs):
        # Sobrescribir el método save para extraer el texto del PDF cuando se sube el archivo
        if self.file and not self.extracted_text:
            from PyPDF2 import PdfReader
            pdf_reader = PdfReader(self.file)
            text = ""
            for page in pdf_reader.pages:
                text += page.extract_text() or ""
            self.extracted_text = text
        super().save(*args, **kwargs)
