from django.contrib import admin
from .models import User, Shift, Good, Order, BalanceModifier, FileUploader, BalanceModifierHistory

admin.site.register(Shift)
# admin.site.register(User)
admin.site.register(Good)
admin.site.register(Order)
admin.site.register(BalanceModifier)
admin.site.register(FileUploader)
admin.site.register(BalanceModifierHistory)


class UserAdmin(admin.ModelAdmin):
	list_filter = ['is_superuser', 'is_staff']


admin.site.register(User,UserAdmin)
