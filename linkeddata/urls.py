
from django.contrib import admin
from django.urls import path
from transformToLD import views
urlpatterns = [
    path('admin/', admin.site.urls),
    path ('',views.file_upload,name="file_upload")
]
