from .models import MedServiceCategory, MedService


def rendering_categories_and_services(request):
    return {
            'all_med_service_categories': MedServiceCategory.objects.all(),
            'all_med_services': MedService.objects.all(),
    }