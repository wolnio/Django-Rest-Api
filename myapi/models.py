from django.db import models


class Car(models.Model):
    make = models.CharField(max_length=15)
    model = models.CharField(max_length=15)

    def __str__(self):      # print it when Car instance is needed
        return self.make


class CarRate(models.Model):
    car_id = models.ForeignKey(Car, related_name='rates',
                            on_delete=models.CASCADE,
                            default=0)
    rating = models.PositiveIntegerField(default=0)
