from django.db import models
from datetime import timedelta
from django.utils import timezone
# Create your models here.
MESSAGE_TYPES = (
    (1, "Работа"),
    (2, "Спорт"),
    (3, "Учеба"),
    
)
MESSAGE_STATUS = (
    (True, "Сделано"),
    (False, "He cделано"),
)
MESSAGE_IMPORTANCE = (
    (0, "Не важно"),
    (1, "Важно"),
    (2, "Заканчивается")
)
class MessageModel(models.Model) :

    class Meta :
        ordering = ["is_done", "-expiring", "-important", "datetime_notification"]

    datetime_notification = models.DateTimeField(
        verbose_name="Время исполнения задачи"
    )

    text = models.CharField(
        max_length=255,
        verbose_name="Текст Задачи"
    )

    types = models.IntegerField(
        choices=MESSAGE_TYPES,
        default=1,
        verbose_name="Тип Задачи"
    )

    is_done = models.BooleanField(
        default=False,
        choices=MESSAGE_STATUS,
        verbose_name="Статус Записи"
    )

    important = models.BooleanField(
        default=False
    )

    expiring = models.BooleanField(
        default=False
    )
    def expiring_test(self) :
        if self.datetime_notification - timezone.now() < timedelta(hours=0):
            self.is_done = True
            self.expiring = False
            self.important = False
            return False 
        elif self.datetime_notification - timezone.now()  < timedelta(hours=10) :
            self.expiring = True
            self.important = True
            self.save()
            return self.datetime_notification - timezone.now()  < timedelta(hours=10) 
    
    def time_count(self) :
        return str(self.datetime_notification - timezone.now())[:-7]
    def __str__(self) -> str:
        return f'{self.types} - {self.text} - {"Сделано" if self.is_done else "Не сделано"}'
