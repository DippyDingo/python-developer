from django.contrib import admin

# Register your models here.
from main.models import Product, Review


class ReviewInline(admin.TabularInline):
    model = Review
    fields = ['text', 'mark']


class ProductAdmin(admin.ModelAdmin):
    inlines = [ReviewInline]
    list_display = ['id', 'title', 'price']


admin.site.register(Product, ProductAdmin)
