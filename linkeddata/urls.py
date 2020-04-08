from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from transformToLD import views

urlpatterns = [
    path('vocabs/', views.listVocabs),
    path('preprocess/',views.properties),

    path('explore/',views.properties)
]

urlpatterns = format_suffix_patterns(urlpatterns)
