from django.contrib import admin
from .models import Employee, Role, Department

class ServiceAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'dept','salary','bonus', 'role', 'phone', 'hire_date')
# Register your models here.
admin.site.register(Employee)
admin.site.register(Role)
admin.site.register(Department)
