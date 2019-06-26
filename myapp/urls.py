from django.conf.urls import url
from myapp import views
from django.urls import path

urlpatterns = [
    path('', views.home, name='home'),
    path('themes/form/', views.theme_form, name='theme_form'),
    path('themes/complete/', views.theme_complete, name='theme_complete'),
    path('themes/delete/<int:id>', views.theme_delete, name='theme_delete'),
    path('themes/', views.theme_index, name="theme_index"),
    path('compare/<int:id>', views.compare, name="compare"),
    path('themes/entry/<int:id>', views.entry, name="entry"),
    path('ranking/<int:theme_id>', views.ranking, name="ranking"),
    path('files/', views.file_index, name='file_index'),
    path('files/delete/<int:id>', views.file_delete, name="file_delete"),
    path('ajax/upload_file', views.upload_file, name="upload_file")
]
