from django.shortcuts import render
from django.http import JsonResponse
from rest_framework import viewsets
from django.views import View 

from .models import Hero
from django.core.serializers import serialize
from json import loads

# Create your views here.
        
class HeroView(View):
  def get(self, request):
    # Serialize the data into JSON then turn the JSON into a dict
    all = loads(serialize('json', Hero.objects.all()))
    # Send the JSON response
    return JsonResponse(all, safe=False)

  def post(self, request):
    # Turn the body into a dict
    body = loads(request.body.decode("utf-8"))
    #create the new item
    newrecord = Hero.objects.create(fields=body)
    # Turn the object to json to dict, put in array to avoid non-iterable error
    data = loads(serialize('json', [newrecord]))
    # send json response with new object
    return JsonResponse(data, safe=False)

class OneHeroView(View):
  def get(self, request, param):
    # Filter and find a single item then serialize the data into JSON then turn the JSON into a dict
    one = loads(serialize("json", Hero.objects.filter(hero=param)))
    # Send the JSON response
    return JsonResponse(one, safe=False)

  def put(self, request, param):
    # Turn the body into a dict
    body = loads(request.body.decode("utf-8"))
    # update the item
    Hero.objects.filter(hero=param).update(fields=body)
    newrecord = Hero.objects.filter(hero=param)
    # Turn the object to json to dict, put in array to avoid non-iterable error
    data = loads(serialize('json', newrecord))
    # send json response with updated object
    return JsonResponse(data, safe=False)

  def delete(self, request, param):
    # delete the item, get all remaining records for response
    Hero.objects.filter(hero=param).delete()
    newrecord = Hero.objects.all()
    # Turn the results to json to dict, put in array to avoid non-iterable error
    data = loads(serialize('json', newrecord))
    # send json response with updated object
    return JsonResponse(data, safe=False)