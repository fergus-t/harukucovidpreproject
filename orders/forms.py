from django import forms

class locationForm(forms.Form):
    countryName = forms.CharField(label='Location Name', max_length=50)
    apisource = forms.CharField(label='API Source', max_length=200)
    resourceurl = forms.CharField(label='Resourceurl', max_length=200)
    population = forms.IntegerField(label='Population')