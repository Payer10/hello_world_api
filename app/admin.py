from django.contrib import admin
from .models import Subcontinent, Country, Dish, DishImage

class DishImageInline(admin.TabularInline):
    model = DishImage
    extra = 1

@admin.register(Dish)
class DishAdmin(admin.ModelAdmin):
    inlines = [DishImageInline]

admin.site.register(Subcontinent)
admin.site.register(Country)
admin.site.register(DishImage)
