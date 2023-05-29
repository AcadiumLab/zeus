from django.db import models


class BaseLookup(models.Model):
    name = models.CharField(max_length=100)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        abstract = True


class SchoolType(BaseLookup):
    """School type Choices"""


class SchoolLevel(BaseLookup):
    """School Level Choices"""
