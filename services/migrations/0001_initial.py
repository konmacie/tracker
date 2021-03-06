# Generated by Django 2.2.7 on 2020-01-18 20:21

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='ScraperRunLog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp_start', models.DateTimeField(auto_now_add=True)),
                ('timestamp_end', models.DateTimeField(null=True)),
                ('status', models.SmallIntegerField(choices=[(1, 'Running'), (2, 'Finished')], default=1)),
            ],
        ),
        migrations.CreateModel(
            name='Service',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('url', models.URLField()),
                ('last_run', models.DateTimeField(blank=True, null=True)),
                ('active', models.BooleanField(default=True)),
                ('scraper', models.IntegerField(choices=[(1, 'Reddit'), (2, 'RSS')], default=1)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='services', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Service',
                'verbose_name_plural': 'Services',
            },
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=255, null=True)),
                ('url', models.URLField(blank=True, max_length=255, null=True)),
                ('guid', models.CharField(max_length=255)),
                ('author', models.CharField(blank=True, max_length=255, null=True)),
                ('description', models.TextField(blank=True)),
                ('timestamp', models.DateTimeField(default=django.utils.timezone.now)),
                ('run_log', models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, to='services.ScraperRunLog')),
                ('service', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='posts', to='services.Service')),
            ],
            options={
                'verbose_name': 'Post',
                'verbose_name_plural': 'Posts',
                'ordering': ('-timestamp', '-id'),
            },
        ),
    ]
