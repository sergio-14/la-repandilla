from seg_mod_graduacion.models import RepositorioTitulados, Modalidad,Periodo
from django import forms
from django.core.validators import MaxValueValidator, MinValueValidator
from django.core.exceptions import ValidationError
import datetime
from gestion_usuarios.models import User

current_year = datetime.datetime.now().year
YEAR_CHOICES = [(year, year) for year in range(2020, current_year + 1)]

class TransferirActividadForm(forms.Form):
    periodo = forms.ModelChoiceField(
        queryset=Periodo.objects.all(),
        label='Periodo y Gestión',
        widget=forms.Select()
    )
    numero_acta = forms.CharField(label='Número de Acta', max_length=50)
    nota_aprobacion = forms.IntegerField(  
        label='Nota',
        validators=[MinValueValidator(50), MaxValueValidator(100)],
        widget=forms.NumberInput(attrs={'min': 50, 'max': 100})
    )

    def clean(self):
        cleaned_data = super().clean()
        return cleaned_data

class ActividadRepositorioForm(forms.ModelForm):
    nota_aprobacion = forms.IntegerField(  
        label='Nota',
        validators=[MinValueValidator(50), MaxValueValidator(100)],
        widget=forms.NumberInput(attrs={'min': 50, 'max': 100})
    )

    def clean(self):
        cleaned_data = super().clean()
        return cleaned_data

    class Meta:
        model = RepositorioTitulados
        fields = ['periodo', 'numero_acta', 'nota_aprobacion']
        labels = {
            'periodo': 'Periodo y Gestion',
            'numero_acta': 'Número de Acta',
            'nota_aprobacion': 'Nota'
        }

class ActividadFilterForm(forms.Form):
    nombre_completo = forms.CharField(
        max_length=100, 
        required=False, 
        label='Nombre Completo',
        widget=forms.TextInput(attrs={'placeholder': 'Nombre o Apellido del Egresado', 'class': 'form-control'}),
    )
    modalidad = forms.ModelChoiceField(
        queryset=Modalidad.objects.all(), 
        required=False, label='Modalidad',
        widget=forms.Select(attrs={'class': 'form-select'}),
        )
    periodo = forms.CharField(
        max_length=50,
        required=False,
        label='Periodo y Géstion',
        widget=forms.TextInput(attrs={'placeholder': 'ejm: "1/año" o "2/año"  ','class': 'form-control'}),
        )

class AgregarForm(forms.ModelForm):
    nota_aprobacion = forms.IntegerField(  
        label='Nota',
        validators=[MinValueValidator(50), MaxValueValidator(100)],
        widget=forms.NumberInput(attrs={'min': 50, 'max': 100, 'class': 'form-control'}),
    )
    
    class Meta:
        model = RepositorioTitulados
        fields = [
            'estudiante', 'tutor', 'jurado_1', 'jurado_2', 'jurado_3', 
            'titulo', 'resumen', 'modalidad', 
            'guia_externo', 'documentacion', 'periodo', 
            'numero_acta', 'nota_aprobacion', 'fecha'
        ]
        widgets = {
            'estudiante': forms.Select(attrs={'class': 'form-select'}),
            'tutor': forms.Select(attrs={'class': 'form-select'}),
            'jurado_1': forms.Select(attrs={'class': 'form-select'}),
            'jurado_2': forms.Select(attrs={'class': 'form-select'}),
            'jurado_3': forms.Select(attrs={'class': 'form-select'}),
            'titulo': forms.TextInput(attrs={'class': 'form-control'}),
            'resumen': forms.Textarea(attrs={'class': 'form-control'}),
            'modalidad': forms.Select(attrs={'class': 'form-select'}),
            'guia_externo': forms.TextInput(attrs={'class': 'form-control'}),
            'documentacion': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'periodo': forms.Select(attrs={'class': 'form-select'}),
            'numero_acta': forms.TextInput(attrs={'class': 'form-control'}),
            'fecha': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            
            
        }
        labels = {
            'estudiante': 'Nombre Completo Egresado:',
            'tutor': 'Tutor Asignado:',
            'jurado_1': '1er. Tribunal Asignado:',
            'jurado_2': '2do. Tribunal Asignado:',
            'jurado_3': '3er. Tribunal Asignado:',
            'titulo': 'Titulo del Proyecto:',
            'resumen': 'Descripción Breve del Proyecto:',
            'modalidad': 'Modalidad:',
            'guia_externo': 'Tutor Externo:',
            'documentacion': 'Documentación:',
            'periodo': 'Periodo y Gestion:',
            'numero_acta': 'Número de Acta',
            'nota_aprobacion': 'Nota',
            'fecha': 'Fecha'
        }
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        estudiantes = User.objects.filter(groups__name='Estudiantes').exclude(repo_estudiante__isnull=False)
        self.fields['estudiante'].queryset = estudiantes

        docentes = User.objects.filter(groups__name='Docentes')
        self.fields['tutor'].queryset = docentes
        self.fields['jurado_1'].queryset = docentes
        self.fields['jurado_2'].queryset = docentes
        self.fields['jurado_3'].queryset = docentes
        
        EXCLUDED_MODALITIES = ['Trabajo Dirigido', 'Proyecto de Grado', 'Tesis de Grado']
        self.fields['modalidad'].choices = [
            (choice_value, choice_label)
            for choice_value, choice_label in self.fields['modalidad'].choices
            if choice_label not in EXCLUDED_MODALITIES
        ]
        
    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.habilitada = True
        instance.jurado_1_aprobado = True
        instance.jurado_2_aprobado = True
        instance.jurado_3_aprobado = True
        instance.estado = 'Aprobado'
        if commit:
            instance.save()
        return instance
    
    def clean(self):
        cleaned_data = super().clean()
        return cleaned_data
