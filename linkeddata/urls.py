from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from transformToLD import views
from django.conf.urls import url, include
urlpatterns = [
    path('vocabs/', views.listVocabs),
    path('preprocess/', views.preprocess),

    path('explore/', views.explore),
    path('test/', views.test),
    url(r'^', include('historique.urls'))
]

urlpatterns = format_suffix_patterns(urlpatterns)
