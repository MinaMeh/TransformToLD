from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from transformToLD import views
from django.conf.urls import url, include
urlpatterns = [
    path('extract/', views.extract),
    path('vocabs/', views.listVocabs),
    path('preprocess/', views.preprocess),
    path('explore/', views.explore),
    path('vocabs/', views.select_vocabs),
    path('convert/', views.convert),

    path('test/', views.test),
    path('searchProperty/', views.search_property),
    url(r'^', include('historique.urls'))
]

urlpatterns = format_suffix_patterns(urlpatterns)
