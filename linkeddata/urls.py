from django.urls import path
from django.contrib import admin

from django.views.generic import TemplateView

from rest_framework.urlpatterns import format_suffix_patterns
from transformToLD import views
from django.conf.urls import url, include
urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path('', TemplateView.as_view(template_name="index.html")),

    path('extract/', views.extract),
    path('vocabs/', views.listVocabs),
    path('preprocess/', views.preprocess),
    path('explore/', views.explore),
    path('test/', views.test),

    url(r'^', include('historique.urls'))
]

urlpatterns = format_suffix_patterns(urlpatterns)
