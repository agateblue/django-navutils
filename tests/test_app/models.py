from django.db import models


class TestModel(models.Model):

    class Meta:
        permissions = (
                ('foo', 'Foo'),
                ('bar', 'Bar'),
            )
