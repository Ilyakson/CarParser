from django.db import models


class Category(models.Model):
    category = models.CharField(max_length=255)
    status = models.CharField(max_length=20, default="New")

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.category


class Vehicle(models.Model):
    vehicle_type = models.CharField(max_length=255, blank=True, null=True)
    vehicle_year = models.CharField(max_length=255, blank=True, null=True)
    vehicle_make = models.CharField(max_length=255, blank=True, null=True)
    vehicle_model = models.CharField(max_length=255, blank=True, null=True)
    vehicle_engine = models.CharField(max_length=255, blank=True, null=True)
    status = models.CharField(max_length=20, default="New")

    class Meta:
        verbose_name = "Car"
        verbose_name_plural = "Cars"

    def __str__(self):
        return self.vehicle_make


class Link(models.Model):
    link = models.URLField(unique=True)
    category = models.CharField(max_length=255)
    vehicle_make = models.CharField(max_length=255)
    status = models.CharField(max_length=20, default="New")

    class Meta:
        verbose_name = "Link"
        verbose_name_plural = "Links"

    def __str__(self):
        return self.link


class ProductInfo(models.Model):
    link = models.URLField()
    title = models.CharField(max_length=255)
    reviews = models.CharField(max_length=255, blank=True, null=True)
    count_of_reviews = models.CharField(max_length=255, blank=True, null=True)
    part = models.CharField(max_length=255)
    price = models.CharField(max_length=255)
    product_details = models.TextField()
    specifications = models.TextField(blank=True, null=True)
    category = models.CharField(max_length=255)
    vehicle_make = models.CharField(max_length=255)

    class Meta:
        verbose_name = "ProductInfo"
        verbose_name_plural = "ProductsInfo"

    def __str__(self):
        return self.title
