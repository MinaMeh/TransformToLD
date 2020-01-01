from django.shortcuts import render
from .forms import TermForm
from .searchTerms import getTerm,getVocab
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
