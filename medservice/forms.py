from django import forms
from .models import *


class MedServiceCategoryForm(forms.ModelForm):
    name = forms.CharField(label='Название категории услуг',
                           widget=forms.Textarea(
                               attrs={
                                   'placeholder': 'Допускается 40 символов',
                                   'class': 'form-control',
                               }
                           ))

    short_name = forms.CharField(label='Сокращенное название',
                                 widget=forms.TextInput(attrs={'placeholder': 'до 10 латинских символов'})
                                 )


    class Meta:
        model = MedServiceCategory
        fields = '__all__'


class MedServiceForm(forms.ModelForm):
    med_service_category = forms.ModelChoiceField(label='Категория услуг',
                                                  queryset=MedServiceCategory.objects.all(),
                                                  widget=forms.Select,
                                                  )

    name = forms.CharField(label='Название вида услуг',
                           widget=forms.Textarea(
                               attrs={
                                   'placeholder': 'Допускается 100 символов',
                                   'class': 'form-control',
                               }
                           ))

    short_name = forms.CharField(label='Сокращенное название',
                                 widget=forms.TextInput(attrs={'placeholder': 'до 10 латинских символов'})
                                 )


    class Meta:
        model = MedService
        fields = '__all__'


class SubMedServiceForm(forms.ModelForm):
    med_service = forms.ModelChoiceField(label='Вид услуг',
                                         queryset=MedService.objects.all(),
                                         widget=forms.Select,
                                         )

    name = forms.CharField(label='Название подвида услуг',
                           widget=forms.Textarea(
                               attrs={
                                   'placeholder': 'Допускается 100 символов',
                                   'class': 'form-control',
                               }
                           ))


    class Meta:
        model = SubMedService
        fields = '__all__'


class PreparationForm(forms.ModelForm):
    name = forms.CharField(label='Название специальной подготовки',
                           widget=forms.Textarea(
                               attrs={
                                   'placeholder': 'Допускается 40 символов',
                                   'class': 'form-control',
                               }
                           ))


    description = forms.CharField(label='Описание',
                                  widget=forms.Textarea(
                                      attrs={
                                          'placeholder': 'Допускается 2000 символов',
                                          'class': 'form-control',
                                      }
                                  ))


    class Meta:
        model = Preparation
        fields = '__all__'


class MedServiceCardForm(forms.ModelForm):
    med_service = forms.ModelChoiceField(label='Вид услуг',
                                         queryset=MedService.objects.all(),
                                         widget=forms.Select,
                                         )

    description = forms.CharField(label='Описание',
                                  widget=forms.Textarea(
                                      attrs={
                                          'placeholder': 'Допускается 2000 символов',
                                          'class': 'form-control',
                                      }
                                  ))

    preparation = forms.ModelMultipleChoiceField(label='Специальная подготовка',
                                  queryset=Preparation.objects.all(),
                                  widget=forms.SelectMultiple,
                                  )

    price = forms.IntegerField(label='Цена услуги',
                                   widget=forms.NumberInput(
                                       attrs={
                                           'min': 1,
                                       }
                                   ))

    interesting_fact = forms.CharField(required=False,
                                       label='Интересный факт',
                                       widget=forms.Textarea(
                                           attrs={
                                               'placeholder': 'Допускается 1000 символов',
                                               'class': 'form-control',
                                           }
                                       ))


    class Meta:
        model = MedServiceCard
        fields = '__all__'


class SubMedServiceCardForm(forms.ModelForm):
    sub_med_service = forms.ModelChoiceField(label='Подвид услуг',
                                         queryset=SubMedService.objects.all(),
                                         widget=forms.Select,
                                         )

    description = forms.CharField(label='Описание',
                                  widget=forms.Textarea(
                                      attrs={
                                          'placeholder': 'Допускается 2000 символов',
                                          'class': 'form-control',
                                      }
                                  ))

    preparation = forms.ModelMultipleChoiceField(label='Специальная подготовка',
                                  queryset=Preparation.objects.all(),
                                  widget=forms.SelectMultiple,
                                  )

    price = forms.IntegerField(label='Цена услуги',
                                   widget=forms.NumberInput(
                                       attrs={
                                           'min': 1,
                                       }
                                   ))

    interesting_fact = forms.CharField(required=False,
                                       label='Интересный факт',
                                       widget=forms.Textarea(
                                           attrs={
                                               'placeholder': 'Допускается 1000 символов',
                                               'class': 'form-control',
                                           }
                                       ))


    class Meta:
        model = SubMedServiceCard
        fields = '__all__'
