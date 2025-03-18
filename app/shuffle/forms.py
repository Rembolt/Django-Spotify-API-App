
from django import forms

class LinkForm(forms.Form):
       link = forms.CharField(required=True,label='',
      widget=forms.TextInput(attrs={ 'placeholder': 'Insert a playlist link','id':'playlist-link', 'class':'input field'}))
       
       genreCheck = forms.BooleanField(required=False,label='', initial=False,
      widget=forms.CheckboxInput(attrs={'id':'genre-shuffle', 'class':'check input field' , 'style':"order:2;"}))
       
       similarityPercentage = forms.IntegerField(required=False,label='', initial=0,
      widget=forms.TextInput(attrs={ 'placeholder': '','id':'similarity-percentage', 'class':'integer input field', 'style':"order:3;"}))
       
       recentCheck = forms.BooleanField(required=False,label='', initial=False,
      widget=forms.CheckboxInput(attrs={'id':'recent-shuffle', 'class':'check input field', 'style':"order:4;"}))
       
       recentPercentage = forms.IntegerField(required=False,label='', initial=100,
      widget=forms.TextInput(attrs={ 'placeholder': '','id':'recent-percentage', 'class':'integer input field', 'style':"order:5;"}))