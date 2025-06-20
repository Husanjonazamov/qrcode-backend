# Generated by Django 5.1.3 on 2025-06-17 13:51

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='GenerateModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('owner', models.CharField(max_length=255, verbose_name='Mulk egasi')),
                ('client', models.CharField(max_length=255, verbose_name='Buyurtmachi')),
                ('purpose', models.CharField(max_length=255, verbose_name='Baholash maqsadi')),
                ('valuation_amount', models.CharField(blank=True, max_length=200, null=True, verbose_name='Baholangan narx')),
                ('input_pdf', models.FileField(upload_to='uploads/original_pdfs/', verbose_name='Asl PDF fayl')),
                ('result_pdf', models.FileField(blank=True, null=True, upload_to='uploads/processed_pdfs/', verbose_name='Tayyorlangan PDF')),
                ('status', models.CharField(choices=[('downloaded', 'Yuklab olingan'), ('pending', 'Kutilmoqda'), ('error', 'Xatolik')], default='pending', max_length=100, verbose_name='Status')),
            ],
            options={
                'verbose_name': 'GenerateModel',
                'verbose_name_plural': 'GenerateModels',
                'db_table': 'generate',
            },
        ),
    ]
