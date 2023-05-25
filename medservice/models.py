from django.db import models


# Вид категорий услуг: прием врача, лабораторная диагностика, инструментальное исследование, выдача справок
class MedServiceCategory(models.Model):
    name = models.TextField(unique=True, max_length=40)
    short_name = models.CharField(unique=True, max_length=10)


    def __str__(self):
        return self.name


    def get_absolute_url(self):
        return "/service/%i/" % self.id


    def get_short_name_url(self):
        return "/service/%s/" % self.short_name


# Конкретный вид услуги: выезд врача на дом, УЗИ, общий анализ крови
class MedService(models.Model):
    med_service_category = models.ForeignKey(MedServiceCategory, on_delete=models.CASCADE)
    name = models.TextField(unique=True, max_length=100)
    short_name = models.CharField(unique=True, max_length=10)


    def __str__(self):
        return self.name


    def get_absolute_url(self):
        return f"{self.med_service_category.get_short_name_url()}{self.id}/"


    def get_short_name_url(self):
        # Чтобы корректно разнести переходы на страницы видов услуг, у которых есть подвиды (список),
        # и виды, которые являются "конечными" и не имеют подвидов (сразу на карточку вида услуги),
        # делаем проврку на существование подвидов и возвращаем соответствующий url
        if SubMedService.objects.filter(med_service=self.id).exists():
            return f"{self.med_service_category.get_short_name_url()}{self.short_name}/"
        else:
            return self.get_absolute_url()


# Подвид услуги: УЗИ сосудов, УЗИ органов брюшной полости
class SubMedService(models.Model):
    med_service = models.ForeignKey(MedService, on_delete=models.CASCADE)
    name = models.TextField(unique=True, max_length=100)


    def __str__(self):
        return self.name


    def get_absolute_url(self):
        return f"{self.med_service.get_short_name_url()}{self.id}/"


# Необходимость специальной подготовки: специальная подготовка не требуется, натощак и т.д.
class Preparation(models.Model):
    name = models.TextField(max_length=40)
    description = models.TextField(max_length=2000)


    def __str__(self):
        return self.name


    def get_absolute_url(self):
        return "/preparation/%i/" % self.id


# Базовый класс карточки с описанием и стоимостью
class Card(models.Model):
    description = models.TextField(max_length=2000)
    preparation = models.ManyToManyField(Preparation)
    price = models.PositiveIntegerField()
    interesting_fact = models.TextField(max_length=1000, blank=True)


# Карточка с описанием конкретного вида услуг
# Если у конкретного вида услуг имеются подвиды, то карточка именно для вида не подлежит созданию
class MedServiceCard(Card):
    med_service = models.OneToOneField(MedService, on_delete=models.CASCADE)


# Карточка с описанием конкретного подвида услуги
class SubMedServiceCard(Card):
    sub_med_service = models.OneToOneField(SubMedService, on_delete=models.CASCADE)
