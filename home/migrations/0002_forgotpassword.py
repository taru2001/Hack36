# Generated by Django 3.1.1 on 2021-04-10 10:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='forgotPassword',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=100)),
                ('token', models.CharField(max_length=500)),
                ('datastamp', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
