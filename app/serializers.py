from rest_framework import serializers
from .models import Subcontinent, Country, Dish, DishImage

class DishImageSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = DishImage
        fields = ["id", "image_url", "caption"]

    def get_image_url(self, obj):
        request = self.context.get("request")
        if request is None:
            return obj.image.url
        return request.build_absolute_uri(obj.image.url)

class DishSerializer(serializers.ModelSerializer):
    images = DishImageSerializer(many=True, read_only=True)

    class Meta:
        model = Dish
        fields = ["id", "name", "short_description", "ingredients", "why_popular", "country", "images", "created_at"]

class CountrySerializer(serializers.ModelSerializer):
    dishes = DishSerializer(many=True, read_only=True)

    class Meta:
        model = Country
        fields = ["id", "name", "iso_code", "subcontinent", "dishes"]

class SubcontinentSerializer(serializers.ModelSerializer):
    countries = CountrySerializer(many=True, read_only=True)

    class Meta:
        model = Subcontinent
        fields = ["id", "name", "order", "countries"]
