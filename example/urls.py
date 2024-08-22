# example/urls.py
from django.urls import path

from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('cvs/', views.cv, name='cv_list'),
    path('results/', views.result, name='results'),
    path('upload_cv/', views.upload_cv, name='upload_cv'),
    path('get_cv_text/<int:cv_id>/', views.get_cv_text, name='get_cv_text'),
    path('delete_cv/<int:cv_id>/', views.delete_cv, name='delete_cv'),
]