# Generated by Django 4.2.3 on 2024-02-01 18:15

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("ams", "0010_timetableslot_batch"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="userprofile",
            name="is_br",
        ),
        migrations.RemoveField(
            model_name="userprofile",
            name="is_classIncharge",
        ),
        migrations.RemoveField(
            model_name="userprofile",
            name="is_coursehead",
        ),
        migrations.RemoveField(
            model_name="userprofile",
            name="is_cr",
        ),
        migrations.RemoveField(
            model_name="userprofile",
            name="is_hod",
        ),
    ]
