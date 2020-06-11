from django.conf.urls import url
from historique import views
'''from .views import check_token'''

urlpatterns = [
    url(r'^api/projects$', views.projects_list),
    url(r'^api/projects/(?P<pk>[0-9]+)$', views.project_details),
]
