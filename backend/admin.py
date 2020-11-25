from django.contrib import admin
from .models import User, Shift_result, Operation, Good, Order, Balance_modifier
from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import User
from django.contrib.auth.admin import UserAdmin


admin.site.register(Shift_result)
admin.site.register(User)
admin.site.register(Operation)
admin.site.register(Good)
admin.site.register(Order)
admin.site.register(Balance_modifier)

# class CustomUserAdmin(UserAdmin):
#     add_form = CustomUserCreationForm
#     form = CustomUserChangeForm
#     model = User
#     list_display = ('email', 'is_staff', 'is_active',)
#     list_filter = ('email', 'is_staff', 'is_active',)
#     fieldsets = (
#         (None, {'fields': ('email', 'password','wms_id')}),
#         ('Permissions', {'fields': ('is_staff', 'is_active')}),
#     )
#     add_fieldsets = (
#         (None, {
#             'classes': ('wide',),
#             'fields': ('email', 'password1', 'password2', 'is_staff', 'is_active')}
#         ),
#     )
#     search_fields = ('email',)
#     ordering = ('email',)
#
#
# admin.site.register(User, CustomUserAdmin)