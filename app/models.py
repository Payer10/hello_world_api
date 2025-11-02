from django.db import models

class Subcontinent(models.Model):   # উপমহাদেশ
    name = models.CharField(max_length=100)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order", "name"]

    def __str__(self):
        return self.name

class Country(models.Model):
    subcontinent = models.ForeignKey(Subcontinent, related_name="countries", on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    iso_code = models.CharField(max_length=10, blank=True, null=True)

    def __str__(self):
        return f"{self.name} ({self.subcontinent.name})"

class Dish(models.Model):   # জনপ্রিয় খাবার
    country = models.ForeignKey(Country, related_name="dishes", on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    short_description = models.CharField(max_length=300, blank=True)
    ingredients = models.TextField(blank=True)             # ei khabar ki ki diye make hoyeche
    why_popular = models.TextField(blank=True)             # জনবৃহত্তর কারণ / জনপ্রিয়তার কারণ
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.country.name}"

class DishImage(models.Model):
    dish = models.ForeignKey(Dish, related_name="images", on_delete=models.CASCADE)
    image = models.ImageField(upload_to="dishes/")
    caption = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return f"Image for {self.dish.name}"
