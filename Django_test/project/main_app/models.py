from django.db import models
from django.utils.translation import gettext_lazy as _

# Create your models here.
class Category(models.Model):
    parent = models.ForeignKey('self', on_delete= models.CASCADE, blank=True, null=True)
    title = models.CharField(_("title"), blank=False, null=False, max_length=100, unique=True)
    order = models.BigIntegerField(default=0, null=True, blank=True)

    def __str__(self):
        return f"{self.title}"

 

class Product(models.Model):
    name = models.CharField(_("name"), max_length=150, unique=True)
    price = models.FloatField(_("price"))
    category = models.ManyToManyField("Category", verbose_name=_("category"))

    def __str__(self):
        return f"{self.name}"