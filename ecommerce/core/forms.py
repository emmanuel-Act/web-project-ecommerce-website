from django import forms  #form is a django module used to create django forms
from core.models import * #to use all models in the core models.py

class ProductForm(forms.ModelForm): #ModelForm is a class in the forms module
    
    class Meta: #used when using ModelForm or simply creating forms from models
        model = Product 
        fields = '__all__'  #from the Product model of models.py take all fields
        
