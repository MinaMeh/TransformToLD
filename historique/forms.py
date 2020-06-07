from django import forms


class projectForm(forms.Form):
    project_name = forms.CharField(label="Project name")
    description = forms.Textarea(label="Description")
    licence = forms.CharField(label="Licence")
    updated = forms.BooleanField()
    data_file = forms.FileField(label="Dataset file")
