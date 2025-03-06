from django.urls import path
from django.shortcuts import HttpResponse
from .views import index, redirect_view, login_view, logout_view, prepodovat_view, edit_grade, uchebnaya_view, dopusk_report_view, uspevaemost_report_view, generate_dopusk_report, zadolzhennosti_report_view, generate_zadolzhennosti_excel, uspevaemost_report_view, generate_uspevaemost_excel, administ_view, add_student, delete_student, import_grades, itogi_view

def uchebnaya_chast_home(request):
    return HttpResponse("Страница учебной части")  # Временно для теста

urlpatterns = [
    path('', index, name='index'),
    path('login/', login_view, name='login'),
    path('redirect/', redirect_view, name='redirect'),
    path('logout/', logout_view, name='logout'),
    path('uchebnaya_chast/', uchebnaya_chast_home, name='uchebnaya_chast_home'),
    path('prepod/', prepodovat_view, name='prepodovat'),
    path('edit-grade/<int:pa_id>/', edit_grade, name='edit_grade'),
    path('uchebnaya/', uchebnaya_view, name='uchebnaya'),
    path('dopusk-report/', dopusk_report_view, name='dopusk_report'),
    path('uspevaemost-report/', uspevaemost_report_view, name='uspevaemost_report'),
    path('generate-dopusk-report/', generate_dopusk_report, name='generate_dopusk_report'),
    path('zadolzhennosti-report/', zadolzhennosti_report_view, name='zadolzhennosti_report'),
    path('generate-zadolzhennosti-excel/', generate_zadolzhennosti_excel, name='generate_zadolzhennosti_excel'),
    path('uspevaemost-report/', uspevaemost_report_view, name='uspevaemost_report'),
    path('generate-uspevaemost-excel/', generate_uspevaemost_excel, name='generate_uspevaemost_excel'),
    path('administ/', administ_view, name='administ'),
    path('add-student/', add_student, name='add_student'),
    path('delete-student/', delete_student, name='delete_student'),
    path('import-grades/', import_grades, name='import_grades'),
    path('itogi/', itogi_view, name='itogi'),
]
