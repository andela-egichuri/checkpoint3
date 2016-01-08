from django.shortcuts import render
from rest_framework import generics
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse


def index(request):
    return render(request, 'index.html', {})


@api_view(('GET',))
def api_root(request, format=None):
    return Response({
        'bucketlists': reverse('bucketlist-list', request=request, format=format),
        'items': reverse('items-list', request=request, format=format),
    })