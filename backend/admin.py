from django.contrib import admin
from .models import User, ShiftResult, Good, Order, BalanceModifier, FileUploader


admin.site.register(ShiftResult)
admin.site.register(User)
admin.site.register(Good)
admin.site.register(Order)
admin.site.register(BalanceModifier)
admin.site.register(FileUploader)
