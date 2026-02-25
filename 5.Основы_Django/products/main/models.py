from django.db import models

#Не нашел клиента
class Client(models.Model):
    name = models.CharField(max_length=100)


    def __str__(self):
        return self.name

VERY_BAD = 1
BAD = 2
SATISFACTORY = 3
GOOD = 4
PERFECT = 5

MARK_CHOICES = (
    (VERY_BAD, "Очень плохо"),
    (BAD, "Плохо"),
    (SATISFACTORY, "Удовлетворительно"),
    (GOOD, "Хорошо"),
    (PERFECT, "Отлично")
)


class Product(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.title


class Review(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews')
    text = models.TextField()
    mark = models.PositiveSmallIntegerField(choices=MARK_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)