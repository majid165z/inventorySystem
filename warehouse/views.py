from django.shortcuts import render, redirect
from .forms import (UnitForm,ProjectForm,
    MaterialRequisitionForm, WarehouseForm,MrItemFromSet,
    ProcurementOrderForm,POItemFromSet,
    PackingListForm,PLItemForm,PLItemFromSet,
    MaterialReceiptSheetForm,MRSItemFromSet,ConditionForm,
    MaterialIssueRequestForm,MIRItemFromSet,CategoryForm,ClusterForm,PipeLineForm
    )
from django.http import HttpRequest,JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import (Project,MaterialRequisition, MrItem, Unit, Warehouse,Item,
POItem, ProcurementOrder,
PackingList,
MaterialReceiptSheet,MRSItem,
Condition,inventoryItem,
MaterialIssueRequest,MIRItem,Category,
Cluster,PipeLine
)
from django.db.models import Sum, Q
from django.views.decorators.csrf import csrf_exempt
from django.forms import inlineformset_factory

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
def category_list(request:HttpRequest):
    units = Category.objects.all()
    context = {'title':'Categories',
    'units':units
    }
    return render(request,'warehouse/category_list.html',context)

@login_required
def category_add(request:HttpRequest):
    user = request.user
    if not user.is_superuser:
        msg = "You don't have the required permission."
        messages.error(request,msg)
        return redirect('category_list')
    form = CategoryForm(request.POST or None)
    if form.is_valid():
        obj = form.save(commit=False)
        obj.created_by = user
        obj.save()
        msg = "The Category was created successfully."
        messages.success(request,msg)
        return redirect('category_list')
    context = {
        'title': "Create Category",
        'form' : form
    }
    return render(request,'warehouse/unit_add.html',context)
@login_required
def category_edit(request:HttpRequest,id):
    user = request.user
    if not user.is_superuser:
        msg = "You don't have the required permission."
        messages.error(request,msg)
        return redirect('category_list')
    instance = Category.objects.get(id=id)
    form = CategoryForm(request.POST or None,instance=instance)
    if form.is_valid():
        obj = form.save()
        msg = "The Categort was edited successfully."
        messages.success(request,msg)
        return redirect('category_list')
    context = {
        'title': "Edit Category",
        'form' : form
    }
    return render(request,'warehouse/unit_add.html',context)

@login_required
def cluster_list(request:HttpRequest):
    units = Cluster.objects.all()
    context = {'title':'Clusters',
    'units':units
    }
    return render(request,'warehouse/cluster_list.html',context)

@login_required
def cluster_add(request:HttpRequest):
    user = request.user
    if not user.is_superuser:
        msg = "You don't have the required permission."
        messages.error(request,msg)
        return redirect('cluster_list')
    form = ClusterForm(request.POST or None)
    if form.is_valid():
        obj = form.save(commit=False)
        obj.created_by = user
        obj.save()
        msg = "The Cluster was created successfully."
        messages.success(request,msg)
        return redirect('cluster_list')
    context = {
        'title': "Create Cluster",
        'form' : form
    }
    return render(request,'warehouse/unit_add.html',context)
@login_required
def cluster_edit(request:HttpRequest,id):
    user = request.user
    if not user.is_superuser:
        msg = "You don't have the required permission."
        messages.error(request,msg)
        return redirect('cluster_list')
    instance = Cluster.objects.get(id=id)
    form = ClusterForm(request.POST or None,instance=instance)
    if form.is_valid():
        obj = form.save()
        msg = "The Categort was edited successfully."
        messages.success(request,msg)
        return redirect('cluster_list')
    context = {
        'title': "Edit Cluster",
        'form' : form
    }
    return render(request,'warehouse/unit_add.html',context)


@login_required
def pipe_line_list(request:HttpRequest):
    units = PipeLine.objects.all()
    context = {'title':'Pipe Line',
    'units':units
    }
    return render(request,'warehouse/pipeline_list.html',context)

@login_required
def pipe_line_add(request:HttpRequest):
    user = request.user
    if not user.is_superuser:
        msg = "You don't have the required permission."
        messages.error(request,msg)
        return redirect('pipe_line_list')
    form = PipeLineForm(request.POST or None)
    if form.is_valid():
        obj = form.save(commit=False)
        obj.created_by = user
        obj.save()
        msg = "The Pipe Line was created successfully."
        messages.success(request,msg)
        return redirect('pipe_line_list')
    context = {
        'title': "Create Pipe Line",
        'form' : form
    }
    return render(request,'warehouse/unit_add.html',context)
@login_required
def pipe_line_edit(request:HttpRequest,id):
    user = request.user
    if not user.is_superuser:
        msg = "You don't have the required permission."
        messages.error(request,msg)
        return redirect('pipe_line_list')
    instance = PipeLine.objects.get(id=id)
    form = PipeLineForm(request.POST or None,instance=instance)
    if form.is_valid():
        obj = form.save()
        msg = "The Pipe Line was edited successfully."
        messages.success(request,msg)
        return redirect('pipe_line_list')
    context = {
        'title': "Edit Pipe Line",
        'form' : form
    }
    return render(request,'warehouse/unit_add.html',context)

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
@csrf_exempt
def mr_list(request:HttpRequest):
    if request.method == 'POST':
        id = request.POST.get('id')
        mr = MaterialRequisition.objects.get(id=id)
        count = mr.pos.all().count()
        if not count:
            if request.user.is_superuser or request.user.technical:
                mr.delete()
                return JsonResponse({
                    "success":True,
                    "msg":f"The MR: {mr.number} was deleted successfully."
                })
            else:
                return JsonResponse({
                    "success":False,
                    "msg":"you dont have required permission."
                })
        else:
            return JsonResponse({
                "success":False,
                "msg":"This MR have been used by some POs. You should delete does POs first."
            })
    else:
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
    units = Unit.objects.all()
    items = Item.objects.all()
    pipes = PipeLine.objects.all()
    clusters = Cluster.objects.all()
    if request.method == 'POST' and form.is_valid():
        obj = form.save(commit=False)
        inline_form = MrItemFromSet(request.POST,instance=obj,
                        form_kwargs={'units':units,
                                    'items':items,
                                    'pipes':pipes,
                                    'clusters':clusters
                                    }
                        )
        if inline_form.is_valid():
            obj.created_by = user
            obj.save()
            inline_form.save()
            msg = 'MR was Created successfully.'
            messages.success(request,msg)
            return redirect('mr_edit',id=obj.id)
        
    if inline_form:
        formset = inline_form
    else:
        formset = MrItemFromSet(request.POST or None,
                                form_kwargs={'units':units,
                                    'items':items,
                                    'pipes':pipes,
                                    'clusters':clusters
                                    }
                                )
        # for form_ in formset:
        #     form_.fields['unit'] = 
        #     form_.fields['item'] = 
        
    context = {
        'title': 'Create MR',
        'form':form,
        'formset':formset
    }
    return render(request,'warehouse/mr-add.html',context)

@login_required
def mr_edit(request:HttpRequest,id):
    user = request.user
    mr = MaterialRequisition.objects.get(id=id)
    units = Unit.objects.all()
    items = Item.objects.all()
    pipes = PipeLine.objects.all()
    clusters = Cluster.objects.all()

    form = MaterialRequisitionForm(request.POST or None,instance=mr)
    inline_form = None
    if form.is_valid():
        obj = form.save()
        inline_form = MrItemFromSet(request.POST,instance=obj,
                            form_kwargs={
                                'units':units,
                                'items':items,
                                'pipes':pipes,
                                'clusters':clusters
                                }
                            )
        if inline_form.is_valid():
            inline_form.save()
            msg = 'MR was edited successfully.'
            messages.success(request,msg)
            return redirect('mr_list')
    if inline_form:
        formset = inline_form
    else:
        formset = MrItemFromSet(form_kwargs={
            'units':units,
            'items':items,
            'pipes':pipes,
            'clusters':clusters
            },instance=mr)
    
    context = {
        'title': 'Edit MR',
        'form':form,
        'formset':formset
    }
    return render(request,'warehouse/mr-add.html',context)

@login_required
@csrf_exempt
def po_list(request:HttpRequest):
    if request.method == 'POST':
        id = request.POST.get('id')
        po = ProcurementOrder.objects.get(id=id)
        count = po.pls.all().count()
        if not count:
            if request.user.is_superuser or request.user.technical:
                po.delete()
                return JsonResponse({
                    "success":True,
                    "msg":f"The PO: {po.number} was deleted successfully."
                })
            else:
                return JsonResponse({
                    "success":False,
                    "msg":"you dont have required permission."
                })
        else:
            return JsonResponse({
                "success":False,
                "msg":"This PO have been used by some PLs. You should delete does Pls first."
            })
    else:
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
        inline_form = POItemFromSet(request.POST,instance=obj)
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
    mr = po.mr
    mritems = [('','---------')] + list(mr.items.all().values_list('id','number'))
    items = Item.objects.filter(mritems__mr=mr)
    items = [("","-------")] + [(item.id, item.__str__()) for item in items]
    units = [("","-------")] + [(item.id, item.__str__()) for item in Unit.objects.all()]
    pipes = [("","--------")]+[(item.id, item.__str__()) for item in PipeLine.objects.all()]
    clusters = [("","--------")]+[(item.id, item.__str__()) for item in Cluster.objects.all()]
    
    
    if request.method == 'POST' and form.is_valid():
        obj = form.save()        
        inline_form = POItemFromSet(request.POST or None,instance=po,form_kwargs={'mritems':mritems,'items':items,'units':units,'pipes':pipes,'clusters':clusters})
        
        
        # inline_form = POItemFromSet(request.POST,instance=po,form_kwargs={'mr':po.mr})
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
        formset = POItemFromSet(request.POST or None,instance=po,form_kwargs={'mritems':mritems,'items':items,'units':units,'pipes':pipes,'clusters':clusters})
        # formset.extra = 2
        # POItemFromSet = inlineformset_factory(
        #     ProcurementOrder,POItem,form=POItemForm,extra=2,
        #     can_delete=True,can_delete_extra=True,
        #     fields=['number','item','unit','quantity','cluster','pipeline']
        # )        
        
        print(formset)
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
@login_required
def condition_list(request:HttpRequest):
    conditions = Condition.objects.all()
    context = {'title':'Item Conditions',
    'units':conditions
    }
    return render(request,'warehouse/condition_list.html',context)

@login_required
def condition_add(request:HttpRequest):
    user = request.user
    if not user.is_superuser:
        msg = "You don't have the required permission."
        messages.error(request,msg)
        return redirect('condition_list')
    form = ConditionForm(request.POST or None)
    if form.is_valid():
        obj = form.save(commit=False)
        obj.created_by = user
        obj.save()
        msg = "The Unit was created successfully."
        messages.success(request,msg)
        return redirect('condition_list')
    context = {
        'title': "Create Condition",
        'form' : form
    }
    return render(request,'warehouse/unit_add.html',context)
@login_required
def condition_edit(request:HttpRequest,id):
    user = request.user
    if not user.is_superuser:
        msg = "You don't have the required permission."
        messages.error(request,msg)
        return redirect('condition_list')
    instance = Condition.objects.get(id=id)
    form = ConditionForm(request.POST or None,instance=instance)
    if form.is_valid():
        obj = form.save()
        msg = "The unit was edited successfully."
        messages.success(request,msg)
        return redirect('condition_list')
    context = {
        'title': "Edit Condition",
        'form' : form
    }
    return render(request,'warehouse/unit_add.html',context)

@login_required
def mrs_list(request:HttpRequest):
    mrss = MaterialReceiptSheet.objects.all()
    context = {
        'title':'Material Receipt Sheet List',
        'mrss':mrss
    }
    return render(request,'warehouse/mrs-list.html',context)

@login_required
def mrs_add(request:HttpRequest):
    user = request.user
    form = MaterialReceiptSheetForm(user,request.POST or None)
    inline_form = None
    if request.method == 'POST' and form.is_valid():
        obj = form.save(commit=False)
        inline_form = MRSItemFromSet(request.POST,instance=obj,form_kwargs={"pl":obj.pl})
        if inline_form.is_valid():
            obj.created_by = user
            obj.vendor = obj.pl.company
            obj.save()
            inline_form.save()
            msg = 'MRS was created successfully.'
            messages.success(request,msg)
            return redirect('mrs_list')
        else:
            print(inline_form.errors)
    else:
        print(form.errors)
    
    context = {
        'title': 'Create Material Receipt Sheet',
        'form':form,
        'formset':inline_form
    }
    return render(request,'warehouse/mrs-add.html',context)

@login_required
def mrs_edit(request:HttpRequest,id):
    user = request.user
    mrs = MaterialReceiptSheet.objects.get(id=id)
    form = MaterialReceiptSheetForm(user,request.POST or None,instance=mrs)
    inline_form = None
    if request.method == 'POST' and form.is_valid():
        obj = form.save()
        inline_form = MRSItemFromSet(request.POST,instance=mrs,form_kwargs={"pl":mrs.pl})
        if inline_form.is_valid():
            inline_form.save()
            msg = 'MRS was edited successfully.'
            messages.success(request,msg)
            return redirect('mrs_list')
        else:
            print(inline_form.errors)
    else:
        print(form.errors)
        
    if inline_form:
        formset = inline_form
    else:
        formset = MRSItemFromSet(request.POST or None,instance=mrs,form_kwargs={"pl":mrs.pl})
        formset.extra = 0

    context = {
        'title': 'Edit MRS',
        'form':form,
        'formset':formset,
        'mrs':mrs,
    }
    return render(request,'warehouse/mrs-add.html',context)

@login_required
def mir_list(request:HttpRequest):
    user = request.user
    if (not user.is_superuser) and (not user.technical):
        msg = "you don't have the required permissions."
        messages.error(request,msg)
        return redirect("home")
    if user.is_superuser:
        mirs = MaterialIssueRequest.objects.all()
    else:
        mirs = MaterialIssueRequest.objects.filter(created_by=user)
    context = {
        'title':'Material Issue Request List',
        'mirs':mirs
    }
    return render(request,'warehouse/mir-list.html',context)

@login_required
def mir_add(request:HttpRequest):
    user = request.user
    if (not user.is_superuser) and (not user.technical):
         msg = "you don't have the required permissions."
         messages.error(request,msg)
         return redirect("home")
    form = MaterialIssueRequestForm(request.POST or None)
    inline_form = None
    if request.method == 'POST' and form.is_valid():
        obj = form.save(commit=False)
        inline_form = MIRItemFromSet(request.POST,instance=obj,form_kwargs={"pl":obj.pl})
        if inline_form.is_valid():
            obj.created_by = user
            obj.save()
            inline_form.save()
            msg = 'MIR was created successfully.'
            messages.success(request,msg)
            return redirect('mir_list')
        else:
            print(inline_form.errors)
    else:
        print(form.errors)
    
    context = {
        'title': 'Create Material Issue Request',
        'form':form,
        'formset':inline_form
    }
    return render(request,'warehouse/mir-add.html',context)

@login_required
def mir_edit(request:HttpRequest,id):
    user = request.user
    if (not user.is_superuser) and (not user.technical):
         msg = "you don't have the required permissions."
         messages.error(request,msg)
         return redirect("home")    
    mir = MaterialIssueRequest.objects.get(id=id)
    if mir.sent_to_warehouse:
        msg = "This MIR has been sent to warehouse and can not be edited."
        return redirect('mir_list')
    form = MaterialIssueRequestForm(request.POST or None,instance=mir)
    inline_form = None
    if request.method == 'POST' and form.is_valid():
        obj = form.save()
        inline_form = MIRItemFromSet(request.POST,instance=mir,form_kwargs={"pl":mir.pl})
        if inline_form.is_valid():
            inline_form.save()
            msg = 'MIR was edited successfully.'
            messages.success(request,msg)
            return redirect('mir_list')
        else:
            print(inline_form.errors)
    else:
        print(form.errors)
        
    if inline_form:
        formset = inline_form
    else:
        formset = MIRItemFromSet(request.POST or None,instance=mir,form_kwargs={"pl":mir.pl})
        formset.extra = 0

    context = {
        'title': 'Edit MIr',
        'form':form,
        'formset':formset,
        'mir':mir,
    }
    return render(request,'warehouse/mir-add.html',context)

@login_required
def send_to_warehouse(request):
    user = request.user
    if (not user.is_superuser) and (not user.technical):
         msg = "you don't have the required permissions."
         messages.error(request,msg)
         return redirect("home")    
    mir = MaterialIssueRequest.objects.get(id=request.POST.get('id',None))
    if mir.sent_to_warehouse:
        msg = "This MIR has been sent to warehouse and can not be edited."
        return redirect('mir_list')
    else:
        if user.is_superuser or user == mir.created_by:
            mir.sent_to_warehouse = True
            mir.save()
            msg = f"The MIR : {mir.number} was sent to {mir.warehouse}"
            messages.success(request,msg)
            return redirect('mir_list')
        else:
            msg = "you don't have the required permissions."
            messages.error(request,msg)
            return redirect("home") 

@login_required
def mir_list_warehouse(request:HttpRequest):
    user = request.user
    if (not user.is_superuser) and (not user.warehouse_keeper):
        msg = "you don't have the required permissions."
        messages.error(request,msg)
        return redirect("home")
    if user.is_superuser:
        mirs = MaterialIssueRequest.objects.filter(sent_to_warehouse=True)
    else:
        mirs = MaterialIssueRequest.objects.filter(sent_to_warehouse=True,warehouse__in=user.whs.all())
    context = {
        'title':'Material Issue Request List',
        'mirs':mirs
    }
    return render(request,'warehouse/mir-list-warehouse.html',context)

@login_required
def send_mir_from_warehouse(request):
    if request.method == 'POST':
        user = request.user
        if user.is_superuser or user.warehouse_keeper:
            mir = MaterialIssueRequest.objects.get(id=request.POST.get('id',None))
            if user.is_superuser:
                if request.POST.get('send_back',None):
                    mir.sent_to_warehouse = False
                    mir.save()
                    msg = "MIR Sent back to Technical unit Successfully."
                    messages.success(request,msg)
                    return redirect("mir_list_warehouse")
                elif request.POST.get('send',None):
                    if not mir.sent_to_location:
                        mir.sent_to_location = True
                        mir.save()
                        msg = "MIR Sent to location  Successfully."
                        messages.success(request,msg)
                        return redirect("mir_list_warehouse")
                        
            else:
                whs = user.whs.all()
                if mir.warehouse in whs:
                    if request.POST.get('send_back',None):
                        mir.sent_to_warehouse = False
                        mir.save()
                        msg = "MIR Sent back to Technical unit Successfully."
                        messages.success(request,msg)
                        return redirect("mir_list_warehouse")
                    elif request.POST.get('send',None):
                        if not mir.sent_to_location:
                            mir.sent_to_location = True
                            mir.save()
                            msg = "MIR Sent to location Successfully."
                            messages.success(request,msg)
                            return redirect("mir_list_warehouse")
                            
                    
                else:
                    msg = "you dont have the required permissions."
                    messages.error(request,msg)
                    return redirect("mir_list_warehouse")
                    
    msg = "you dont have the required permissions."
    messages.error(request,msg)
    return redirect("mir_list_warehouse")
    
        
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
        mritems = [('','---------')] + list(mr.items.all().values_list('id','number'))
        items = Item.objects.filter(mritems__mr=mr)
        items = [("","-------")] + [(item.id, item.__str__()) for item in items]
        units = [("","-------")] + [(item.id, item.__str__()) for item in Unit.objects.all()]
        pipes = [("","--------")]+[(item.id, item.__str__()) for item in PipeLine.objects.all()]
        clusters = [("","--------")]+[(item.id, item.__str__()) for item in Cluster.objects.all()]
        
        formset = POItemFromSet(form_kwargs={'mritems':mritems,'items':items,'units':units,'pipes':pipes,'clusters':clusters})
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
                'cluster':item.cluster.id if item.cluster else False,
                'pipeline':item.pipeline.id if item.pipeline else False

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

@login_required
def get_pl_items(request):
    po_id = request.GET.get('po_id',None)
    if po_id:
        pls = PackingList.objects.filter(po__id=po_id)
        return render(request,'warehouse/partials/pl_items.html',context={'pls':pls})
@login_required
def get_mrs_formset(request):
    pl_id = request.GET.get('pl_id',None)
    if pl_id:
        pl = PackingList.objects.get(id=pl_id)
        formset = MRSItemFromSet(form_kwargs={'pl':pl})
        return render(request,'warehouse/partials/mrs_form.html',context={'formset':formset})

@login_required
def get_mir_formset(request):
    pl_id = request.GET.get('pl_id',None)
    if pl_id:
        pl = PackingList.objects.get(id=pl_id)
        formset = MIRItemFromSet(form_kwargs={'pl':pl})
        return render(request,'warehouse/partials/mir_form.html',context={'formset':formset})
@login_required
def get_pl_warehouse(request):
    pl_id = request.GET.get('pl_id',None)
    if pl_id:
        whs = Warehouse.objects.filter(mrs__pl__id=pl_id).distinct()
        return render(request,'warehouse/partials/pl_warehouse.html',context={'whs':whs})

@login_required
def get_warehouse_items(request):
    wh_id = request.GET.get('id',None)
    if wh_id:
        # items = Item.objects.filter(mrsitems__mrs__warehouse__id=wh_id).annotate
        items = inventoryItem.objects.filter(warehouse__id=wh_id)
        return render(request,'warehouse/partials/warehouse_items.html',context={'items':items})
# @login_required
# def get_po_items(request):
#     po_id = request.GET.get('id',None)
#     if po_id:
#         items = POItem.objects.filter(po__id=po_id).values_list('number')
#         items = MrItem.objects.filter(id__in=items).values_list('id','number')
#         return JsonResponse({'items':list(items)})
@login_required
def get_mir_details(request):
    user = request.user
    id = request.GET.get('id',None)
    if id:
        mir = MaterialIssueRequest.objects.get(id=id)
        return render(request,'warehouse/partials/mir_details.html',context={'mir':mir})

@login_required
def get_items_ajax(request):
    term = request.GET.get("term",None)
    if term:
        items = Item.objects.filter(name__contains=term)
        items = [{"id":item.id,"text":item.name} for item in items]
        return JsonResponse({"results":items})
    else:
        return JsonResponse({})
    