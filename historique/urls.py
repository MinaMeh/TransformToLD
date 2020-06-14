from django.conf.urls import url, include
from historique import views


urlpatterns = [

    url(r'^auth/', include('rest_auth.urls')),
    url(r'^auth/google/$', views.GoogleLogin.as_view(), name='google_login'),


    url(r'^api/projects$', views.projects_list),
    url(r'^api/projects/(?P<pk>[0-9]+)$', views.project_details),
]
