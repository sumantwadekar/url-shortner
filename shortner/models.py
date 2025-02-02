from django.db import models


class URLs(models.Model):
    short_url = models.CharField(
        verbose_name="Shortened URL for customer",
        max_length=6,
    )
    long_url = models.TextField(verbose_name="Long URL provided by customer")

    class Meta:
        db_table = 'urls'
