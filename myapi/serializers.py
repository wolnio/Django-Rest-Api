from rest_framework import serializers
from .models import Car, CarRate


class CarRateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CarRate
        fields=('__all__')
        


class CarSerializer(serializers.ModelSerializer):
    rates = CarRateSerializer(many=True, read_only=True)

    ''' -----> get all rates of given object and calculate average rate
                can't figure how to extract rating value...

    avg_rating=serializers.SerializerMethodField('_get_average_rate')

    def _get_average_rate(self, car_obj):
        
        mylist=car_obj.annotate(CarRate('rating'))
        #y=CarRate.objects.prefetch_related('rating')
        #x=y.objects.values_list('rating')
        print(mylist)       #test returned value
        avg_rating=mylist
        return avg_rating
    '''

    def create(self, validated_data):
        rates_data = validated_data.pop("rates")
        car = Car.objects.create(**validated_data)
        for rate_data in rates_data:
            CarRate.objects.create(car=car, **rate_data)
        return car

    class Meta:
        model = Car
        fields = ('id', 'make', 'model','rates','avg_rating')

    
