from django.contrib import admin
from .models import Book,Author,Tag, Series,Translator,Publisher
# Register your models here.
admin.site.register(Book)
admin.site.register(Author)
admin.site.register(Tag)
admin.site.register(Series)
admin.site.register(Translator)
admin.site.register(Publisher)