# Generated by Django 4.1.3 on 2024-08-22 05:15

from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="CV",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "name",
                    models.CharField(max_length=255, verbose_name="Nombre del archivo"),
                ),
                (
                    "file",
                    models.FileField(upload_to="cvs/", verbose_name="Archivo PDF"),
                ),
                (
                    "upload_date",
                    models.DateTimeField(
                        auto_now_add=True, verbose_name="Fecha de subida"
                    ),
                ),
                (
                    "extracted_text",
                    models.TextField(
                        blank=True, null=True, verbose_name="Texto extraído"
                    ),
                ),
            ],
            options={
                "db_table": "example_cv",
            },
        ),
    ]
