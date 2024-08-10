from tortoise import fields 
from tortoise.models import Model


class User(Model):
    id = fields.BigIntField(pk=True)
    username = fields.CharField(max_lenght="32", null=True)
    
    
    