from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from decimal import Decimal

units = [
    ('km2', 'Square kilometre'),
    ('m2', 'Square metre'),
]

animals = [
    ('lion', 'lion'),
    ('monkey', 'monkey'),
    ('tiger', 'tiger'),
    ('elephant', 'elephant')
]


class ZOO(models.Model):
    title = models.CharField(max_length=256, unique=True)
    total_area = models.FloatField(default=3.4)
    free_area = models.FloatField(default=0.0)
    unit = models.CharField(choices=units, max_length=20)

    def get_free_area(self) -> float:
        all_aviaries = ZOO.objects.get(pk=self.pk).aviaries.all()
        occupied_area = Decimal('0.0')
        for area in all_aviaries:
            if area.unit == 'm2':
                occupied_area += Decimal(str(area.total_area)) / Decimal('1000000.0')
            else:
                occupied_area += Decimal(str(area.total_area))
        return Decimal(str(self.total_area)) - occupied_area

    def clean(self):
        super().clean()
        self.free_area = self.get_free_area()
        if self.free_area < 0:
            raise ValidationError(_("No free territory"))

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        super().save()

    def __str__(self):
        return self.title


class Aviary(models.Model):
    total_area = models.FloatField()
    free_area = models.FloatField(default=1)
    occupied_place = models.FloatField(default=0)
    unit = models.CharField(choices=units, default=units[1][0], max_length=20)
    zoo = models.ForeignKey(to=ZOO, on_delete=models.PROTECT, related_name='aviaries')
    typeOfAnimals = models.CharField(max_length=20, choices=animals)
    required_area = models.FloatField()
    amount_animals = models.IntegerField(default=0)

    def set_free_area(self):
        return self.total_area - (self.required_area * self.amount_animals)

    def clean(self):
        super().clean()
        self.free_area = self.set_free_area()
        if not self.free_area >= 0:
            raise ValidationError(_('Not enough space for all animals'))
        if Decimal(str(self.total_area)) / Decimal('1000000.0') >= Decimal(str(self.zoo.total_area)):
            raise ValidationError(_('The enclosure area exceeds the available area of the zoo'))

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        self.occupied_place = self.total_area - self.free_area
        super().save()
        self.__update_zoo()

    def __update_zoo(self):
        zoo = ZOO.objects.get(pk=self.zoo.pk)
        zoo.free_area = zoo.get_free_area()
        zoo.save()

    def __str__(self):
        return f'Zoo: {self.zoo}; Aviary type: {self.typeOfAnimals}'




