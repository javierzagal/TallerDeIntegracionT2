# Generated by Django 3.2.7 on 2021-09-25 03:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0012_auto_20210924_2351'),
    ]

    operations = [
        migrations.RenameField(
            model_name='league',
            old_name='self',
            new_name='self_name',
        ),
        migrations.AlterField(
            model_name='league',
            name='id',
            field=models.CharField(max_length=100, primary_key=True, serialize=False),
        ),
    ]
