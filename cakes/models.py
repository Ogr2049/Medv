from django.db import models

class Product(models.Model):
    name = models.CharField(max_length=255, verbose_name='Название',)
    price = models.IntegerField(verbose_name='Цена',)
    image = models.CharField(max_length=1024, verbose_name='Фотография',)
    amount = models.CharField(max_length=32, verbose_name='Вес/Количество',)
    category = models.CharField(max_length=255, verbose_name='Категория',)

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'

    def __str__(self):
        return '%s %s' % (self.category, self.name)