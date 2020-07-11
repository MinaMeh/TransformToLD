from django.conf.urls import url, include
from rest_framework_jwt.views import obtain_jwt_token, refresh_jwt_token

from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from transformToLD import views
from django.contrib import admin
admin.autodiscover()


urlpatterns = [
    url(r'^admin/', admin.site.urls),

    path('extract/', views.extract),
    path('vocabs/', views.listVocabs),
    path('preprocess/', views.preprocess),
    path('explore/', views.explore),
    path('vocabs/', views.select_vocabs),
    path('convert/', views.convert),
    path('document/', views.document),
    path('translate/', views.rdf_translate),
    path('api/token/', obtain_jwt_token, name='token_obtain_pair'),
    path('api/token/refresh/', refresh_jwt_token, name='token_refresh'),
    path('register/', views.register),
    path('getFile/', views.get_file),
    path('searchProperty/', views.search_property),
    path('searchClass/', views.search_class),
    path('createProperty/', views.create_property),
    path('createClass/', views.create_class),

    url(r'^', include('historique.urls'))
]

urlpatterns = format_suffix_patterns(urlpatterns)
