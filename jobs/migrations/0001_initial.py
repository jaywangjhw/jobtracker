# Generated by Django 3.2 on 2021-04-17 17:51

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Company',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('careers_url', models.URLField(max_length=300, null=True)),
                ('industry', models.CharField(choices=[('tech', 'Tech'), ('ecommerce', 'Ecommerce'), ('healthcare', 'Healthcare'), ('pharma', 'Pharmaceutical'), ('aerospace', 'Aerospace'), ('fintech', 'FinTech'), ('nonprofit', 'Nonprofit'), ('defense', 'Defense'), ('other', 'Other')], max_length=100, null=True)),
            ],
        ),
    ]
