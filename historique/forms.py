from django import forms


class projectForm(forms.Form):
    project_name = forms.CharField(label="Project name")
    description = forms.Textarea(label="Description")
    licence = forms.CharField(label="Licence")
    file_path = forms.FileField(label="Dataset file")
