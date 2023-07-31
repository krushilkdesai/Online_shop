# Generated by Django 4.2.1 on 2023-06-25 14:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0005_alter_product_table'),
    ]

    operations = [
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('msg_id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=50)),
                ('phone', models.CharField(default='None', max_length=10)),
                ('email', models.CharField(default='None', max_length=50)),
                ('desc', models.CharField(default='None', max_length=300)),
            ],
        ),
        migrations.AlterField(
            model_name='product',
            name='desc',
            field=models.CharField(max_length=800),
        ),
    ]
