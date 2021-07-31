from django.contrib import admin
from app.models import constants, itemstacks, locations, users

admin.site.register(constants.Region)
admin.site.register(constants.Mob)
admin.site.register(constants.Item)
admin.site.register(constants.EnchantmentLevel)
admin.site.register(constants.EnchantmentType)
admin.site.register(constants.PotionType)
admin.site.register(constants.ItemClass)
admin.site.register(constants.ItemIcon)

admin.site.register(locations.Location)
admin.site.register(locations.Maintainer)
admin.site.register(locations.StockRecord)
admin.site.register(locations.ServiceRecord)
admin.site.register(locations.FarmRecord)

admin.site.register(itemstacks.Enchantment)
admin.site.register(itemstacks.Potion)

admin.site.register(users.UserDetails)
