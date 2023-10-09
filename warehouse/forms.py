from django import forms
from .models import (Item,Warehouse,Unit,Project,MaterialRequisition,MrItem,
    POItem,ProcurementOrder,
    PackingList,PLItem,MaterialReceiptSheet,MRSItem,Condition,
    MaterialIssueRequest,MIRItem
    )
from jalali_date.fields import JalaliDateField, SplitJalaliDateTimeField
from jalali_date.widgets import AdminJalaliDateWidget, AdminSplitJalaliDateTime
from django.forms import inlineformset_factory
from django.contrib.auth import get_user_model
class WarehouseForm(forms.ModelForm):
    class Meta:
        model = Warehouse
        fields = ['name','address','users']

class UnitForm(forms.ModelForm):
    class Meta:
        model = Unit
        fields = ['name','abrv']

class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['name','number']

class MaterialRequisitionForm(forms.ModelForm):
    class Meta:
        model = MaterialRequisition
        fields = ['number','date','project']
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['date'] = JalaliDateField(label='Approved Date', 
            widget=AdminJalaliDateWidget 
        )

class MrItemForm(forms.ModelForm):
    class Mata:
        model = MrItem
        fields = ['number','tag_number','item','unit','quantity']

MrItemFromSet = inlineformset_factory(
    MaterialRequisition,MrItem,form=MrItemForm,extra=2,
    can_delete=True,can_delete_extra=True,
    fields=['number','tag_number','item','unit','quantity']
)

class ProcurementOrderForm(forms.ModelForm):
    class Meta:
        model = ProcurementOrder
        fields = ['project','number','mr','date','company',        ]
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.pk:
            self.fields['mr'].queryset = self.fields['mr'].queryset.filter(project=self.instance.project)
        self.fields['date'] = JalaliDateField(label='PO Date', 
            widget=AdminJalaliDateWidget 
        )

class POItemForm(forms.ModelForm):
    class Mata:
        model = MrItem
        fields = ['number','item','unit','quantity']
    def __init__(self, *args, **kwargs):
        mr = kwargs.pop('mr',None)
        super().__init__(*args, **kwargs)
        if mr:
            mritems = [('','---------')] + list(mr.items.all().values_list('id','number'))
            self.fields['number'].widget = forms.Select(choices=mritems)
            self.fields['item'].queryset = Item.objects.filter(mritems__mr=mr)
        
        # if self.instance.pk:
        #     mritems = self.instance.po.mr.items.all().values_list('id','number')
        #     self.fields['number'].widget = forms.Select(choices=mritems)
        #     # self.fields['number'].choices = mritems
        # else:
        #     self.fields['number'].widget = forms.Select()


POItemFromSet = inlineformset_factory(
    ProcurementOrder,POItem,form=POItemForm,extra=2,
    can_delete=True,can_delete_extra=True,
    fields=['number','item','unit','quantity']
)

class PackingListForm(forms.ModelForm):
    class Meta:
        model = PackingList
        fields = ['project','number','mr','po','date',        ]
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.pk:
            self.fields['mr'].queryset = self.fields['mr'].queryset.filter(project=self.instance.project)
            self.fields['po'].queryset = self.fields['po'].queryset.filter(mr=self.instance.mr)
        self.fields['date'] = JalaliDateField(label='Packing List Date', 
            widget=AdminJalaliDateWidget 
        )

class PLItemForm(forms.ModelForm):
    class Mata:
        model = PLItem
        fields = ['number','item','unit','quantity']
    def __init__(self, *args, **kwargs):
        po = kwargs.pop('po',None)
        super().__init__(*args, **kwargs)
        if po:
            poitems = list(po.items.all().values_list('number',flat=True))
            mr_items = [("","-------")] + list(MrItem.objects.filter(id__in=poitems).values_list('id','number'))
            self.fields['number'].widget = forms.Select(choices=mr_items)
            self.fields['item'].queryset = Item.objects.filter(poitems__po=po)
        
        
        # if self.instance.pk:
        #     poitems = self.instance.pl.po.items.all().values_list('number')
        #     mritems = MrItem.objects.filter(id__in=poitems).values_list('id','number')
        #     self.fields['number'].widget = forms.Select(choices=mritems)
        #     # self.fields['number'].choices = mritems
        # else:
        #     self.fields['number'].widget = forms.Select()


PLItemFromSet = inlineformset_factory(
    PackingList,PLItem,form=PLItemForm,extra=2,
    can_delete=True,can_delete_extra=True,
    fields=['number','item','unit','quantity']
)

class MaterialReceiptSheetForm(forms.ModelForm):
    class Meta:
        model = MaterialReceiptSheet
        fields = ['project','number','mr','po','pl','warehouse']
    def __init__(self,user, *args, **kwargs):
        self.user = user
        super().__init__(*args, **kwargs)
        if self.user:
            whs = user.whs.all()
            self.fields['warehouse'].queryset = whs

        if self.instance.pk:
            self.fields['mr'].queryset = self.fields['mr'].queryset.filter(project=self.instance.project)
            self.fields['po'].queryset = self.fields['po'].queryset.filter(mr=self.instance.mr)
            self.fields['pl'].queryset = self.fields['pl'].queryset.filter(mr=self.instance.mr)

class MRSItemForm(forms.ModelForm):
    class Mata:
        model = MRSItem
        fields = ['number','item','unit','quantity','condition','loc']
    def __init__(self, *args, **kwargs):
        pl = kwargs.pop('pl',None)
        super().__init__(*args, **kwargs)
        if pl:
            plitems = list(pl.items.all().values_list('number',flat=True))
            mr_items = [("","-------")] + list(MrItem.objects.filter(id__in=plitems).values_list('id','number'))
            self.fields['number'].widget = forms.Select(choices=mr_items)
            self.fields['item'].queryset = Item.objects.filter(plitems__pl=pl)

MRSItemFromSet = inlineformset_factory(
    MaterialReceiptSheet,MRSItem,form=MRSItemForm,extra=2,
    can_delete=True,can_delete_extra=True,
    fields=['number','item','unit','quantity','condition','loc']
)

class ConditionForm(forms.ModelForm):
    class Meta:
        model = Condition
        fields = ['name',]

class MaterialIssueRequestForm(forms.ModelForm):
    class Meta:
        model = MaterialIssueRequest
        fields = ['project','number','mr','po','pl','warehouse','issue_date','required_date','client_department','location']
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.pk:
            self.fields['mr'].queryset = self.fields['mr'].queryset.filter(project=self.instance.project)
            self.fields['po'].queryset = self.fields['po'].queryset.filter(mr=self.instance.mr)
            self.fields['pl'].queryset = self.fields['pl'].queryset.filter(mr=self.instance.mr)
        self.fields['issue_date'] = JalaliDateField(label='Issue Date', 
            widget=AdminJalaliDateWidget 
        )
        self.fields['required_date'] = JalaliDateField(label='Required Date', 
            widget=AdminJalaliDateWidget 
        )

class MIRItemForm(forms.ModelForm):
    class Mata:
        model = MIRItem
        fields = ['number','item','unit','quantity','remarks','condition']
    def __init__(self, *args, **kwargs):
        pl = kwargs.pop('pl',None)
        super().__init__(*args, **kwargs)
        if pl:
            plitems = list(pl.items.all().values_list('number',flat=True))
            mr_items = [("","-------")] + list(MrItem.objects.filter(id__in=plitems).values_list('id','number'))
            self.fields['number'].widget = forms.Select(choices=mr_items)
            self.fields['item'].queryset = Item.objects.filter(plitems__pl=pl)

MIRItemFromSet = inlineformset_factory(
    MaterialIssueRequest,MIRItem,form=MIRItemForm,extra=2,
    can_delete=True,can_delete_extra=True,
    fields=['number','item','unit','quantity','remarks','condition']
)