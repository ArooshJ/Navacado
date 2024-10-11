# Generated by Django 4.2.3 on 2024-01-26 16:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("ams", "0007_alter_department_hod_alter_faculty_profile_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="class",
            name="incharge",
            field=models.OneToOneField(
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="incharged_class",
                to="ams.faculty",
            ),
        ),
    ]
