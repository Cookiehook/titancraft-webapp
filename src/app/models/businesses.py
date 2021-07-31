"""
All data used to create and manage Shops, Farms and their stocks.
These are defined by the user.
"""
from django.contrib.auth.models import User
from django.db import models
from django.utils.text import slugify

from app.models import constants


class Business(models.Model):
    name = models.CharField(max_length=50, unique=True)
    type = models.ForeignKey(constants.BusinessType, on_delete=models.CASCADE)
    slug = models.SlugField()
    description = models.CharField(max_length=1000, blank=True, null=True)
    x_pos = models.IntegerField()
    z_pos = models.IntegerField()

    def __str__(self):
        return f"{self.name} ({self.x_pos}/{self.z_pos})"

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

    # Itemstack for sale
    stock_item = models.ForeignKey(constants.Item, on_delete=models.CASCADE, related_name="stock")
    stock_description = models.CharField(max_length=200, null=True, blank=True)
    stock_stack_size = models.IntegerField()

    # Itemstack accepted as payment
    cost_item = models.ForeignKey(constants.Item, on_delete=models.CASCADE, related_name="cost")
    cost_description = models.CharField(max_length=200, null=True, blank=True)
    cost_stack_size = models.IntegerField()

    units = models.IntegerField()
    last_updated = models.DateTimeField()

    def __str__(self):
        if self.enchantment_set.all():
            labels = " | ".join([str(i) for i in self.enchantment_set.all()])
            return f"{self.business}: {self.stock_stack_size}x {self.stock_item} ({labels}) - {self.cost_stack_size}x {self.cost_item}"
        if self.potion_set.all():
            labels = " | ".join([str(i) for i in self.potion_set.all()])
            return f"{self.business}: {self.stock_stack_size}x {self.stock_item} ({labels}) - {self.cost_stack_size}x {self.cost_item}"
        return f"{self.business}: {self.stock_stack_size}x {self.stock_item} - {self.cost_stack_size}x {self.cost_item}"


class ServiceRecord(models.Model):
    business = models.ForeignKey(Business, on_delete=models.CASCADE)
    name = models.CharField(max_length=1000)
    description = models.CharField(max_length=1000)

    def __str__(self):
        return f"{self.business}: {self.name}"


class FarmRecord(models.Model):
    business = models.ForeignKey(Business, on_delete=models.CASCADE)
    mob = models.ForeignKey(constants.Mob, on_delete=models.CASCADE, null=True, blank=True)
    item = models.ForeignKey(constants.Item, on_delete=models.CASCADE, null=True, blank=True)
    xp = models.BooleanField(default=False)
