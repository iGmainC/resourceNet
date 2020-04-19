# Generated by Django 3.0.5 on 2020-04-19 06:19

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Author',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='不详', max_length=30, verbose_name='作者姓名')),
                ('information', models.TextField(default='暂无', verbose_name='作者介绍')),
            ],
            options={
                'verbose_name': '作者',
                'verbose_name_plural': '作者',
            },
        ),
        migrations.CreateModel(
            name='Book',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file_name', models.CharField(blank=True, max_length=100, null=True, verbose_name='文件名')),
                ('title', models.CharField(blank=True, max_length=100, null=True, verbose_name='书名')),
                ('subtitle', models.CharField(blank=True, default='', max_length=100, null=True, verbose_name='副标题')),
                ('english_title', models.CharField(blank=True, default='', max_length=200, null=True, verbose_name='英文书名')),
                ('price', models.CharField(blank=True, default='未知', max_length=10, null=True, verbose_name='售价')),
                ('cover', models.CharField(blank=True, default='http://18.222.57.174/static/images/None_cover.png/', max_length=200, verbose_name='封面链接')),
                ('large_cover', models.CharField(default='http://18.222.57.174/static/images/None_cover.png/', max_length=200, verbose_name='封面大图')),
                ('summary', models.TextField(blank=True, default='暂无', null=True, verbose_name='简介')),
                ('catalog', models.TextField(blank=True, default='暂无', null=True, verbose_name='目录')),
                ('douban_id', models.CharField(blank=True, default='', max_length=30, null=True, verbose_name='豆瓣ID')),
                ('true_douban_id', models.CharField(blank=True, default='', max_length=30, null=True, verbose_name='用于勘误的豆瓣ID')),
                ('isbn10', models.CharField(blank=True, default='', max_length=20, null=True)),
                ('isbn13', models.CharField(blank=True, default='', max_length=26, null=True)),
                ('pages', models.IntegerField(blank=True, null=True, verbose_name='页数')),
                ('epub_flag', models.BooleanField(default=False)),
                ('azw3_flag', models.BooleanField(default=False)),
                ('mobi_flag', models.BooleanField(default=False)),
                ('pdf_flag', models.BooleanField(default=False)),
                ('kfx_flag', models.BooleanField(default=False)),
                ('epub_download', models.TextField(blank=True, default='', null=True, verbose_name='EPUB下载链接')),
                ('azw3_download', models.TextField(blank=True, default='', null=True, verbose_name='AZW3下载链接')),
                ('mobi_download', models.TextField(blank=True, default='', null=True, verbose_name='MOBI下载链接')),
                ('pdf_download', models.TextField(blank=True, default='', null=True, verbose_name='PDF下载链接')),
                ('kfx_download', models.TextField(blank=True, default='', null=True, verbose_name='KFX下载链接')),
                ('date', models.DateTimeField(null=True)),
                ('author', models.ManyToManyField(blank=True, related_name='book_author', to='book.Author', verbose_name='作者')),
            ],
            options={
                'verbose_name': '书籍',
                'verbose_name_plural': '书籍',
            },
        ),
        migrations.CreateModel(
            name='Translator',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30, verbose_name='译者姓名')),
                ('book', models.ManyToManyField(blank=True, related_name='translator_book', to='book.Book', verbose_name='译者的书')),
            ],
            options={
                'verbose_name': '译者',
                'verbose_name_plural': '译者',
            },
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30, verbose_name='标签名')),
                ('title', models.CharField(max_length=30, verbose_name='标签标题')),
                ('book', models.ManyToManyField(blank=True, related_name='tag_book', to='book.Book', verbose_name='类型的书')),
            ],
            options={
                'verbose_name': '标签',
                'verbose_name_plural': '标签',
            },
        ),
        migrations.CreateModel(
            name='Series',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='系列名')),
                ('book', models.ManyToManyField(blank=True, related_name='series_book', to='book.Book', verbose_name='系列的书')),
            ],
            options={
                'verbose_name': '系列',
                'verbose_name_plural': '系列',
            },
        ),
        migrations.CreateModel(
            name='Publisher',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30, verbose_name='出版社名')),
                ('book', models.ManyToManyField(blank=True, related_name='publisher_book', to='book.Book', verbose_name='出版社的书')),
            ],
            options={
                'verbose_name': '出版社',
                'verbose_name_plural': '出版社',
            },
        ),
        migrations.AddField(
            model_name='book',
            name='publisher',
            field=models.ManyToManyField(blank=True, related_name='book_publisher', to='book.Publisher', verbose_name='出版社'),
        ),
        migrations.AddField(
            model_name='book',
            name='series',
            field=models.ManyToManyField(blank=True, related_name='book_series', to='book.Series', verbose_name='系列'),
        ),
        migrations.AddField(
            model_name='book',
            name='tags',
            field=models.ManyToManyField(blank=True, related_name='book_tags', to='book.Tag', verbose_name='标签'),
        ),
        migrations.AddField(
            model_name='book',
            name='translator',
            field=models.ManyToManyField(blank=True, related_name='book_translator', to='book.Translator', verbose_name='译者'),
        ),
        migrations.AddField(
            model_name='author',
            name='book',
            field=models.ManyToManyField(blank=True, related_name='author_book', to='book.Book', verbose_name='作者的书'),
        ),
    ]
