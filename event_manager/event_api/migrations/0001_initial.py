# Generated by Django 4.0.3 on 2022-03-29 16:54

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('name', models.CharField(max_length=100)),
                ('uuid', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('source', models.IntegerField(choices=[(1, 'users'), (2, 'products'), (3, 'revievs'), (4, 'comments'), (5, 'files'), (6, 'messages')])),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('description', models.TextField()),
            ],
        ),
    ]
