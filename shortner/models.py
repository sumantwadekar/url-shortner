from django.db import models


class URLCounter(models.Model):
    counter = models.BigIntegerField(
        verbose_name="Incremental counter for generating base62 string",
        default=0
    )

    class Meta:
        db_table = 'urlcounter'


class URLs(models.Model):
    short_code = models.CharField(
        verbose_name="Shortened url code for customer",
        max_length=8,
    )
    long_url = models.TextField(verbose_name="Long URL provided by customer")

    class Meta:
        db_table = "urls"
