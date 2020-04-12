from django.db import models
from django.db.models import CharField, DateTimeField, IntegerField
import json

# Create your models here.
class Movie(models.Model):
    id = IntegerField(primary_key=True)
    name = CharField(max_length=100)
    file_idm = CharField(max_length=100,null = True)
    douban_id = CharField(max_length=15,null = True)
    download_url = CharField(max_length=300)
    cover_img_url = CharField(null = True,max_length=300)
    
    def __str__(self):
        return self.name

    def toDict(self):
        d = {
            'id':self.id,
            'name':self.name,
            'file_imd':self.file_imd,
            'douban_id':self.douban_id,
            'download_url':self.downloas_url,
            'cover_img_url':self.cover_img_url,
            }
        return d

    def toJson(self):
        return json.dumps(self.toDict(),ensure_ascii=False)