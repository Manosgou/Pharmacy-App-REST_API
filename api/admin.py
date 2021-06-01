from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .models import *

# Register your models here.

class MedicineCategoryAdmin(admin.ModelAdmin):
    class Meta:
        model = MedicineCategory
        fields='__all__'

admin.site.register(MedicineCategory,MedicineCategoryAdmin)


class OrderInline(admin.StackedInline):
    model = Order

class MedicineAdmin(admin.ModelAdmin):
    inlines=[OrderInline,]
    class Meta:
        model=Medicine
        fields='_all__'

admin.site.register(Medicine,MedicineAdmin)



class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'user_profile'


class UserAdmin(BaseUserAdmin):
    inlines = (UserProfileInline,)


admin.site.unregister(User)
admin.site.register(User, UserAdmin)


class LocationAdmin(admin.ModelAdmin):
    class Meta:
        model=Location
        fields='_all__'

admin.site.register(Location,LocationAdmin)




class OrderAdmin(admin.ModelAdmin):
    class Meta:
        model = Order
        fields='__all__'

admin.site.register(Order,OrderAdmin)