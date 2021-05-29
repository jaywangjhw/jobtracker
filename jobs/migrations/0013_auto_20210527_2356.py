# Generated by Django 3.2.3 on 2021-05-27 23:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jobs', '0012_auto_20210527_0306'),
    ]

    operations = [
        migrations.AlterField(
            model_name='company',
            name='careers_url',
            field=models.URLField(blank=True, max_length=1000, null=True),
        ),
        migrations.AlterField(
            model_name='company',
            name='industry',
            field=models.CharField(blank=True, choices=[('tech', 'Tech'), ('ecommerce', 'Ecommerce'), ('gaming', 'Gaming'), ('healthcare', 'Healthcare'), ('pharma', 'Pharmaceutical'), ('aerospace', 'Aerospace'), ('fintech', 'FinTech'), ('nonprofit', 'Nonprofit'), ('defense', 'Defense'), ('other', 'Other')], max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='position',
            name='position_url',
            field=models.URLField(max_length=1000, null=True),
        ),
    ]
