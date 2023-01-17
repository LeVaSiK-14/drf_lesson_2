from django.db import models
from django.contrib.auth import get_user_model

from mainapp.config import RAITING, ONE

User = get_user_model()

class Category(models.Model):
    name = models.CharField(
        max_length=127, verbose_name='Название'
    )
    image = models.ImageField(
        upload_to='categories/images/', verbose_name='Картинка'
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Product(models.Model):
    category = models.ForeignKey(
        to=Category, on_delete=models.CASCADE, 
        related_name='products', verbose_name='Категория'
    )
    name = models.CharField(
        max_length=127, verbose_name='Название'
    )
    price = models.DecimalField(
        max_digits=10, decimal_places=2, verbose_name='Цена'
    )
    image = models.ImageField(
        upload_to='products/images', verbose_name='Картинка'
    )
    description = models.TextField(verbose_name='Описание')

    def __str__(self):
        return f'Продукт {self.name} от категории {self.category.name}'

    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = verbose_name + 'ы'



class Comment(models.Model):
    raiting = models.CharField(
        max_length=127, choices=RAITING, 
        default=ONE, verbose_name='Рейтинг'
    )
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, 
        related_name='comments', verbose_name='Продукт'
    )
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, 
        related_name='comments', verbose_name='Пользователь'
    )
    comment_text = models.TextField(verbose_name='Текст коммента')
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name='Дата создания'
    )

    

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name = 'Коммент'
        verbose_name_plural = verbose_name + 'ы'



# serializer
# views
# urls