from django.db import models
from django.shortcuts import reverse

# Create your models here.
class Easy(models.Model):
    text  = models.TextField(max_length=200, db_index=True)
    use   = models.BooleanField(null = True)


class Medium(models.Model):
    text  = models.TextField(max_length=200, db_index=True)
    use   = models.BooleanField(null = True)


class HardForWomen(models.Model):
    text  = models.TextField(max_length=200, db_index=True)
    use   = models.BooleanField(null = True)


class HardForMen(models.Model):
    text  = models.TextField(max_length=200, db_index=True)
    use   = models.BooleanField(null = True)


class Bonus(models.Model):
    text  = models.TextField(max_length=200, db_index=True)
    use   = models.BooleanField(null = True)


class Action(models.Model):
    text  = models.TextField(max_length=100, db_index=True)
    use   = models.BooleanField(null = True)
