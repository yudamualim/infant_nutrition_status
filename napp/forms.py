from django import forms
from .models import Person

class PersonForm(forms.ModelForm):
    class Meta:
        model = Person
        fields = ['NIK', 'Nama', 'Berat_Badan', 'Tinggi_Badan', 'Usia_Saat_UKur', 'Jenis_Kelamin', 'Status_Gizi_Balita']
        
        # Add widgets for better user experience
        widgets = {
            'NIK': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter NIK'}),
            'Nama': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Name'}),
            'Berat_Badan': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter Weight'}),
            'Tinggi_Badan': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter Height'}),
            'Usia_Saat_UKur': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter Age'}),
            'Jenis_Kelamin': forms.Select(choices=[('L', 'Laki-Laki'), ('P', 'Perempuan')], attrs={'class': 'form-control'}),
            'Status_Gizi_Balita': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Nutrition Status'}),
        }
