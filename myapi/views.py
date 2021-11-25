from django.shortcuts import render
from django.http.response import JsonResponse

from rest_framework.parsers import JSONParser
from rest_framework import status
from rest_framework.decorators import api_view

from .serializers import CarSerializer, CarRateSerializer
from .models import Car, CarRate
import requests
import logging


@api_view(['GET', 'POST'])
def car_list(request):
    if request.method == 'GET':
        cars = Car.objects.all()

        make = request.query_params.get('make', None)
        if make is not None:
            cars = cars.filter(make__icontains=make)

        cars_serializer = CarSerializer(cars, many=True)

        return JsonResponse(cars_serializer.data, safe=False)

    elif request.method == 'POST':
        car_data = JSONParser().parse(request)
        car_serializer = CarSerializer(data=car_data)

        if car_serializer.is_valid():

            # get the right URL based on 'make' proivided in JSON
            api_url = "https://vpic.nhtsa.dot.gov/api/vehicles/getmodelsformake/{}?format=json".format(
                car_serializer.validated_data["make"].lower())

            try:
                req = requests.get(api_url)
                models = req.json()
            except:
                return JsonResponse({'message': 'No response from given URL'})

            for model in models['Results']:
                c = car_serializer.validated_data["make"].lower()
                if c == model["Make_Name"].lower() and c == model["Model_Name"].lower():
                    car_serializer.save()
                    return JsonResponse(car_serializer.data, status=status.HTTP_201_CREATED)

            return JsonResponse({'message': 'Car model not found!'})

        return JsonResponse(car_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
def car_detail(request, pk):
    try:
        car = Car.objects.get(pk=pk)
    except Car.DoesNotExist:
        return JsonResponse({'message': 'The car with given ID does not exist!'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'DELETE':
        car.delete()
        return JsonResponse({'message': 'Car was deleted succesfully!'}, status=status.HTTP_204_NO_CONTENT)


@api_view(['POST'])
def car_rate(request):

    if request.method == 'POST':
        rate_data = JSONParser().parse(request)
        rate_serializer = CarRateSerializer(data=rate_data)

        if rate_serializer.is_valid():
            try:
                car_obj = Car.objects.get(pk=rate_data['car_id'])
            except Car.DoesNotExist:
                return JsonResponse({'message': 'The car with given ID does not exist!'}, status=status.HTTP_404_NOT_FOUND)

            # check if rate is from 1 to 5
            r = rate_serializer.validated_data['rating']
            if int(r) >= 1 and int(r) <= 5:
                rate_serializer.save()
                return JsonResponse({'message': 'The rate is in the scope!'})
            else:
                return JsonResponse({'message': 'The rate is NOT in the scope!'})

        return JsonResponse(rate_serializer.errors)
