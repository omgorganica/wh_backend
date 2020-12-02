from django.contrib import admin
from .models import User, Shift_result, Good, Order, Balance_modifier


admin.site.register(Shift_result)
admin.site.register(User)
admin.site.register(Good)
admin.site.register(Order)
admin.site.register(Balance_modifier)

#