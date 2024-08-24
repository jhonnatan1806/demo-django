import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import os
from api.settings import BASE_DIR
from .models import JobResult

# Rutas y URLs de ejemplo

path_driver = os.path.join(BASE_DIR, 'driver', 'chromedriver.exe')

    # Diccionario de URLs para las plataformas
urls = {
        'indeed': 'https://pe.indeed.com/?from=gnav-compui',
        'bumeran': 'https://www.bumeran.com.pe/empleos-busqueda-web.html'
    }

class JobScraper:
    def __init__(self, base_urls= urls, driver_path = path_driver):
        service = Service(executable_path=driver_path)
        self.driver = webdriver.Chrome(service=service)
        self.base_urls = base_urls
    
    def scrape_indeed(self, text_input):
        self.driver.get(self.base_urls['indeed'])

        # Buscamos el input de búsqueda
        search_input = self.driver.find_element(By.XPATH, '//*[@id="text-input-what"]')

        # Escribimos la búsqueda
        search_input.send_keys(text_input)
        search_input.send_keys(Keys.ENTER)
        time.sleep(2)

        # Obtenemos los resultados
        postulaciones = self.driver.find_elements(By.CLASS_NAME, 'css-5lfssm.eu4oa1w0')

        # Inicializamos las listas para almacenar la información
        titulos, sueldos, tipo_empleos, ubicaciones, descripciones , links_postulacion = [], [], [], [], [],[]

        for i in range(1, 20):
            try:
                postulacion = self.driver.find_element(By.XPATH, f'/html/body/main/div/div[2]/div/div[5]/div/div[1]/div[5]/div/ul/li[{i}]/div')
                postulacion.click()
                time.sleep(2)

                # Obtenemos el título
                try:
                    titulo = self.driver.find_element(By.XPATH, '//*[@id="jobsearch-ViewjobPaneWrapper"]/div/div[2]/div[2]/div[1]/div/div[1]/div[1]/h2/span').text
                    titulo = titulo.split('\n')[0]
                except:
                    titulo = "No especificado"
                titulos.append(titulo)
                
                # Obtenemos el sueldo
                try:
                    X_path = '//*[@id="jobDetailsSection"]/div/div[1]/div[2]/div[1]/div/div/ul/li/div/div/div[1]'
                    sueldo = self.driver.find_element(By.XPATH, X_path).text
                except:
                    sueldo = "No especificado"
                sueldos.append(sueldo)

                # Obtenemos el tipo de empleo
                try:
                    tipo_empleo = self.driver.find_element(By.XPATH, '//*[@id="jobDetailsSection"]/div/div[1]/div[2]/div[2]/div/div/ul/li/div/div/div[1]').text
                except:
                    tipo_empleo = "No especificado"
                tipo_empleos.append(tipo_empleo)

                # Obtenemos la ubicación
                try:
                    ubicacion = self.driver.find_element(By.XPATH, '//*[@id="jobLocationText"]/div/span').text
                except:
                    ubicacion = "No especificado"
                ubicaciones.append(ubicacion)

                # Obtenemos la descripción
                try:
                    descripcion = self.driver.find_element(By.XPATH, '//*[@id="jobDescriptionText"]').text
                except:
                    descripcion = "No especificado"
                descripciones.append(descripcion)

                try:
                    link_postulacion = self.driver.current_url
                except:
                    link_postulacion = "No especificado"
                links_postulacion.append(link_postulacion)

                
                job_result = JobResult(
                                title=titulo,
                                salary=sueldo,
                                employment_type=tipo_empleo,
                                location=ubicacion,
                                description=descripcion,
                                link=link_postulacion
                            )
                job_result.save()  # Aquí se guarda la instancia en la base de datos.


            except Exception as e:
                continue

    
    def close_driver(self):
        self.driver.quit()