from django.conf.urls import url
from historique import views
from django.urls import path, include
from django.views.generic import TemplateView

urlpatterns = [

    #url(r'^auth/', include('rest_auth.urls')),
    #url(r'^auth/google/$', views.GoogleLogin.as_view(), name='google_login'),

    path('accounts/', include('allauth.urls')),
    path('', TemplateView.as_view(template_name='index.html')),


    url(r'^api/projects$', views.projects_list),
    url(r'^api/projects/(?P<pk>[0-9]+)$', views.project_details),
]
