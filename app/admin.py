from django.contrib import admin

from app.models import Category, Link, ProductInfo, Vehicle


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = [
        "category", "status",
    ]


@admin.register(Vehicle)
class VehicleAdmin(admin.ModelAdmin):
    list_display = [
        "vehicle_type", "vehicle_year",
        "vehicle_make", "vehicle_model", "vehicle_engine", "status",
    ]


@admin.register(Link)
class LinkAdmin(admin.ModelAdmin):
    list_display = ["link", "category", "vehicle_make", "status"]


@admin.register(ProductInfo)
class ProductInfoAdmin(admin.ModelAdmin):
    list_display = [
        "link", "title", "part",
        "price", "reviews", "count_of_reviews",
        "product_details", "specifications", "category", "vehicle_make",
    ]
