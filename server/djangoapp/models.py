# Uncomment the following imports before adding the Model code

from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator


# Create your models here.

class CarMake(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.name  # String representation of the CarMake object


# CarModel model
class CarModel(models.Model):
    car_make = models.ForeignKey(
        CarMake, on_delete=models.CASCADE
    )  # Many-to-One relationship
    name = models.CharField(max_length=100)

    # Choices for car types
    CAR_TYPES = [
        ('SEDAN', 'Sedan'),
        ('SUV', 'SUV'),
        ('WAGON', 'Wagon'),
        # Add more choices if necessary
    ]
    type = models.CharField(max_length=10, choices=CAR_TYPES, default='SUV')
    dealer_id = models.IntegerField()
    year = models.IntegerField(
        validators=[
            MaxValueValidator(2023),
            MinValueValidator(2015)
        ]
    )

    def __str__(self):
        return f"{self.car_make.name} {self.name} ({self.year})"
