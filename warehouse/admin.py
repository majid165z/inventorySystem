import warehouse
from django.contrib import admin

from .models import (Item,Unit,Warehouse,MrItem,MaterialRequisition,
# ProcurementOrder,POItem,PackingList,PLItem
)
# Register your models here.
admin.site.register(Item)
admin.site.register(Unit)
admin.site.register(Warehouse)
admin.site.register(MrItem)
admin.site.register(MaterialRequisition)
# admin.site.register(ProcurementOrder)
# admin.site.register(POItem)
# admin.site.register(PackingList)
# admin.site.register(PLItem)