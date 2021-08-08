from django.contrib import admin

from app.models import constants, locations, stock, users

admin.site.register(constants.Region)
admin.site.register(constants.Mob)
admin.site.register(constants.Item)
admin.site.register(constants.Enchantment)
admin.site.register(constants.Potion)
admin.site.register(constants.ItemClass)
admin.site.register(constants.ItemIcon)

admin.site.register(locations.Path)
admin.site.register(locations.PathLink)

admin.site.register(locations.Location)
admin.site.register(locations.Maintainer)
admin.site.register(stock.StockRecord)
admin.site.register(stock.ItemStackToStockRecord)
admin.site.register(stock.EnchantmentToItemStack)
admin.site.register(stock.PotionToItemStack)
admin.site.register(stock.ServiceRecord)
admin.site.register(stock.FarmRecord)

admin.site.register(users.UserDetails)
