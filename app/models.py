from django.db import models

class Continent(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Country(models.Model):
    continent = models.ForeignKey(Continent, related_name='countries', on_delete=models.CASCADE,default = 1)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Food(models.Model):
    country = models.ForeignKey(Country, related_name='foods', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    description = models.TextField()  # why popular
    ingredients = models.TextField()   # ingredients
    preparation = models.TextField()   # how it’s made

    def __str__(self):
        return self.name 
