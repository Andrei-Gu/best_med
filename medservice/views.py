from django.shortcuts import render
from .models import *
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .forms import *


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


class MedServiceCategoryCreateView(CreateView):
    model = MedServiceCategory
    template_name = 'medservice/med_service_category_form.html'
    form_class = MedServiceCategoryForm
    success_url = '/service/'


class MedServiceCategoryUpdateView(UpdateView):
    model = MedServiceCategory
    template_name = 'medservice/med_service_category_form.html'
    form_class = MedServiceCategoryForm
    success_url = '/service/'


class MedServiceCategoryDeleteView(DeleteView):
    model = MedServiceCategory
    template_name = 'medservice/confirm_deletion.html'
    success_url = '/service/'


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
        return context


class MedServiceCreateView(CreateView):
    model = MedService
    template_name = 'medservice/med_service_form.html'
    form_class = MedServiceForm
    success_url = '/success/'


class MedServiceUpdateView(UpdateView):
    model = MedService
    template_name = 'medservice/med_service_form.html'
    form_class = MedServiceForm
    success_url = '/success/'


class MedServiceDeleteView(DeleteView):
    model = MedService
    template_name = 'medservice/confirm_deletion.html'
    success_url = '/success/'


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


class SubMedServiceCreateView(CreateView):
    model = SubMedService
    template_name = 'medservice/sub_med_service_form.html'
    form_class = SubMedServiceForm
    success_url = '/success/'


class SubMedServiceUpdateView(UpdateView):
    model = SubMedService
    template_name = 'medservice/sub_med_service_form.html'
    form_class = SubMedServiceForm
    success_url = '/success/'


class SubMedServiceDeleteView(DeleteView):
    model = SubMedService
    template_name = 'medservice/confirm_deletion.html'
    success_url = '/success/'


# Ниже идут вью для выполнения CRUD-действий в отношении специальной подготовки
class PreparationListView(ListView):
    model = Preparation
    template_name = 'medservice/preparation_list.html'


class PreparationCreateView(CreateView):
    model = Preparation
    template_name = 'medservice/preparation_form.html'
    form_class = PreparationForm
    success_url = '/preparation/'


class PreparationUpdateView(UpdateView):
    model = Preparation
    template_name = 'medservice/preparation_form.html'
    form_class = PreparationForm
    success_url = '/preparation/'


class PreparationDeleteView(DeleteView):
    model = Preparation
    template_name = 'medservice/confirm_deletion.html'
    success_url = '/preparation/'


# Ниже идут вью для выполнения CRUD-действий в отношении карточек видов услуг
class MedServiceCardCreateView(CreateView):
    model = MedServiceCard
    template_name = 'medservice/card_form.html'
    form_class = MedServiceCardForm
    success_url = '/success/'

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


class MedServiceCardUpdateView(UpdateView):
    model = MedServiceCard
    template_name = 'medservice/card_form.html'
    form_class = MedServiceCardForm
    success_url = '/success/'

    def get_object(self, **kwargs):
        med_service_id = self.kwargs['pk']
        return MedServiceCard.objects.get(med_service=med_service_id)


class MedServiceCardDeleteView(DeleteView):
    model = MedServiceCard
    template_name = 'medservice/card_confirm_deletion.html'
    success_url = '/success/'

    def get_object(self, **kwargs):
        med_service_id = self.kwargs['pk']
        return MedServiceCard.objects.get(med_service=med_service_id)


# Ниже идут вью для выполнения CRUD-действий в отношении карточек подвидов услуг
class SubMedServiceCardCreateView(CreateView):
    model = SubMedServiceCard
    template_name = 'medservice/card_form.html'
    form_class = SubMedServiceCardForm
    success_url = '/success/'

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


class SubMedServiceCardUpdateView(UpdateView):
    model = SubMedServiceCard
    template_name = 'medservice/card_form.html'
    form_class = SubMedServiceCardForm
    success_url = '/success/'

    def get_object(self, **kwargs):
        sub_med_service_id = self.kwargs['pk']
        return SubMedServiceCard.objects.get(sub_med_service=sub_med_service_id)


class SubMedServiceCardDeleteView(DeleteView):
    model = SubMedServiceCard
    template_name = 'medservice/card_confirm_deletion.html'
    success_url = '/success/'

    def get_object(self, **kwargs):
        sub_med_service_id = self.kwargs['pk']
        return SubMedServiceCard.objects.get(sub_med_service=sub_med_service_id)
