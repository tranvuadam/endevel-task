# Generated by Django 3.2.7 on 2022-07-01 11:36

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('tag', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='BlogPost',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=150, verbose_name='Title')),
                ('detail', models.TextField(max_length=300, verbose_name='Detail')),
                ('text', models.TextField(max_length=3000, verbose_name='Text')),
                ('tags', models.ManyToManyField(related_name='blog_posts', to='tag.Tag')),
            ],
        ),
    ]