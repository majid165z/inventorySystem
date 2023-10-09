from django.db import models
from django.db.models import Sum
from django.conf import settings
from django.urls import reverse
# Create your models here.

class Category(models.Model):
    name = models.CharField("Category Name",max_length=50)
    created = models.DateTimeField(auto_now=False,auto_now_add=True)
    updated = models.DateTimeField(auto_now=True,auto_now_add=False)
    class Meta:
        verbose_name = "category"
        verbose_name_plural = "categories"
    def __str__(self) -> str:
        return f'{self.name}'

class Item(models.Model):
    name = models.CharField("Item Description",max_length=10)
    created = models.DateTimeField(auto_now=False,auto_now_add=True)
    updated = models.DateTimeField(auto_now=True,auto_now_add=False)
    class Meta:
        verbose_name = "کالا"
        verbose_name_plural = "کالا ها"
    def __str__(self) -> str:
        return f'{self.name}'

class Unit(models.Model):
    name = models.CharField("Unit Name",max_length=10)
    abrv = models.CharField("Abriviation",max_length=10)
    created = models.DateTimeField(auto_now=False,auto_now_add=True)
    updated = models.DateTimeField(auto_now=True,auto_now_add=False)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL,
        verbose_name='Created By',null=True,on_delete=models.SET_NULL,
        related_name='units')
    class Meta:
        verbose_name = "واحد"
        verbose_name_plural = "واحد ها"
    def __str__(self) -> str:
        return f'{self.name} ({self.abrv})'
    def save(self,*args,**kwargs):
        self.abrv = str(self.abrv).upper()
        super().save(*args, **kwargs)
    def get_edit_url(self):
        return reverse('unit_edit',kwargs={'id':self.id})

class WarehouseManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().select_related('created_by')

class Warehouse(models.Model):
    name = models.CharField("Name",max_length=40)
    address = models.TextField("Address",blank=True,null=True)
    users = models.ManyToManyField(settings.AUTH_USER_MODEL,verbose_name='Warehouse Keepers',blank=True,limit_choices_to={'warehouse_keeper':True},related_name='whs')
    created = models.DateTimeField(auto_now=False,auto_now_add=True)
    updated = models.DateTimeField(auto_now=True,auto_now_add=False)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL,
        verbose_name='Created By',null=True,on_delete=models.SET_NULL,
        related_name='warehouses')
    
    objects = WarehouseManager()
    class Meta:
        verbose_name = "انبار"
        verbose_name_plural = "انبارها"
    def __str__(self) -> str:
        return self.name
    def get_edit_url(self):
        return reverse('warehouse_edit',kwargs={'id':self.id})

class Project(models.Model):
    name = models.CharField("Project Name",max_length=40)
    number = models.CharField("Project Number",max_length=40)
    created = models.DateTimeField(auto_now=False,auto_now_add=True)
    updated = models.DateTimeField(auto_now=True,auto_now_add=False)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL,
        verbose_name='Created By',null=True,on_delete=models.SET_NULL,
        related_name='projects')
    
    objects = WarehouseManager()
    class Meta:
        verbose_name = "پروژه"
        verbose_name_plural = "پروژه ها"
    def __str__(self) -> str:
        return self.name
    def get_edit_url(self):
        return reverse('project_edit',kwargs={'id':self.id}) #TODO
class MaterialRequisitionManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().select_related('created_by','project')

class MaterialRequisition(models.Model):
    number = models.CharField('MR Number',max_length=200)
    date = models.DateField('Approved Date',blank=True)
    project = models.ForeignKey(Project,verbose_name='Project',null=True,blank=True,
        on_delete=models.SET_NULL,related_name='mr')
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL,
        verbose_name='ثبت شده توسط',null=True,on_delete=models.SET_NULL,
        related_name='mr')
    category = models.ForeignKey(Category,verbose_name='category',related_name='mr',blank=True,null=True,on_delete=models.SET_NULL)
    created = models.DateTimeField(auto_now=False,auto_now_add=True)
    updated = models.DateTimeField(auto_now=True,auto_now_add=False)
    objects = MaterialRequisitionManager()
    class Meta:
        verbose_name = "درخواست مواد"
        verbose_name_plural = "درخواست های مواد"
        ordering = ['-created']
    def __str__(self) -> str:
        return self.number
    def get_edit_url(self):
        return reverse('mr_edit',kwargs={'id':self.id}) #TODO

class MrItemManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().select_related('mr','unit','item')
class MrItem(models.Model):
    mr = models.ForeignKey(MaterialRequisition,related_name='items',on_delete=models.CASCADE)
    number = models.PositiveIntegerField('Item Number')
    tag_number = models.CharField('MESC Number',max_length=200,blank=True)
    item = models.ForeignKey(Item,related_name='mritems',on_delete=models.CASCADE,verbose_name='Item Description')
    unit = models.ForeignKey(Unit,on_delete=models.SET_NULL,null=True,related_name='items',verbose_name='Unit')
    quantity = models.DecimalField('Quantity',max_digits=10,decimal_places=3)
    created = models.DateTimeField(auto_now=False,auto_now_add=True)
    updated = models.DateTimeField(auto_now=True,auto_now_add=False)
    objects = MrItemManager()
    class Meta:
        verbose_name = "قلم درخواست  مواد"
        verbose_name_plural = "اقلام درخواست های مواد"
    def __str__(self) -> str:
        return self.item.name

class ProcurementOrderManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().select_related('mr','created_by','project')

class ProcurementOrder(models.Model):
    project = models.ForeignKey(Project,verbose_name='Project',null=True,blank=True,
        on_delete=models.SET_NULL,related_name='pos')
    number = models.CharField('PO Number',max_length=200)
    mr = models.ForeignKey(MaterialRequisition,related_name='pos',on_delete=models.CASCADE,verbose_name='MR Number')
    date = models.DateField('Date Confirmed',blank=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL,
        verbose_name='ثبت شده توسط',null=True,on_delete=models.SET_NULL,
        related_name='pos')
    company = models.CharField('Seller (Company Name)',max_length=100)
    created = models.DateTimeField(auto_now=False,auto_now_add=True)
    updated = models.DateTimeField(auto_now=True,auto_now_add=False)

    objects = ProcurementOrderManager()
    class Meta:
        verbose_name = "سفارش خرید"
        verbose_name_plural = "سفارش های خرید"
        ordering = ['-created']
    def __str__(self) -> str:
        return self.number
    def get_edit_url(self):
        return reverse('po_edit',kwargs={'id':self.id}) #TODO

class POItemManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().select_related('po','unit','item')
class POItem(models.Model):
    po = models.ForeignKey(ProcurementOrder,related_name='items',on_delete=models.CASCADE)
    number = models.PositiveIntegerField('Mr Item No.')
    item = models.ForeignKey(Item,related_name='poitems',on_delete=models.CASCADE,verbose_name='Item Description')
    unit = models.ForeignKey(Unit,on_delete=models.SET_NULL,null=True,related_name='poitems',verbose_name='Unit')
    quantity = models.DecimalField('Quantity',max_digits=10,decimal_places=3)
    created = models.DateTimeField(auto_now=False,auto_now_add=True)
    updated = models.DateTimeField(auto_now=True,auto_now_add=False)
    objects = POItemManager()
    class Meta:
        verbose_name = "قلم سفارش خرید"
        verbose_name_plural = "اقلام سفارش خرید"
    def __str__(self) -> str:
        return self.item.name

class PackingListManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().select_related('project','mr','po','created_by')
class PackingList(models.Model):
    project = models.ForeignKey(Project,verbose_name='Project',null=True,blank=True,
        on_delete=models.SET_NULL,related_name='pls')
    number = models.CharField('Packing List Number',max_length=200)
    mr = models.ForeignKey(MaterialRequisition,related_name='pls',on_delete=models.CASCADE,verbose_name='MR Number')
    po = models.ForeignKey(ProcurementOrder,related_name='pls',on_delete=models.CASCADE,verbose_name='PO Number')
    company = models.CharField('شرکت فروشنده کالا',max_length=100)
    date = models.DateField('Sent Date',blank=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL,
        verbose_name='ثبت شده توسط',null=True,on_delete=models.SET_NULL,
        related_name='pls')
    created = models.DateTimeField(auto_now=False,auto_now_add=True)
    updated = models.DateTimeField(auto_now=True,auto_now_add=False)
    objects = PackingListManager()
    class Meta:
        verbose_name = "بارنامه"
        verbose_name_plural = "بارنامه ها"
        ordering = ['-created']
    def __str__(self) -> str:
        return self.number
    def get_edit_url(self):
        return reverse('pl_edit',kwargs={'id':self.id}) #TODO
    
    def save(self,*args,**kwargs):
        self.company = self.po.company
        super().save(*args,**kwargs)
class PLItemManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().select_related('pl','unit')
class PLItem(models.Model):
    pl = models.ForeignKey(PackingList,related_name='items',on_delete=models.CASCADE)
    number = models.PositiveIntegerField('Mr Item No.')
    item = models.ForeignKey(Item,related_name='plitems',on_delete=models.CASCADE,verbose_name='Item Description')
    unit = models.ForeignKey(Unit,on_delete=models.SET_NULL,null=True,related_name='plitems',verbose_name='Unit')
    quantity = models.DecimalField('Quantity',max_digits=10,decimal_places=3)
    created = models.DateTimeField(auto_now=False,auto_now_add=True)
    updated = models.DateTimeField(auto_now=True,auto_now_add=False)
    objects = PLItemManager()
    class Meta:
        verbose_name = "قلم  بارنامه"
        verbose_name_plural = "اقلام بارنامه"
    def __str__(self) -> str:
        return self.item.name
class Condition(models.Model):
    name = models.CharField('Condition',max_length=20)
    created = models.DateTimeField(auto_now=False,auto_now_add=True)
    updated = models.DateTimeField(auto_now=True,auto_now_add=False)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL,
        verbose_name='ثبت شده توسط',null=True,on_delete=models.SET_NULL,
        related_name='conditions')
    class Meta:
        verbose_name = "Condition"
        verbose_name_plural = "Conditions"
        ordering = ['-created']
    def __str__(self) -> str:
        return self.name

class MRStManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().select_related('project','mr','po','pl','created_by')
    
class MaterialReceiptSheet(models.Model):
    project = models.ForeignKey(Project,verbose_name='Project',null=True,blank=True,
        on_delete=models.SET_NULL,related_name='mrs')
    number = models.CharField('MRS Number',max_length=200)
    mr = models.ForeignKey(MaterialRequisition,related_name='mrs',on_delete=models.CASCADE,verbose_name='MR Number')
    po = models.ForeignKey(ProcurementOrder,related_name='mrs',on_delete=models.CASCADE,verbose_name='PO Number')
    pl = models.ForeignKey(PackingList,related_name='mrs',on_delete=models.CASCADE,verbose_name='Packing List Number')
    warehouse = models.ForeignKey(Warehouse,related_name='mrs',on_delete=models.CASCADE,verbose_name='Warehouse')
    vendor = models.CharField('Vendor',max_length=100)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL,
        verbose_name='ثبت شده توسط',null=True,on_delete=models.SET_NULL,
        related_name='mrs')
    created = models.DateTimeField(auto_now=False,auto_now_add=True)
    updated = models.DateTimeField(auto_now=True,auto_now_add=False)
    objects = PackingListManager()
    class Meta:
        verbose_name = "Material Receipt Sheet"
        verbose_name_plural = "Material Receipt Sheets"
        ordering = ['-created']
    def __str__(self) -> str:
        return self.number
    def get_edit_url(self):
        return reverse('mrs_edit',kwargs={'id':self.id}) #TODO

class MRSItemManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().select_related('mrs','unit','condition')
class MRSItem(models.Model):
    mrs = models.ForeignKey(MaterialReceiptSheet,related_name='items',on_delete=models.CASCADE)
    number = models.PositiveIntegerField('Mr Item No.')
    item = models.ForeignKey(Item,related_name='mrsitems',on_delete=models.CASCADE,verbose_name='Item Description')
    unit = models.ForeignKey(Unit,on_delete=models.SET_NULL,null=True,related_name='mrsitems',verbose_name='Unit')
    quantity = models.DecimalField('Quantity',max_digits=10,decimal_places=3)
    condition = models.ForeignKey(Condition,related_name='mrsitems',verbose_name='Condition',on_delete=models.CASCADE,default=1)
    loc = models.CharField('loc',max_length=10,null=True,blank=True)

    created = models.DateTimeField(auto_now=False,auto_now_add=True)
    updated = models.DateTimeField(auto_now=True,auto_now_add=False)
    objects = MRSItemManager()
    class Meta:
        verbose_name = "MRS Item"
        verbose_name_plural = "MRS Items"
    def __str__(self) -> str:
        return self.item.name
    def save(self,*args,**kwargs):
        super().save(*args,**kwargs)
        iv,created = inventoryItem.objects.get_or_create(
            project = self.mrs.project,
            warehouse = self.mrs.warehouse,
            item = self.item,
            condition=self.condition
            )
        if created:
            iv.incoming = self.quantity
        else:
            iv.incoming = MRSItem.objects.filter(mrs__project=self.mrs.project,
                                                 mrs__warehouse = self.mrs.warehouse,
                                                 item = self.item,
                                                 condition=self.condition
                                                 ).aggregate(total=Sum('quantity'))['total']
        iv.save()
class InventoryItemManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().select_related('project','warehouse','item')

class inventoryItem(models.Model):
    project = models.ForeignKey(Project,verbose_name='Project',null=True,blank=True,
        on_delete=models.SET_NULL,related_name='ivitems')
    warehouse = models.ForeignKey(Warehouse,related_name='ivitems',on_delete=models.CASCADE,verbose_name='Warehouse')
    item = models.ForeignKey(Item,related_name='ivitems',on_delete=models.CASCADE,verbose_name='Item Description')
    condition = models.ForeignKey(Condition,related_name='ivitems',verbose_name='Condition',on_delete=models.CASCADE,default=1)
    incoming = models.DecimalField('incoming',max_digits=10,decimal_places=3,default=0)
    outgoing = models.DecimalField('outgoing',max_digits=10,decimal_places=3,default=0)
    remaining = models.DecimalField('remaining',max_digits=10,decimal_places=3,default=0)
    objects = InventoryItemManager()
    total_in_all_warehouse_project = models.DecimalField('total_in_all_warehouse_project',max_digits=10,decimal_places=3,default=0)
    total_in_all = models.DecimalField('total_in_all',max_digits=10,decimal_places=3,default=0)
    class Meta:
        verbose_name = "inventory Item"
        verbose_name_plural = "inventory Item"
    def save(self,*args,**kwargs):
        self.remaining = self.incoming - self.outgoing
        super().save(*args,**kwargs)
        
        inventoryItem.objects.filter(item=self.item,project=self.project,condition=self.condition).update(
             total_in_all_warehouse_project=inventoryItem.objects.filter(item=self.item,project=self.project,condition=self.condition).aggregate(total=Sum('remaining'))['total'])
        inventoryItem.objects.filter(item=self.item,condition=self.condition).update(
             total_in_all=inventoryItem.objects.filter(item=self.item,condition=self.condition).aggregate(total=Sum('remaining'))['total'])
                
        
    def __str__(self) -> str:
        return self.item.name
class MaterialIssueRequest(models.Model):
    project = models.ForeignKey(Project,verbose_name='Project',null=True,blank=True,
        on_delete=models.SET_NULL,related_name='mir')
    number = models.CharField('MIR Number',max_length=200)
    mr = models.ForeignKey(MaterialRequisition,related_name='mir',on_delete=models.CASCADE,verbose_name='MR Number')
    po = models.ForeignKey(ProcurementOrder,related_name='mir',on_delete=models.CASCADE,verbose_name='PO Number')
    pl = models.ForeignKey(PackingList,related_name='mir',on_delete=models.CASCADE,verbose_name='Packing List Number')
    warehouse = models.ForeignKey(Warehouse,related_name='mir',on_delete=models.CASCADE,verbose_name='Origin(From)')
    issue_date = models.DateField('Issue Date',blank=True)
    required_date = models.DateField('Required Date',blank=True)
    client_department = models.CharField("Client Department",max_length=100)
    sent_to_warehouse = models.BooleanField("sent to warehouse",default=False)
    sent_to_location = models.BooleanField("sent to location",default=False)
    location = models.CharField("Destination",max_length=100,blank=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL,
        verbose_name='ثبت شده توسط',null=True,on_delete=models.SET_NULL,
        related_name='mir')
    created = models.DateTimeField(auto_now=False,auto_now_add=True)
    updated = models.DateTimeField(auto_now=True,auto_now_add=False)
    objects = PackingListManager()
    class Meta:
        verbose_name = "Material Issue Request"
        verbose_name_plural = "Material Issue Requests"
        ordering = ['-created']
    def __str__(self) -> str:
        return self.number
    def get_edit_url(self):
        return reverse('mir_edit',kwargs={'id':self.id}) 
    def save(self,*args,**kwargs):
        super().save(*args,**kwargs)
        if self.sent_to_location:
            items = self.items.all()
            for item in items:
                iv,created = inventoryItem.objects.get_or_create(
                    project = self.project,
                    warehouse = self.warehouse,
                    item = item.item,
                    condition=item.condition  
                )
                iv.outgoing = MIRItem.objects.filter(mir__project=self.project,
                                                 mir__warehouse = self.warehouse,
                                                 item = item.item,
                                                 condition=item.condition
                                                 ).aggregate(total=Sum('quantity'))['total']
                iv.save()
                
                
                

class MIRItemManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().select_related('mir','unit','item')
class MIRItem(models.Model):
    mir = models.ForeignKey(MaterialIssueRequest,related_name='items',on_delete=models.CASCADE)
    number = models.PositiveIntegerField('Mr Item No.')
    item = models.ForeignKey(Item,related_name='miritems',on_delete=models.CASCADE,verbose_name='Item Description')
    unit = models.ForeignKey(Unit,on_delete=models.SET_NULL,null=True,related_name='miritems',verbose_name='Unit')
    quantity = models.DecimalField('Quantity',max_digits=10,decimal_places=3)
    remarks = models.CharField('remakrs',max_length=200,null=True,blank=True)
    condition = models.ForeignKey(Condition,related_name='miritems',verbose_name='Condition',on_delete=models.CASCADE,default=1)

    created = models.DateTimeField(auto_now=False,auto_now_add=True)
    updated = models.DateTimeField(auto_now=True,auto_now_add=False)
    objects = MIRItemManager()
    class Meta:
        verbose_name = "MIR Item"
        verbose_name_plural = "MIR Items"
    def __str__(self) -> str:
        return self.item.name
    def save(self,*args,**kwargs):
        super().save(*args,**kwargs)
