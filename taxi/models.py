from django.db import models
from django.contrib.auth.models import AbstractUser
from django.forms import ValidationError
from django.urls import reverse


class Manufacturer(models.Model):
    name = models.CharField(max_length=255, unique=True)
    country = models.CharField(max_length=255)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return f"{self.name} {self.country}"


class Driver(AbstractUser):
    license_number = models.CharField(max_length=255, unique=True)

    class Meta:
        verbose_name = "driver"
        verbose_name_plural = "drivers"

    def clean(self):
        license_number = self.license_number

        if len(license_number) != 8:
            raise ValidationError("License number must be exactly 8 characters long.")

        letters = license_number[:3]
        digits = license_number[3:]

        if not letters.isalpha() or not letters.isupper():
            raise ValidationError("First 3 characters must be uppercase letters.")

        if not digits.isdigit():
            raise ValidationError("Last 5 characters must be digits.")

    def __str__(self):
        return f"{self.username} ({self.first_name} {self.last_name})"

    def get_absolute_url(self):
        return reverse("taxi:driver-detail", kwargs={"pk": self.pk})


class Car(models.Model):
    model = models.CharField(max_length=255)
    manufacturer = models.ForeignKey(Manufacturer, on_delete=models.CASCADE)
    drivers = models.ManyToManyField(Driver, related_name="cars")

    def __str__(self):
        return self.model
