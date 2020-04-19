from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from transformToLD import views

urlpatterns = [
    path('vocabs/', views.listVocabs),
    path('preprocess/',views.preprocess),

    path('explore/',views.properties),
    path('test/',views.test)

]

urlpatterns = format_suffix_patterns(urlpatterns)
