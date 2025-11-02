from rest_framework.decorators import api_view, parser_classes
from rest_framework.parsers import JSONParser, MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework import status

from .models import Subcontinent, Country, Dish, DishImage
from .serializers import SubcontinentSerializer, CountrySerializer, DishSerializer, DishImageSerializer

# Subcontinents
@api_view(["GET", "POST"])
def subcontinent_list_create(request):
    if request.method == "GET":
        objs = Subcontinent.objects.all()
        serializer = SubcontinentSerializer(objs, many=True, context={"request": request})
        return Response(serializer.data)
    else:  # POST
        serializer = SubcontinentSerializer(data=request.data, context={"request": request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(["GET", "PUT", "DELETE"])
def subcontinent_detail(request, pk):
    try:
        obj = Subcontinent.objects.get(pk=pk)
    except Subcontinent.DoesNotExist:
        return Response({"detail": "Not found"}, status=status.HTTP_404_NOT_FOUND)

    if request.method == "GET":
        serializer = SubcontinentSerializer(obj, context={"request": request})
        return Response(serializer.data)
    if request.method == "PUT":
        serializer = SubcontinentSerializer(obj, data=request.data, context={"request": request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    if request.method == "DELETE":
        obj.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

# Countries
@api_view(["GET", "POST"])
def country_list_create(request):
    if request.method == "GET":
        objs = Country.objects.select_related("subcontinent").all()
        serializer = CountrySerializer(objs, many=True, context={"request": request})
        return Response(serializer.data)
    else:
        serializer = CountrySerializer(data=request.data, context={"request": request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(["GET", "PUT", "DELETE"])
def country_detail(request, pk):
    try:
        obj = Country.objects.get(pk=pk)
    except Country.DoesNotExist:
        return Response({"detail": "Not found"}, status=status.HTTP_404_NOT_FOUND)

    if request.method == "GET":
        serializer = CountrySerializer(obj, context={"request": request})
        return Response(serializer.data)
    if request.method == "PUT":
        serializer = CountrySerializer(obj, data=request.data, context={"request": request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    if request.method == "DELETE":
        obj.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

# Dishes
@api_view(["GET", "POST"])
@parser_classes([MultiPartParser, FormParser, JSONParser])
def dish_list_create(request):
    if request.method == "GET":
        objs = Dish.objects.select_related("country__subcontinent").prefetch_related("images").all()
        serializer = DishSerializer(objs, many=True, context={"request": request})
        return Response(serializer.data)

    # POST: expect fields: name, country (id), short_description, ingredients, why_popular
    # images: one or many files named 'images'
    data = request.data.copy()
    serializer = DishSerializer(data=data, context={"request": request})
    if serializer.is_valid():
        dish = serializer.save()
        # handle uploaded images
        images = request.FILES.getlist("images")
        for img in images:
            DishImage.objects.create(dish=dish, image=img)
        out_serializer = DishSerializer(dish, context={"request": request})
        return Response(out_serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(["GET", "PUT", "DELETE"])
@parser_classes([MultiPartParser, FormParser, JSONParser])
def dish_detail(request, pk):
    try:
        obj = Dish.objects.get(pk=pk)
    except Dish.DoesNotExist:
        return Response({"detail": "Not found"}, status=status.HTTP_404_NOT_FOUND)

    if request.method == "GET":
        serializer = DishSerializer(obj, context={"request": request})
        return Response(serializer.data)
    if request.method == "PUT":
        serializer = DishSerializer(obj, data=request.data, partial=True, context={"request": request})
        if serializer.is_valid():
            dish = serializer.save()
            # optional: handle new images if provided
            images = request.FILES.getlist("images")
            for img in images:
                DishImage.objects.create(dish=dish, image=img)
            return Response(DishSerializer(dish, context={"request": request}).data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    if request.method == "DELETE":
        obj.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
