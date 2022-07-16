from django.db import models


class OptionChoice(models.Model):
    option_group = models.ForeignKey('OptionGroup', on_delete=models.CASCADE)

    text = models.TextField(blank=True)

    class Meta:
        db_table = 'option_choice'
        verbose_name = 'option choice'
        verbose_name_plural = 'option choices'
