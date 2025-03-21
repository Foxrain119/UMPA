# Generated by Django 4.2.20 on 2025-03-16 04:54

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Exchange',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cur_unit', models.CharField(max_length=10)),
                ('cur_nm', models.CharField(max_length=30)),
                ('ttb', models.FloatField()),
                ('tts', models.FloatField()),
                ('deal_bas_r', models.FloatField()),
                ('bkpr', models.FloatField()),
                ('kftc_deal_bas_r', models.FloatField()),
                ('kftc_bkpr', models.FloatField()),
            ],
        ),
    ]
