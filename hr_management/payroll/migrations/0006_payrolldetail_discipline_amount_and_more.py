# Generated by Django 4.2.7 on 2025-05-13 20:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payroll', '0005_payrolldetail_attendance_ratio'),
    ]

    operations = [
        migrations.AddField(
            model_name='payrolldetail',
            name='discipline_amount',
            field=models.DecimalField(decimal_places=0, default=0, max_digits=12, verbose_name='Tiền phạt'),
        ),
        migrations.AddField(
            model_name='payrolldetail',
            name='income_tax',
            field=models.DecimalField(decimal_places=0, default=0, max_digits=12, verbose_name='Thuế TNCN'),
        ),
        migrations.AddField(
            model_name='payrolldetail',
            name='reward_amount',
            field=models.DecimalField(decimal_places=0, default=0, max_digits=12, verbose_name='Tiền thưởng'),
        ),
    ]
