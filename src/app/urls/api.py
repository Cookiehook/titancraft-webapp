from django.urls import include, path
from rest_framework import routers

import app.views.api.constants as constants_views
import app.views.api.itemstacks as itemstacks_views
import app.views.api.businesses as businesses_views
import app.views.api.users as users_views

router_v1 = routers.DefaultRouter()

router_v1.register('constants/business_type', constants_views.BusinessTypeViewSet)
router_v1.register('constants/item', constants_views.ItemViewSet)
router_v1.register('constants/potion_type', constants_views.PotionTypeViewSet)
router_v1.register('constants/potion_modifier', constants_views.PotionModifierViewSet)
router_v1.register('constants/enchantment_type', constants_views.EnchantmentTypeViewSet)
router_v1.register('constants/enchantment_level', constants_views.EnchantmentLevelViewSet)
router_v1.register('constants/item_class', constants_views.ItemClassViewSet)
router_v1.register('constants/item_icon', constants_views.ItemIconViewSet)

router_v1.register('itemstacks/itemstack', itemstacks_views.ItemStackViewSet)
router_v1.register('itemstacks/enchantment', itemstacks_views.EnchantmentViewSet)
router_v1.register('itemstacks/potion', itemstacks_views.PotionViewSet)
router_v1.register('itemstacks/potion_modifier_to_potion', itemstacks_views.PotionModifierToPotionViewSet)
router_v1.register('itemstacks/enchantment_to_itemstack', itemstacks_views.EnchantmentToItemStackViewSet)
router_v1.register('itemstacks/potion_to_itemstack', itemstacks_views.PotionToItemStackStackViewSet)

router_v1.register('businesses/business', businesses_views.BusinessViewSet)
router_v1.register('businesses/staff_member', businesses_views.StaffMemberViewSet)
router_v1.register('businesses/stock_record', businesses_views.StockRecordViewSet)
router_v1.register('businesses/service_record', businesses_views.ServiceRecordViewSet)

router_v1.register('users/users', users_views.UserViewSet)
router_v1.register('users/user_details', users_views.UserDetailsViewSet)


urlpatterns = [
    path('v1/', include(router_v1.urls)),
]
