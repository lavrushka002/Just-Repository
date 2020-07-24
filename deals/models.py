from django.db import models
from django.core.validators import FileExtensionValidator

class Data(models.Model):
	file = models.FileField(blank=False, null=False, validators=[FileExtensionValidator(['csv'])])
	def __str__(self):
		return self.file.name

class Deal(models.Model):
	customer = models.CharField(verbose_name = 'customer', max_length = 50)
	item = models.CharField(verbose_name = 'item', max_length = 300)
	total = models.IntegerField(verbose_name = 'total')
	quantity = models.IntegerField(verbose_name = 'quantity')
	date = models.DateTimeField(verbose_name = 'date')

class ResultResponse(models.Model):
	username = models.CharField(verbose_name = 'username', max_length = 50)
	spent_money = models.IntegerField(verbose_name = 'spent_money')
	gems = models.CharField(verbose_name = 'gems', max_length = 300)