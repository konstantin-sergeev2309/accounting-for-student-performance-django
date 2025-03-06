from django.contrib import admin
from .models import Group, Student, Prepods, PredM, Predmets, Cabs, Schedule, PA, Grade, CustomUser
from django.contrib.auth.admin import UserAdmin

class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        ('Дополнительная информация', {'fields': ('role', 'prepod')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Дополнительная информация', {'fields': ('role', 'prepod')}),
    )

    list_display = ('username', 'role', 'prepod', 'is_staff', 'is_superuser')
    list_filter = ('role', 'is_staff')

admin.site.register(CustomUser, CustomUserAdmin)

admin.site.register(Group)
admin.site.register(Student)
admin.site.register(Prepods)
admin.site.register(PredM)
admin.site.register(Predmets)
admin.site.register(Cabs)
admin.site.register(Schedule)
admin.site.register(PA)
admin.site.register(Grade)

