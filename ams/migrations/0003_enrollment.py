# Generated by Django 4.2.3 on 2024-01-04 19:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ams', '0002_alter_userprofile_email_alter_userprofile_phone'),
    ]

    operations = [
        migrations.CreateModel(
            name='Enrollment',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('cid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ams.course')),
                ('sid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ams.student')),
            ],
        ),
    ]