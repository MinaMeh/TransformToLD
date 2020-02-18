from django import forms
class TermForm(forms.Form):
    term= forms.CharField(label='The term',max_length=100)
    term_type= forms.ChoiceField(label="Type of the term",choices=[("Classe","Classe"),('Propriété','Propriété'),('Instance','Instance')])


class FileForm(forms.Form):
    data_file= forms.FileField(label="The file")