# Generated by Django 2.2.5 on 2019-09-25 14:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0002_auto_20190925_1805'),
    ]

    operations = [
        migrations.AlterField(
            model_name='issue',
            name='status',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='issues', to='webapp.Status', verbose_name='Статус'),
        ),
        migrations.AlterField(
            model_name='issue',
            name='type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='issues', to='webapp.Type', verbose_name='Тип'),
        ),
    ]