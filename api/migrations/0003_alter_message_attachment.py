# Generated by Django 4.2.3 on 2023-07-12 23:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_chat_is_open'),
    ]

    operations = [
        migrations.AlterField(
            model_name='message',
            name='attachment',
            field=models.FileField(blank=True, upload_to='files/'),
        ),
    ]
