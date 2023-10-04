from django.urls import path,reverse
from django.contrib.auth import views as auth_views
from . import views
urlpatterns = [
    # warehouse urls
    path('warehouse-add',views.warehouse_add,name='warehouse_add'),
    path('warehouse-list',views.warehouse_list,name='warehouse_list'),
    path('warehouse-edit/<int:id>',views.warehouse_edit,name='warehouse_edit'),
    path('get-warehouse-keepers',views.get_warehouse_keepers,name='get_warehouse_keepers'),

    # unit urls
    path('unit-add',views.unit_add,name='unit_add'),
    path('unit-list',views.unit_list,name='unit_list'),
    path('unit-edit/<int:id>',views.unit_edit,name='unit_edit'),

    # project urls
    path('project-add',views.project_add,name='project_add'),
    path('proejct-list',views.project_list,name='project_list'),
    path('poject-edit/<int:id>',views.project_edit,name='project_edit'),

    # material requisition urls
    path('material-requisition-add',views.mr_add,name='mr_add'),
    path('material-requisition-list',views.mr_list,name='mr_list'),
    path('material-requisition-edit/<int:id>',views.mr_edit,name='mr_edit'),
    # procurment order urls
    path('procurment-order-add',views.po_add,name='po_add'),
    path('procurment-order-list',views.po_list,name='po_list'),
    path('procurment-order-edit/<int:id>',views.po_edit,name='po_edit'),
    # packing list urls
    path('packing-list-add',views.pl_add,name='pl_add'),
    path('packing-list-list',views.pl_list,name='pl_list'),
    path('packing-list-edit/<int:id>',views.pl_edit,name='pl_edit'),

    # AJAX calls ----------------------------------------
    path('ajax/create_item_name',views.create_item_name,name='create_item_name'),
    path('ajax/get_project_mr',views.get_project_mr,name='get_project_mr'),
    path('ajax/get_po_formset',views.get_po_formset,name='get_po_formset'),
    # path('get_mr_item_numbers',views.get_mr_item_numbers,name='get_mr_item_numbers'),
    path('ajax/get_item_desc',views.get_item_desc,name='get_item_desc'),
    path('ajax/get_po_list',views.get_po_list,name='get_po_list'),
    path('ajax/get_pl_formset',views.get_pl_formset,name='get_pl_formset'),
    # path('get_po_items',views.get_po_items,name='get_po_items'),
]
