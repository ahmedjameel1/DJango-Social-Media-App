# Generated by Django 4.1.2 on 2022-10-28 18:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0010_alter_profile_friends_friendrequests'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='friends',
            field=models.ManyToManyField(blank=True, to='accounts.profile'),
        ),
    ]