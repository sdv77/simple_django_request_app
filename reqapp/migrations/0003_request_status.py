# Generated by Django 5.1.5 on 2025-02-04 18:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reqapp', '0002_device_request_device'),
    ]

    operations = [
        migrations.AddField(
            model_name='request',
            name='status',
            field=models.CharField(choices=[('open', 'Открыта'), ('in_progress', 'В процессе'), ('closed', 'Закрыта')], default='open', max_length=20),
        ),
    ]
