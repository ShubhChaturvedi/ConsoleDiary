# Generated by Django 4.0.5 on 2022-06-29 12:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0005_post_slug'),
    ]

    operations = [
        migrations.CreateModel(
            name='tanishqblog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.CharField(max_length=2000)),
                ('title', models.CharField(max_length=15)),
                ('username', models.CharField(max_length=10)),
            ],
        ),
    ]
