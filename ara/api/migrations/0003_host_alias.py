# Generated by Django 2.1.1 on 2018-09-04 00:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_add_labels'),
    ]

    operations = [
        migrations.AddField(
            model_name='host',
            name='alias',
            field=models.CharField(max_length=255, null=True),
        ),
    ]
