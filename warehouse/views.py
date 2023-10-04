from django.shortcuts import render, redirect
from .forms import (UnitForm,ProjectForm,
    MaterialRequisitionForm, WarehouseForm,MrItemFromSet,
    ProcurementOrderForm,POItemFromSet,
    PackingListForm,PLItemForm,PLItemFromSet
    )
from django.http import HttpRequest,JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import (Project,MaterialRequisition, MrItem, Unit, Warehouse,Item,
POItem, ProcurementOrder,
PackingList
)
# Create your views here.

@login_required
def warehouse_list(request:HttpRequest):
    user = request.user
    if not user.is_superuser:
        msg = "You don't have the required permission."
        messages.error(request,msg)
        return redirect('home')
    warehouses = Warehouse.objects.all()
    context = {'warehouses':warehouses}
    return render(request,'warehouse/list.html',context)
    

@login_required
def warehouse_add(request:HttpRequest):
    user = request.user
    form = WarehouseForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        obj = form.save(commit=False)
        obj.created_by = user
        obj.save()
        form.save_m2m()
        msg = 'The warehouse was created successfully.'
        messages.success(request,msg)
        return redirect('warehouse_list')
    context = {
        'form':form,
        'user':user,
        'title':"Create Warehouse"
    }
    return render(request,'warehouse/warehouse_add.html',context)

@login_required
def warehouse_edit(request:HttpRequest,id):
    user = request.user
    if not user.is_superuser:
        msg = "You don't have the required permission."
        messages.error(request,msg)
        return redirect('warehouse_list')
    warehouse = Warehouse.objects.get(id=id)
    form = WarehouseForm(request.POST or None,instance=warehouse)
    if request.method == 'POST' and form.is_valid():
        obj = form.save()
        msg = "The warehouse was edited successfully."
        messages.success(request,msg)
        return redirect('warehouse_list')
    context = {
        'form':form,
        'user':user,
        "title":"Edit Warehouse"
    }
    return render(request,'warehouse/warehouse_add.html',context)

@login_required
def get_warehouse_keepers(request:HttpRequest):
    id = request.GET.get('id',None)
    if id:
        wh = Warehouse.objects.get(id=id)
        users = wh.users.all()
        return render(request,'warehouse/get_warehouse_keepers.html',context={'users':users})

@login_required
def unit_list(request:HttpRequest):
    units = Unit.objects.all()
    context = {'title':'Units',
    'units':units
    }
    return render(request,'warehouse/unit_list.html',context)

@login_required
def unit_add(request:HttpRequest):
    user = request.user
    if not user.is_superuser:
        msg = "You don't have the required permission."
        messages.error(request,msg)
        return redirect('unit_list')
    form = UnitForm(request.POST or None)
    if form.is_valid():
        obj = form.save(commit=False)
        obj.created_by = user
        obj.save()
        msg = "The Unit was created successfully."
        messages.success(request,msg)
        return redirect('unit_list')
    context = {
        'title': "Create Unit",
        'form' : form
    }
    return render(request,'warehouse/unit_add.html',context)
@login_required

def unit_edit(request:HttpRequest,id):
    user = request.user
    if not user.is_superuser:
        msg = "You don't have the required permission."
        messages.error(request,msg)
        return redirect('unit_list')
    instance = Unit.objects.get(id=id)
    form = UnitForm(request.POST or None,instance=instance)
    if form.is_valid():
        obj = form.save()
        msg = "The unit was edited successfully."
        messages.success(request,msg)
        return redirect('unit_list')
    context = {
        'title': "Edit Unit",
        'form' : form
    }
    return render(request,'warehouse/unit_add.html',context)

@login_required
def project_list(request:HttpRequest):
    projects = Project.objects.all()
    context = {
        'title':'Projects List',
        'projects':projects
    }
    return render(request,'warehouse/project-list.html',context)

@login_required
def project_add(request:HttpRequest):
    user = request.user
    if not user.is_superuser:
        msg = "You don't have the required permission."
        messages.error(request,msg)
        return redirect('project_list')
    form = ProjectForm(request.POST or None)
    if form.is_valid():
        obj = form.save(commit=False)
        obj.created_by = user
        obj.save()
        msg = "The Project was created successfully."
        messages.success(request,msg)
        return redirect('project_list')
    context = {
        'title': 'Create Project',
        'form' : form
    }
    return render(request,'warehouse/project_add.html',context)

@login_required
def project_edit(request:HttpRequest,id):
    user = request.user
    if not user.is_superuser:
        msg = "You don't have the required permission."
        messages.error(request,msg)
        return redirect('project_list')
    project = Project.objects.get(id=id)
    form = ProjectForm(request.POST or None,instance=project)
    if form.is_valid():
        obj = form.save()
        msg = 'The Project was edited successfully.'
        messages.success(request,msg)
        return redirect('project_list')
    context = {
        'title': 'Edit Project',
        'form' : form
    }
    return render(request,'warehouse/project_add.html',context)

@login_required
def mr_list(request:HttpRequest):
    mrs = MaterialRequisition.objects.all()
    context = {
        'title':'MR List',
        'mrs':mrs
    }
    return render(request,'warehouse/mr-list.html',context)

@login_required
def mr_add(request:HttpRequest):
    user = request.user
    form = MaterialRequisitionForm(request.POST or None)
    inline_form = None
    if request.method == 'POST' and form.is_valid():
        obj = form.save(commit=False)
        inline_form = MrItemFromSet(request.POST,instance=obj)
        if inline_form.is_valid():
            obj.created_by = user
            obj.save()
            inline_form.save()
            msg = 'MR was Created successfully.'
            messages.success(request,msg)
            return redirect('mr_list')
        
    
    context = {
        'title': 'Create MR',
        'form':form,
        'formset':inline_form or MrItemFromSet(request.POST or None)
    }
    return render(request,'warehouse/mr-add.html',context)

@login_required
def mr_edit(request:HttpRequest,id):
    user = request.user
    mr = MaterialRequisition.objects.get(id=id)
    form = MaterialRequisitionForm(request.POST or None,instance=mr)
    inline_form = None
    if form.is_valid():
        obj = form.save()
        inline_form = MrItemFromSet(request.POST,instance=obj)
        if inline_form.is_valid():
            inline_form.save()
            msg = 'MR was edited successfully.'
            messages.success(request,msg)
            return redirect('mr_list')
        
    
    context = {
        'title': 'Edit MR',
        'form':form,
        'formset':inline_form or MrItemFromSet(request.POST or None,instance=mr)
    }
    return render(request,'warehouse/mr-add.html',context)

@login_required
def po_list(request:HttpRequest):
    pos = ProcurementOrder.objects.all()
    context = {
        'title':'PO List',
        'pos':pos
    }
    return render(request,'warehouse/po-list.html',context)

@login_required
def po_add(request:HttpRequest):
    user = request.user
    form = ProcurementOrderForm(request.POST or None)
    inline_form = None
    items = None
    if request.method == 'POST' and form.is_valid():
        obj = form.save(commit=False)
        inline_form = POItemFromSet(request.POST,instance=obj,form_kwargs={"mr":obj.mr})
        if inline_form.is_valid():
            obj.created_by = user
            obj.save()
            inline_form.save()
            msg = 'PO was created successfully.'
            messages.success(request,msg)
            return redirect('po_list')
    
    context = {
        'title': 'Create PO',
        'form':form,
        'formset':inline_form,
        'items':items
    }
    return render(request,'warehouse/po-add.html',context)

@login_required
def po_edit(request:HttpRequest,id):
    user = request.user
    po = ProcurementOrder.objects.get(id=id)
    form = ProcurementOrderForm(request.POST or None,instance=po)
    inline_form = None
    if form.is_valid():
        obj = form.save()
        inline_form = POItemFromSet(request.POST,instance=po,form_kwargs={'mr':po.mr})
        if inline_form.is_valid():
            inline_form.save()
            msg = 'PO was edited successfully.'
            messages.success(request,msg)
            return redirect('po_list')
        else:
            print(inline_form.errors)
    else:
        print(form.errors)
        
    if inline_form:
        formset = inline_form
    else:
        formset = POItemFromSet(request.POST or None,instance=po,form_kwargs={'mr':po.mr})
        formset.extra = 0

    context = {
        'title': 'Edit PO',
        'form':form,
        'formset':formset,
        'po':po
    }
    return render(request,'warehouse/po-add.html',context)

@login_required
def pl_list(request:HttpRequest):
    pls = PackingList.objects.all()
    context = {
        'title':'Packing List',
        'pls':pls
    }
    return render(request,'warehouse/pl-list.html',context)

@login_required
def pl_add(request:HttpRequest):
    user = request.user
    form = PackingListForm(request.POST or None)
    inline_form = None
    if request.method == 'POST' and form.is_valid():
        obj = form.save(commit=False)
        inline_form = PLItemFromSet(request.POST,instance=obj,form_kwargs={"po":obj.po})
        if inline_form.is_valid():
            obj.created_by = user
            obj.save()
            inline_form.save()
            msg = 'Packing List was created successfully.'
            messages.success(request,msg)
            return redirect('pl_list')
    
    context = {
        'title': 'Create Packing List',
        'form':form,
        'formset':inline_form
    }
    return render(request,'warehouse/pl-add.html',context)

@login_required
def pl_edit(request:HttpRequest,id):
    user = request.user
    pl = PackingList.objects.get(id=id)
    form = PackingListForm(request.POST or None,instance=pl)
    inline_form = None
    if request.method == 'POST' and form.is_valid():
        obj = form.save()
        inline_form = PLItemFromSet(request.POST,instance=pl,form_kwargs={"po":pl.po})
        if inline_form.is_valid():
            inline_form.save()
            msg = 'Packing List was created successfully.'
            messages.success(request,msg)
            return redirect('pl_list')
        else:
            print(inline_form.errors)
    else:
        print(form.errors)
        
    if inline_form:
        formset = inline_form
    else:
        formset = PLItemFromSet(request.POST or None,instance=pl,form_kwargs={"po":pl.po})
        formset.extra = 0

    context = {
        'title': 'Edit Packing List',
        'form':form,
        'formset':formset,
        'pl':pl,
    }
    return render(request,'warehouse/pl-add.html',context)


# # -----------------------------------
# # ajax calls
# # -----------------------------------
@login_required
def create_item_name(request):
    name = request.GET.get('name',None)
    if name:
        obj , created = Item.objects.get_or_create(name=name)
        return JsonResponse({'id':obj.id})

@login_required
def get_po_formset(request):
    mr_id = request.GET.get('mr_id',None)
    if mr_id:
        mr = MaterialRequisition.objects.get(id=mr_id)
        formset = POItemFromSet(form_kwargs={'mr':mr})
        return render(request,'warehouse/partials/po_form.html',context={'formset':formset})
@login_required
def get_project_mr(request:HttpRequest):
    project_id = request.GET.get('id',None)
    if project_id:
        mrs = MaterialRequisition.objects.filter(project__id=project_id)
        return render(request,'warehouse/partials/get_project_mrs.html',context = {
            'mrs':mrs
        })
# @login_required
# def get_mr_item_numbers(request:HttpRequest):
#     mr_id = request.GET.get('id',None)
#     if mr_id:
#         mritems = MrItem.objects.filter(mr__id=mr_id).values_list('id','number')
#         return JsonResponse({'items':list(mritems)})
#         # print(list(mritems),mritems)
#         # return render(request,'warehouse/partials/get_project_mrs.html',context = {
#         #     'mrs':mrs
#         # })

@login_required
def get_item_desc(request:HttpRequest):
    item_id = request.GET.get('id',None)
    if item_id:
        item = MrItem.objects.get(id=item_id)
        return JsonResponse(
            {
                'name':item.item.id,
                'unit':item.unit.id,

            }
        )

@login_required
def get_po_list(request):
    mr_id = request.GET.get('id',None)
    if mr_id:
        pos = ProcurementOrder.objects.filter(mr__id=mr_id).values_list('id','number')
        return JsonResponse({'items':list(pos)})
@login_required
def get_pl_formset(request):
    po_id = request.GET.get('po_id',None)
    if po_id:
        po = ProcurementOrder.objects.get(id=po_id)
        formset = PLItemFromSet(form_kwargs={'po':po})
        return render(request,'warehouse/partials/pl_form.html',context={'formset':formset})

# @login_required
# def get_po_items(request):
#     po_id = request.GET.get('id',None)
#     if po_id:
#         items = POItem.objects.filter(po__id=po_id).values_list('number')
#         items = MrItem.objects.filter(id__in=items).values_list('id','number')
#         return JsonResponse({'items':list(items)})
