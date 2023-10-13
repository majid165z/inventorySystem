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
    # Condition urls
    path('condition-list',views.condition_list,name='condition_list'),
    path('condition-add',views.condition_add,name='condition_add'),
    path('condition-edit/<int:id>',views.condition_edit,name='condition_edit'),
    # categories urls
    path('category-list',views.category_list,name='category_list'),
    path('category-add',views.category_add,name='category_add'),
    path('category-edit/<int:id>',views.category_edit,name='category_edit'),
    # clusters urls
    path('cluster-list',views.cluster_list,name='cluster_list'),
    path('cluster-add',views.cluster_add,name='cluster_add'),
    path('cluster-edit/<int:id>',views.cluster_edit,name='cluster_edit'),
    # pipe line urls
    path('pipe-line-list',views.pipe_line_list,name='pipe_line_list'),
    path('pipe-line-add',views.pipe_line_add,name='pipe_line_add'),
    path('pipe-line-edit/<int:id>',views.pipe_line_edit,name='pipe_line_edit'),


    # Material Reciept Sheet Urls
    path('material-receipt-sheet-add',views.mrs_add,name='mrs_add'),
    path('material-receipt-sheet-list',views.mrs_list,name='mrs_list'),
    path('material-receipt-sheet-edit/<int:id>',views.mrs_edit,name='mrs_edit'),
    
    # material Issue request urls
    path('material-issue-request-list',views.mir_list,name='mir_list'),
    path('material-issue-request-add',views.mir_add,name='mir_add'),
    path('material-issue-request-edit/<int:id>',views.mir_edit,name='mir_edit'),
    path('send_to_warehouse',views.send_to_warehouse,name='send_to_warehouse'),
    path('mir-list-warehouse',views.mir_list_warehouse,name='mir_list_warehouse'),
    path('send_mir_from_warehouse',views.send_mir_from_warehouse,name='send_mir_from_warehouse'),
    
    # AJAX calls ----------------------------------------
    path('ajax/create_item_name',views.create_item_name,name='create_item_name'),
    path('ajax/get_project_mr',views.get_project_mr,name='get_project_mr'),
    path('ajax/get_po_formset',views.get_po_formset,name='get_po_formset'),
    # path('get_mr_item_numbers',views.get_mr_item_numbers,name='get_mr_item_numbers'),
    path('ajax/get_item_desc',views.get_item_desc,name='get_item_desc'),
    path('ajax/get_po_list',views.get_po_list,name='get_po_list'),
    path('ajax/get_pl_formset',views.get_pl_formset,name='get_pl_formset'),
    path('ajax/get_pl_items',views.get_pl_items,name='get_pl_items'),
    path('ajax/get_mrs_formset',views.get_mrs_formset,name='get_mrs_formset'),
    path('ajax/get_warehouse_items',views.get_warehouse_items,name='get_warehouse_items'),
    path('ajax/get_mir_formset',views.get_mir_formset,name='get_mir_formset'),
    path('ajax/get_pl_warehouse',views.get_pl_warehouse,name='get_pl_warehouse'),
    path('ajax/get_mir_details',views.get_mir_details,name='get_mir_details'),
    path('ajax/get_items_ajax',views.get_items_ajax,name='get_items_ajax')
    # path('get_po_items',views.get_po_items,name='get_po_items'),
]
