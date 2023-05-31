"""best_med URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from medservice.views import *
from userapp.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index_view),
    path('contacts/', contacts_view),
    path('success/', success_result_view),
    path('registration/', UserRegistrationView.as_view(), name="UserRegistration"),
    path('login/', UserLoginView.as_view(), name="UserLogin"),
    path('logout/', UserLogoutView.as_view(), name="UserLogout"),

    # Пути для создания категорий, видов, подвидов услуг и специальной подготовки
    path('create/',
         include(
             [
             path('med-service-category/', MedServiceCategoryCreateView.as_view(), name="create-MedServiceCategory"),
             path('med-service/', MedServiceCreateView.as_view(), name="create-MedService"),
             path('sub-med-service/', SubMedServiceCreateView.as_view(), name="create-SubMedService"),
             path('preparation/', PreparationCreateView.as_view(), name="create-Preparation"),
             path('med-specialty/', MedSpecialtyCreateView.as_view(), name="create-MedSpecialty"),
             path('doctor/', DoctorCreateView.as_view(), name="create-Doctor"),
             ]
         )
    ),

    # Пути относятся к специальной подготовке
    path('preparation/',
         include(
             [
             path('', PreparationListView.as_view(), name="Preparation"),
             path('<int:pk>/update/', PreparationUpdateView.as_view()),
             path('<int:pk>/delete/', PreparationDeleteView.as_view()),
             ]
         )
    ),

    # Пути относятся к медицинской специальности (медицинскому направлению)
    path('med-specialty/',
         include(
             [
             path('', MedSpecialtyListView.as_view(), name="MedSpecialty"),
             path('<slug:short_name>/', MedSpecialtyDetailView.as_view()),
             path('<int:pk>/update/', MedSpecialtyUpdateView.as_view()),
             path('<int:pk>/delete/', MedSpecialtyDeleteView.as_view()),
             ]
         )
    ),

    # Пути относятся к врачам / докторам
    path('doctor/',
         include(
             [
             path('', DoctorListView.as_view(), name="Doctor"),
             path('<int:pk>/', DoctorDetailView.as_view()),
             path('<int:pk>/update/', DoctorUpdateView.as_view()),
             path('<int:pk>/delete/', DoctorDeleteView.as_view()),
             ]
         )
    ),

    # Пути для медицинских услуг - отображение, обновление, удаление
    path('service/',
         include(
             [
             path('', MedServiceCategoryListView.as_view()),
             path('<int:pk>/update/', MedServiceCategoryUpdateView.as_view()),
             path('<int:pk>/delete/', MedServiceCategoryDeleteView.as_view()),

             # Пути ниже относятся к виду услуг, например, выезд врача на дом
             path('<slug:category_short_name>/', MedServiceListView.as_view()),
             path('<slug:category_short_name>/<int:pk>/', MedServiceDetailView.as_view()),
             path('<slug:category_short_name>/<int:pk>/update/', MedServiceUpdateView.as_view()),
             path('<slug:category_short_name>/<int:pk>/delete/', MedServiceDeleteView.as_view()),
             path('<slug:category_short_name>/<int:pk>/card/create/', MedServiceCardCreateView.as_view()),
             path('<slug:category_short_name>/<int:pk>/card/update/', MedServiceCardUpdateView.as_view()),
             path('<slug:category_short_name>/<int:pk>/card/delete/', MedServiceCardDeleteView.as_view()),

             # Пути ниже относятся к подвиду услуг, например, УЗИ органов брюшной полости
             path('<slug:category_short_name>/<slug:short_name>/', SubMedServiceListView.as_view()),
             path('<slug:category_short_name>/<slug:short_name>/<int:pk>/', SubMedServiceDetailView.as_view()),
             path('<slug:category_short_name>/<slug:short_name>/<int:pk>/update/', SubMedServiceUpdateView.as_view()),
             path('<slug:category_short_name>/<slug:short_name>/<int:pk>/delete/', SubMedServiceDeleteView.as_view()),
             path('<slug:category_short_name>/<slug:short_name>/<int:pk>/card/create/', SubMedServiceCardCreateView.as_view()),
             path('<slug:category_short_name>/<slug:short_name>/<int:pk>/card/update/', SubMedServiceCardUpdateView.as_view()),
             path('<slug:category_short_name>/<slug:short_name>/<int:pk>/card/delete/', SubMedServiceCardDeleteView.as_view()),
             ]
         )
    ),
]
