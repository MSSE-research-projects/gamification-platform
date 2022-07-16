from django.db import models


class OptionGroup(models.Model):
    """
    Model for OptionGroup
    """
    name = models.CharField(max_length=150)

    class Meta:
        db_table = 'option_group'
        verbose_name = 'option group'
        verbose_name_plural = 'option groups'

    def __str__(self):
        return self.name
