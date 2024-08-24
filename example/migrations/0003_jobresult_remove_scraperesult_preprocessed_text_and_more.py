# Generated by Django 4.1.3 on 2024-08-24 02:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("example", "0002_scraperesult_cv_preprocessed_text"),
    ]

    operations = [
        migrations.CreateModel(
            name="JobResult",
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
                ("title", models.CharField(max_length=255, verbose_name="Título")),
                ("salary", models.CharField(max_length=100, verbose_name="Sueldo")),
                (
                    "employment_type",
                    models.CharField(max_length=100, verbose_name="Tipo de empleo"),
                ),
                (
                    "location",
                    models.CharField(max_length=255, verbose_name="Ubicación"),
                ),
                ("description", models.TextField(verbose_name="Descripción")),
                (
                    "preprocessed_description",
                    models.TextField(
                        blank=True, null=True, verbose_name="Descripción Preprocesada"
                    ),
                ),
            ],
            options={
                "db_table": "job_results",
            },
        ),
        migrations.RemoveField(
            model_name="scraperesult",
            name="preprocessed_text",
        ),
        migrations.RemoveField(
            model_name="scraperesult",
            name="raw_text",
        ),
        migrations.AddField(
            model_name="scraperesult",
            name="job_result",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="scrape_results",
                to="example.jobresult",
                verbose_name="Resultado de Empleo",
            ),
        ),
    ]
