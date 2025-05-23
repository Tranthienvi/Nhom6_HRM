# Generated by Django 4.2.7 on 2025-05-13 19:45

from decimal import Decimal
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payroll', '0004_remove_payrolldetail_attendance_ratio'),
    ]

    operations = [
        migrations.AddField(
            model_name='payrolldetail',
            name='attendance_ratio',
            field=models.DecimalField(decimal_places=4, default=Decimal('1.0000'), max_digits=5, verbose_name='Tỷ lệ hưởng lương'),
        ),
    ]
