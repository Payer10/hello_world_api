from django.http import HttpResponse

def home(request):
    return HttpResponse("Hello, World!")


from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Continent
from .serializers import ContinentSerializer

@api_view(['GET'])
def continent_list(request):
    """
    Returns all continents with nested countries and their popular foods
    """
    continents = Continent.objects.all()
    serializer = ContinentSerializer(continents, many=True)
    return Response(serializer.data)
