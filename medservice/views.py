from django.shortcuts import render
from .models import *
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .forms import *
from django.contrib.auth.mixins import PermissionRequiredMixin, UserPassesTestMixin


def index_view(request):
    return render(request, 'medservice/index.html',
                  {'content': 'Вас приветствует BestMed - лучшая частная клиника!'})


def success_result_view(request):
    return render(request, 'medservice/index.html', {'content': 'Действие успешно выполнено'})


def contacts_view(request):
    contacts = ('Телефон: 8(800)-55-55-777',
                'E-mail: info@bestmed.com',
                'Адрес клиники: г. Москва, ул. Невыдуманная, д. 17',
                )
    return render(request, 'medservice/contacts.html', {'content': contacts})


# Ниже идут вью для выполнения CRUD-действий в отношении категорий услуг
class MedServiceCategoryListView(ListView):
    model = MedServiceCategory
    template_name = 'medservice/med_service_category_list.html'


class MedServiceCategoryCreateView(PermissionRequiredMixin, CreateView):
    model = MedServiceCategory
    template_name = 'medservice/med_service_category_form.html'
    form_class = MedServiceCategoryForm
    success_url = '/service/'
    permission_required = 'medservice.add_medservicecategory'


class MedServiceCategoryUpdateView(PermissionRequiredMixin, UpdateView):
    model = MedServiceCategory
    template_name = 'medservice/med_service_category_form.html'
    form_class = MedServiceCategoryForm
    success_url = '/service/'
    permission_required = 'medservice.change_medservicecategory'


class MedServiceCategoryDeleteView(UserPassesTestMixin, DeleteView):
    model = MedServiceCategory
    template_name = 'medservice/confirm_deletion.html'
    success_url = '/service/'


    def test_func(self):
        return self.request.user.is_superuser


# Ниже идут вью для выполнения CRUD-действий в отношении видов услуг
class MedServiceListView(ListView):
    model = MedService
    template_name = 'medservice/med_service_list.html'


    def get_queryset(self):
        category_short_name = self.kwargs['category_short_name']
        med_service_category = MedServiceCategory.objects.get(short_name=category_short_name)
        return MedService.objects.filter(med_service_category=med_service_category)


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # кортеж для понимания, создана ли уже карточка у конкретного исследования
        med_service_cards = ()

        for item in context['object_list']:
            # Django не умеет делать get_or_none(), поэтому приходится получать пустой или непустой queryset по id
            if MedServiceCard.objects.filter(med_service=item.id).exists():
                med_service_cards += (item.id,)
        context['med_service_cards'] = med_service_cards
        return context


class MedServiceDetailView(DetailView):
    model = MedService
    template_name = 'medservice/detail_view.html'


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        card = MedServiceCard.objects.get(med_service=self.object.id)
        preparations = Preparation.objects.filter(card__id=card.id)
        context['card'] = card
        context['preparations'] = preparations

        # понимаю, что это совсем костыль, но уже нет времени сделать красиво - буду благодарен за подсказку :)
        # идея в том, чтобы при выборе видов услуг "Приём врача в отделении клиники", "Выезд врача на дом"
        # и "Приём врача по видеосвязи" отображались только доступные для них медицинские направления
        if self.object.short_name == 'indoor':
            med_specialties = MedSpecialty.objects.filter(is_available_indoor=True).order_by('name')
            context['med_specialties'] = med_specialties
        elif self.object.short_name == 'home_visit':
            med_specialties = MedSpecialty.objects.filter(is_available_home_visit=True).order_by('name')
            context['med_specialties'] = med_specialties
        elif self.object.short_name == 'video':
            med_specialties = MedSpecialty.objects.filter(is_available_video=True).order_by('name')
            context['med_specialties'] = med_specialties

        return context


class MedServiceCreateView(PermissionRequiredMixin, CreateView):
    model = MedService
    template_name = 'medservice/med_service_form.html'
    form_class = MedServiceForm
    success_url = '/success/'
    permission_required = 'medservice.add_medservice'


class MedServiceUpdateView(PermissionRequiredMixin, UpdateView):
    model = MedService
    template_name = 'medservice/med_service_form.html'
    form_class = MedServiceForm
    success_url = '/success/'
    permission_required = 'medservice.change_medservice'


class MedServiceDeleteView(UserPassesTestMixin, DeleteView):
    model = MedService
    template_name = 'medservice/confirm_deletion.html'
    success_url = '/success/'


    def test_func(self):
        return self.request.user.is_superuser


# Ниже идут вью для выполнения CRUD-действий в отношении подвидов услуг
class SubMedServiceListView(ListView):
    model = SubMedService
    template_name = 'medservice/sub_med_service_list.html'


    def get_queryset(self):
        short_name = self.kwargs['short_name']
        med_service = MedService.objects.get(short_name=short_name)
        return SubMedService.objects.filter(med_service=med_service)


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # кортеж для понимания, создана ли уже карточка у конкретного исследования
        sub_med_service_cards = ()

        for item in context['object_list']:
            # Django не умеет делать get_or_none(), поэтому приходится получать пустой или непустой queryset по id
            if SubMedServiceCard.objects.filter(sub_med_service=item.id).exists():
                sub_med_service_cards += (item.id,)
        context['sub_med_service_cards'] = sub_med_service_cards
        return context


class SubMedServiceDetailView(DetailView):
    model = SubMedService
    template_name = 'medservice/detail_view.html'


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        card = SubMedServiceCard.objects.get(sub_med_service=self.object.id)
        preparations = Preparation.objects.filter(card__id=card.id)
        context['card'] = card
        context['preparations'] = preparations
        return context


class SubMedServiceCreateView(PermissionRequiredMixin, CreateView):
    model = SubMedService
    template_name = 'medservice/sub_med_service_form.html'
    form_class = SubMedServiceForm
    success_url = '/success/'
    permission_required = 'medservice.add_submedservice'


class SubMedServiceUpdateView(PermissionRequiredMixin, UpdateView):
    model = SubMedService
    template_name = 'medservice/sub_med_service_form.html'
    form_class = SubMedServiceForm
    success_url = '/success/'
    permission_required = 'medservice.change_submedservice'


class SubMedServiceDeleteView(UserPassesTestMixin, DeleteView):
    model = SubMedService
    template_name = 'medservice/confirm_deletion.html'
    success_url = '/success/'


    def test_func(self):
        return self.request.user.is_superuser


# Ниже идут вью для выполнения CRUD-действий в отношении специальной подготовки
class PreparationListView(PermissionRequiredMixin, ListView):
    model = Preparation
    template_name = 'medservice/preparation_list.html'
    permission_required = 'medservice.view_preparation'


class PreparationCreateView(PermissionRequiredMixin, CreateView):
    model = Preparation
    template_name = 'medservice/preparation_form.html'
    form_class = PreparationForm
    success_url = '/preparation/'
    permission_required = 'medservice.add_preparation'


class PreparationUpdateView(PermissionRequiredMixin, UpdateView):
    model = Preparation
    template_name = 'medservice/preparation_form.html'
    form_class = PreparationForm
    success_url = '/preparation/'
    permission_required = 'medservice.change_preparation'


class PreparationDeleteView(UserPassesTestMixin, DeleteView):
    model = Preparation
    template_name = 'medservice/confirm_deletion.html'
    success_url = '/preparation/'


    def test_func(self):
        return self.request.user.is_superuser


# Ниже идут вью для выполнения CRUD-действий в отношении карточек видов услуг
class MedServiceCardCreateView(PermissionRequiredMixin, CreateView):
    model = MedServiceCard
    template_name = 'medservice/card_form.html'
    form_class = MedServiceCardForm
    success_url = '/success/'
    permission_required = 'medservice.add_medservicecard'

    def form_valid(self, form):
        med_service_card = form.save(commit=False)
        med_service_id = self.kwargs['pk']
        med_service_card.med_service = MedService.objects.get(id=med_service_id)
        med_service_card.save()
        return super().form_valid(form)


    def get_context_data(self, **kwargs):
        # Так как объект (карточка) еще не создан, то приходится отдельно вытягивать название вида услуги,
        # для которой создается карточка, чтобы отображать его она странице
        context = super().get_context_data(**kwargs)
        med_service_id = self.kwargs['pk']
        med_service = MedService.objects.get(id=med_service_id)
        context['name'] = med_service.name
        return context


class MedServiceCardUpdateView(PermissionRequiredMixin, UpdateView):
    model = MedServiceCard
    template_name = 'medservice/card_form.html'
    form_class = MedServiceCardForm
    success_url = '/success/'
    permission_required = 'medservice.change_medservicecard'

    def get_object(self, **kwargs):
        med_service_id = self.kwargs['pk']
        return MedServiceCard.objects.get(med_service=med_service_id)


class MedServiceCardDeleteView(UserPassesTestMixin, DeleteView):
    model = MedServiceCard
    template_name = 'medservice/card_confirm_deletion.html'
    success_url = '/success/'

    def get_object(self, **kwargs):
        med_service_id = self.kwargs['pk']
        return MedServiceCard.objects.get(med_service=med_service_id)


    def test_func(self):
        return self.request.user.is_superuser


# Ниже идут вью для выполнения CRUD-действий в отношении карточек подвидов услуг
class SubMedServiceCardCreateView(PermissionRequiredMixin, CreateView):
    model = SubMedServiceCard
    template_name = 'medservice/card_form.html'
    form_class = SubMedServiceCardForm
    success_url = '/success/'
    permission_required = 'medservice.add_submedservicecard'

    def form_valid(self, form):
        sub_med_service_card = form.save(commit=False)
        sub_med_service_id = self.kwargs['pk']
        sub_med_service_card.sub_med_service = SubMedService.objects.get(id=sub_med_service_id)
        sub_med_service_card.save()
        return super().form_valid(form)


    def get_context_data(self, **kwargs):
        # Так как объект (карточка) еще не создан, то приходится отдельно вытягивать название подвида услуги,
        # для которой создается карточка, чтобы отображать его она странице
        context = super().get_context_data(**kwargs)
        sub_med_service_id = self.kwargs['pk']
        sub_med_service = SubMedService.objects.get(id=sub_med_service_id)
        context['name'] = sub_med_service.name
        return context


class SubMedServiceCardUpdateView(PermissionRequiredMixin, UpdateView):
    model = SubMedServiceCard
    template_name = 'medservice/card_form.html'
    form_class = SubMedServiceCardForm
    success_url = '/success/'
    permission_required = 'medservice.change_submedservicecard'

    def get_object(self, **kwargs):
        sub_med_service_id = self.kwargs['pk']
        return SubMedServiceCard.objects.get(sub_med_service=sub_med_service_id)


class SubMedServiceCardDeleteView(UserPassesTestMixin, DeleteView):
    model = SubMedServiceCard
    template_name = 'medservice/card_confirm_deletion.html'
    success_url = '/success/'

    def get_object(self, **kwargs):
        sub_med_service_id = self.kwargs['pk']
        return SubMedServiceCard.objects.get(sub_med_service=sub_med_service_id)


    def test_func(self):
        return self.request.user.is_superuser


# Ниже идут вью для выполнения CRUD-действий в отношении мединских специальностей (медицинских направлений)
class MedSpecialtyListView(ListView):
    model = MedSpecialty
    template_name = 'medservice/med_specialty_list.html'


class MedSpecialtyDetailView(DetailView):
    model = MedSpecialty
    template_name = 'medservice/med_specialty_detail_view.html'


    def get_object(self, **kwargs):
        med_specialty_short_name = self.kwargs['short_name']
        return MedSpecialty.objects.get(short_name=med_specialty_short_name)
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        med_specialty_short_name = self.kwargs['short_name']
        doctors = Doctor.objects.filter(med_specialty__short_name=med_specialty_short_name, is_active=True).order_by('full_name')
        context['doctors'] = doctors
        return context


class MedSpecialtyCreateView(PermissionRequiredMixin, CreateView):
    model = MedSpecialty
    template_name = 'medservice/med_specialty_form.html'
    form_class = MedSpecialtyForm
    success_url = '/med-specialty/'
    permission_required = 'medservice.add_medspecialty'


class MedSpecialtyUpdateView(PermissionRequiredMixin, UpdateView):
    model = MedSpecialty
    template_name = 'medservice/med_specialty_form.html'
    form_class = MedSpecialtyForm
    success_url = '/med-specialty/'
    permission_required = 'medservice.change_medspecialty'


class MedSpecialtyDeleteView(UserPassesTestMixin, DeleteView):
    model = MedSpecialty
    template_name = 'medservice/confirm_deletion.html'
    success_url = '/med-specialty/'


    def test_func(self):
        return self.request.user.is_superuser


# Ниже идут вью для выполнения CRUD-действий в отношении врачей / докторов
class DoctorListView(PermissionRequiredMixin, ListView):
    model = Doctor
    template_name = 'medservice/doctor_list.html'
    permission_required = 'medservice.view_doctor'


    def get_queryset(self):
        return Doctor.objects.all().order_by('full_name')


class DoctorDetailView(DetailView):
    model = Doctor
    template_name = 'medservice/doctor_detail_view.html'


class DoctorCreateView(PermissionRequiredMixin, CreateView):
    model = Doctor
    template_name = 'medservice/doctor_form.html'
    form_class = DoctorForm
    success_url = '/doctor/'
    permission_required = 'medservice.add_doctor'


class DoctorUpdateView(PermissionRequiredMixin, UpdateView):
    model = Doctor
    template_name = 'medservice/doctor_form.html'
    form_class = DoctorForm
    success_url = '/doctor/'
    permission_required = 'medservice.change_doctor'


class DoctorDeleteView(UserPassesTestMixin, DeleteView):
    model = Doctor
    template_name = 'medservice/confirm_deletion.html'
    success_url = '/doctor/'

    def test_func(self):
        return self.request.user.is_superuser
