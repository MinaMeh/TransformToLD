from django.conf.urls import url, include
from historique import views
from .views import check_token

urlpatterns = [
    url(r'^api/projects$', views.projects_list),
    url(r'^api/projects/(?P<pk>[0-9]+)$', views.project_details),

    url(r'^api/login/', include('rest_social_auth.urls_jwt')),
    url(r'^api/login/', include('rest_social_auth.urls_token')),
    url(r'^api/login/', include('rest_social_auth.urls_session')),
    url(r'^auth/', include('rest_framework_social_oauth2.urls')),
    url(r'api/check/', check_token),

]
