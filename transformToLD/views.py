from django.shortcuts import render
from django.http import HttpResponse
from .forms import *
from .trait_files import *
from .searchTerms import getTerm,getVocab
import pandas as pd
import csv
import io
from django.conf import settings
from django.core.files.storage import FileSystemStorage
# Create your views here.
def home(request):
    if request.method== "POST":
        filled_form= (TermForm(request.POST))
        if filled_form.is_valid():
            term=filled_form.cleaned_data['term']
            term_type=filled_form.cleaned_data['term_type']
            if term_type=="Instance":
                show="dbpedia"
                tab=getTerm(term)
            else:
                show="lov"
                tab= getVocab(term,term_type)
            results = tab
            new_form= TermForm()
            return render(request, 'transformToLd/home.html',{'form':new_form,'results':results, 'show':show})

    else:
        form= TermForm()
        return render(request, 'transformToLd/home.html',{'form':form})

def file_upload(request):
    if request.method=="POST":
        file=request.FILES['data_file']
        fs= FileSystemStorage()
        filename= fs.save(file.name,file)
        upload_file= fs.url(filename)
        type= file.content_type
        form= FileForm()

        if (type=='text/csv'):
            results= trait_csv(upload_file)
            return render(request,'transformToLd/file.html',{'form':form,'results':results})
        elif (type=='text/html'):
            results= trait_html(upload_file)
            return render(request,'transformToLd/file.html',{'form':form,'results':results})

    else:
        form= FileForm()
        return render(request,'transformToLd/file.html',{'form':form})