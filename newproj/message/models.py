from django.db import models

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
class MessageModel(models.Model) :

    class Meta :
        ordering = ["is_done", "-important", "datetime_notification"]

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
    
    def __str__(self) -> str:
        return f'{self.types} - {self.text} - {"Сделано" if self.is_done else "Не сделано"}'
