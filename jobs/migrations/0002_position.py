# Generated by Django 3.2 on 2021-04-17 19:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jobs', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Position',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('position_title', models.CharField(max_length=100)),
                ('position_url', models.URLField(max_length=300, null=True)),
                ('date_opened', models.DateField(null=True)),
                ('date_closed', models.DateField(blank=True, default='', null=True)),
                ('skills', models.CharField(choices=[{'Java', 'java'}, {'C++', 'c++'}, {'Algorithm Design', 'algorithm'}, {'Object Oriented', 'object'}, {'kubernetes', 'Kubernetes'}], max_length=100, null=True)),
                ('job_description', models.TextField(null=True)),
            ],
        ),
    ]
