"""
All data used to create and manage Shops, Farms and their stocks.
These are defined by the user.
"""
from django.contrib.auth.models import User
from django.db import models
from django.utils.text import slugify

from app.models import constants, itemstacks


class Business(models.Model):
    name = models.CharField(max_length=50, unique=True)
    type = models.ForeignKey(constants.BusinessType, on_delete=models.CASCADE)
    slug = models.SlugField()
    description = models.CharField(max_length=1000, blank=True, null=True)
    x_pos = models.IntegerField()
    y_pos = models.IntegerField()

    def __str__(self):
        return f"{self.name} ({self.x_pos}/{self.y_pos})"

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        self.slug = slugify(self.name)
        super(Business, self).save(force_insert, force_update, using, update_fields)


class StaffMember(models.Model):
    business = models.ForeignKey(Business, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.business} - {self.user}"


class StockRecord(models.Model):
    business = models.ForeignKey(Business, on_delete=models.CASCADE)
    item = models.ForeignKey(itemstacks.ItemStack, on_delete=models.CASCADE)
    cost = models.ForeignKey(itemstacks.ItemStack, on_delete=models.CASCADE, related_name='currency')
    units = models.IntegerField()
    last_updated = models.DateTimeField()

    def __str__(self):
        return f"{self.business}: {self.item} - {self.cost}"


class ServiceRecord(models.Model):
    business = models.ForeignKey(Business, on_delete=models.CASCADE)
    name = models.CharField(max_length=1000)
    description = models.CharField(max_length=1000)

    def __str__(self):
        return f"{self.business}: {self.name}"
