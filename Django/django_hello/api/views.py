# api/views.py
from rest_framework.decorators import api_view, renderer_classes
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response

@api_view(['GET'])
def hello_world(request):
    return Response({"message": "Hello World!"})

@api_view(['GET', 'POST'])
@renderer_classes([JSONRenderer])  # Только JSON для этого view
def hello_name(request):
    if request.method == 'POST':
        name = request.data.get('name', 'World')
        return Response({"message": f"Hello, {name}!"})
    else:
        return Response({"message": "Send a POST request with your name!"})

@api_view(['GET'])
def hello(request, name):
    return Response({"message": f"Hello {name}!"})

@api_view(['GET'])
def params(request):
    return Response(request.query_params)