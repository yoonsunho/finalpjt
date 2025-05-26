from django.db import models

# Create your models here.
class GoldPrice(models.Model):
    date = models.DateField()
    close_last = models.DecimalField(max_digits=10, decimal_places=3)
    volume = models.DecimalField(max_digits=15, decimal_places=3)
    open_price = models.DecimalField(max_digits=10, decimal_places=3)
    high = models.DecimalField(max_digits=10, decimal_places=3)
    low = models.DecimalField(max_digits=10, decimal_places=3)

    class Meta:
        ordering = ('date',)

class SilverPrice(models.Model):
    date = models.DateField()
    close_last = models.DecimalField(max_digits=10, decimal_places=3)
    volume = models.DecimalField(max_digits=15, decimal_places=3)
    open_price = models.DecimalField(max_digits=10, decimal_places=3)
    high = models.DecimalField(max_digits=10, decimal_places=3)
    low = models.DecimalField(max_digits=10, decimal_places=3)

    class Meta:
        ordering = ['date']
