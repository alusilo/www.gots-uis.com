import uuid
from django.db import models

class Country(models.Model):

    #id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=45, unique=True)
    code = models.CharField(max_length=45, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        '''
        to set table name in database
        '''
        db_table = "country"