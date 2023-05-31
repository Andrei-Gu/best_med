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
                                 widget=forms.TextInput(
                                     attrs={
                                         'placeholder': 'до 10 латинских символов',
                                     }
                                 ))


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
                                 widget=forms.TextInput(
                                     attrs={
                                         'placeholder': 'до 10 латинских символов',
                                     }
                                 ))


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


class MedSpecialtyForm(forms.ModelForm):
    name = forms.CharField(label='Название медицинской специальности / медицинского направления',
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

    short_name = forms.CharField(label='Сокращенное название',
                                 widget=forms.TextInput(
                                     attrs={
                                         'placeholder': 'до 10 латинских символов',
                                     }
                                 ))
    

    is_available_indoor = forms.BooleanField(label='Доступно для "Приём в клинике"', required=False)
    is_available_home_visit = forms.BooleanField(label='Доступно для "Приём на дому"', required=False)
    is_available_video = forms.BooleanField(label='Доступно для "Приём по видеосвязи"', required=False)


    class Meta:
        model = MedSpecialty
        fields = '__all__'


class DoctorForm(forms.ModelForm):
    full_name = forms.CharField(label='ФИО врача полостью',
                                widget=forms.Textarea(
                                    attrs={
                                        'placeholder': 'Допускается 50 символов',
                                        'class': 'form-control',
                                    }
                                ))


    education_and_degree = forms.CharField(label='Образование и ученая степень',
                                           widget=forms.Textarea(
                                               attrs={
                                                   'placeholder': 'Допускается 2000 символов',
                                                   'class': 'form-control',
                                               }
                                           ))


    date_med_practice_started = forms.DateInput()


    med_specialty = forms.ModelMultipleChoiceField(label='Медицинская специальность',
                                                   queryset=MedSpecialty.objects.all(),
                                                   widget=forms.SelectMultiple,
                                                   )


    is_active = forms.BooleanField(label='Ведет / не ведет приём', required=False)


    class Meta:
        model = Doctor
        fields = '__all__'
