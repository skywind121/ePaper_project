# Generated by Django 3.2.9 on 2021-12-02 11:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ePaperLineBot', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user_info',
            old_name='mtext',
            new_name='lineName',
        ),
        migrations.RenameField(
            model_name='user_info',
            old_name='name',
            new_name='userTrueName',
        ),
    ]
