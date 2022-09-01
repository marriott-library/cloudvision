# Generated by Django 3.2.2 on 2021-09-13 21:18

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import ocr.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Log',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('service_name', models.CharField(max_length=200)),
                ('input_file', models.FilePathField(path=ocr.models.images_path)),
                ('output_file', models.FilePathField(path=ocr.models.output_path)),
                ('ocr_result', models.TextField()),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('run_start_time', models.DateTimeField()),
                ('run_end_time', models.DateTimeField()),
                ('run_time', models.IntegerField()),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
