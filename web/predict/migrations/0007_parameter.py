# Generated by Django 4.0.3 on 2022-05-23 15:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('predict', '0006_delete_parameterr'),
    ]

    operations = [
        migrations.CreateModel(
            name='Parameter',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('parameter_list', models.CharField(default='', max_length=255)),
                ('parameter_descriptions', models.TextField(default='')),
                ('parameter_using', models.IntegerField(default=0)),
                ('time', models.DateTimeField(auto_now=True)),
            ],
        ),
    ]