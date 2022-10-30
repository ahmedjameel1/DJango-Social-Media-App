# Generated by Django 4.1.2 on 2022-10-26 15:07

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('name', models.CharField(blank=True, max_length=50, null=True)),
                ('username', models.CharField(blank=True, max_length=50, null=True)),
                ('email', models.EmailField(blank=True, max_length=254, null=True)),
                ('short_intro', models.CharField(blank=True, max_length=150, null=True)),
                ('bio', models.TextField(blank=True, max_length=300, null=True)),
                ('location', models.CharField(blank=True, max_length=50, null=True)),
                ('profile_image', models.ImageField(default='user-default.png', upload_to='profile_pics/%y/%m/%d')),
                ('social_github', models.CharField(blank=True, max_length=50, null=True)),
                ('social_twitter', models.CharField(blank=True, max_length=50, null=True)),
                ('social_youtube', models.CharField(blank=True, max_length=50, null=True)),
                ('social_website', models.CharField(blank=True, max_length=50, null=True)),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('account', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-created'],
            },
        ),
    ]