from django.db import models
from django.conf import settings
from django.db.models.fields import CharField
from django.urls import reverse
# Create your models here.
class Item(models.Model):
    name = models.CharField("شرج کالا",max_length=10)
    created = models.DateTimeField(auto_now=False,auto_now_add=True)
    updated = models.DateTimeField(auto_now=True,auto_now_add=False)
    class Meta:
        verbose_name = "کالا"
        verbose_name_plural = "کالا ها"
    def __str__(self) -> str:
        return f'{self.name}'

class Unit(models.Model):
    name = models.CharField("نام واحد",max_length=10)
    abrv = models.CharField("واحد اختصاری",max_length=10)
    created = models.DateTimeField(auto_now=False,auto_now_add=True)
    updated = models.DateTimeField(auto_now=True,auto_now_add=False)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL,
        verbose_name='ثبت شده توسط',null=True,on_delete=models.SET_NULL,
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
    name = models.CharField("نام انبار",max_length=40)
    address = models.TextField("آدرس",blank=True,null=True)
    users = models.ManyToManyField(settings.AUTH_USER_MODEL,verbose_name='انباردارها',blank=True,limit_choices_to={'warehouse_keeper':True})
    created = models.DateTimeField(auto_now=False,auto_now_add=True)
    updated = models.DateTimeField(auto_now=True,auto_now_add=False)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL,
        verbose_name='ثبت شده توسط',null=True,on_delete=models.SET_NULL,
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
    name = models.CharField("نام پروژه",max_length=40)
    number = models.CharField("شماره پروژه",max_length=40)
    created = models.DateTimeField(auto_now=False,auto_now_add=True)
    updated = models.DateTimeField(auto_now=True,auto_now_add=False)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL,
        verbose_name='ثبت شده توسط',null=True,on_delete=models.SET_NULL,
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
    number = models.CharField('شماره MR',max_length=200)
    date = models.DateField('تاریخ تایید',blank=True)
    project = models.ForeignKey(Project,verbose_name='پروژه',null=True,blank=True,
        on_delete=models.SET_NULL,related_name='mr')
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL,
        verbose_name='ثبت شده توسط',null=True,on_delete=models.SET_NULL,
        related_name='mr')

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
    number = models.PositiveIntegerField('شماره')
    tag_number = models.CharField('Tag/Part number',max_length=200)
    item = models.ForeignKey(Item,related_name='mritems',on_delete=models.CASCADE,verbose_name='شرح کالا')
    unit = models.ForeignKey(Unit,on_delete=models.SET_NULL,null=True,related_name='items',verbose_name='واحد')
    quantity = models.DecimalField('مقدار',max_digits=10,decimal_places=3)
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
    project = models.ForeignKey(Project,verbose_name='پروژه',null=True,blank=True,
        on_delete=models.SET_NULL,related_name='pos')
    number = models.CharField('شماره PO',max_length=200)
    mr = models.ForeignKey(MaterialRequisition,related_name='pos',on_delete=models.CASCADE,verbose_name='شماره درخواست کالا')
    date = models.DateField('تاریخ درخواست',blank=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL,
        verbose_name='ثبت شده توسط',null=True,on_delete=models.SET_NULL,
        related_name='pos')
    company = models.CharField('شرکت فروشنده کالا',max_length=100)
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
    item = models.ForeignKey(Item,related_name='poitems',on_delete=models.CASCADE,verbose_name='شرح کالا')
    unit = models.ForeignKey(Unit,on_delete=models.SET_NULL,null=True,related_name='poitems',verbose_name='واحد')
    quantity = models.DecimalField('مقدار',max_digits=10,decimal_places=3)
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
    project = models.ForeignKey(Project,verbose_name='پروژه',null=True,blank=True,
        on_delete=models.SET_NULL,related_name='pls')
    number = models.CharField('شماره بارنامه',max_length=200)
    mr = models.ForeignKey(MaterialRequisition,related_name='pls',on_delete=models.CASCADE,verbose_name='شماره درخواست کالا')
    po = models.ForeignKey(ProcurementOrder,related_name='pls',on_delete=models.CASCADE,verbose_name='شماره سفارش خرید کالا')
    company = models.CharField('شرکت فروشنده کالا',max_length=100)
    date = models.DateField('تاریخ درخواست',blank=True)
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
    item = models.ForeignKey(Item,related_name='plitems',on_delete=models.CASCADE,verbose_name='شرح کالا')
    unit = models.ForeignKey(Unit,on_delete=models.SET_NULL,null=True,related_name='plitems',verbose_name='واحد')
    quantity = models.DecimalField('مقدار',max_digits=10,decimal_places=3)
    created = models.DateTimeField(auto_now=False,auto_now_add=True)
    updated = models.DateTimeField(auto_now=True,auto_now_add=False)
    objects = PLItemManager()
    class Meta:
        verbose_name = "قلم  بارنامه"
        verbose_name_plural = "اقلام بارنامه"
    def __str__(self) -> str:
        return self.item.name
