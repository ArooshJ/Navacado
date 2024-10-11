# Generated by Django 4.2.3 on 2024-01-02 20:27

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Batch',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('bname', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Class',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('year', models.IntegerField()),
                ('division', models.CharField(max_length=1)),
                ('acad_year', models.CharField(max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='Course',
            fields=[
                ('cid', models.AutoField(primary_key=True, serialize=False)),
                ('cname', models.CharField(max_length=255)),
                ('semester', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Department',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('dname', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Faculty',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('department', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='faculty_members', to='ams.department')),
            ],
        ),
        migrations.CreateModel(
            name='Lab',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('date', models.DateField()),
                ('start_time', models.TimeField()),
                ('end_time', models.TimeField()),
                ('room', models.IntegerField(blank=True, null=True)),
                ('batch', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='labs', to='ams.batch')),
                ('course', models.ManyToManyField(related_name='labs', to='ams.course')),
                ('faculty', models.ManyToManyField(related_name='labs', to='ams.faculty')),
            ],
        ),
        migrations.CreateModel(
            name='Timetable',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('semester', models.IntegerField()),
                ('valid_from', models.DateField(blank=True, null=True)),
                ('valid_till', models.DateField(blank=True, null=True)),
                ('class_field', models.ManyToManyField(related_name='timetables', to='ams.class')),
            ],
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('profileid', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255)),
                ('email', models.EmailField(max_length=254)),
                ('phone', models.BigIntegerField()),
                ('date_of_birth', models.DateField()),
                ('is_cr', models.BooleanField(default=False)),
                ('is_br', models.BooleanField(default=False)),
                ('is_hod', models.BooleanField(default=False)),
                ('is_coursehead', models.BooleanField(default=False)),
                ('is_classIncharge', models.BooleanField(default=False)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='profile', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='TimeTableSlot',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('day', models.IntegerField()),
                ('start_time', models.TimeField()),
                ('end_time', models.TimeField()),
                ('lec_lab', models.BooleanField(default=True)),
                ('course', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='ams.course')),
                ('faculty', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='ams.faculty')),
                ('ttid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='time_table_slots', to='ams.timetable')),
            ],
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('uid', models.BigAutoField(primary_key=True, serialize=False)),
                ('joined_year', models.IntegerField()),
                ('batch', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='students', to='ams.batch')),
                ('class_field', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='students', to='ams.class')),
                ('profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='student', to='ams.userprofile')),
            ],
        ),
        migrations.CreateModel(
            name='Lecture',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('date', models.DateField()),
                ('start_time', models.TimeField()),
                ('end_time', models.TimeField()),
                ('room', models.IntegerField(blank=True, null=True)),
                ('class_field', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='lectures', to='ams.class')),
                ('course', models.ManyToManyField(related_name='lectures', to='ams.course')),
                ('faculty', models.ManyToManyField(related_name='lectures', to='ams.faculty')),
            ],
        ),
        migrations.CreateModel(
            name='LecAttendance',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('present', models.BooleanField()),
                ('lecid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='attendance', to='ams.lecture')),
                ('sid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='lecture_attendance', to='ams.student')),
            ],
        ),
        migrations.CreateModel(
            name='LabAttendance',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('present', models.BooleanField()),
                ('labid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='attendance', to='ams.lab')),
                ('sid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='lab_attendance', to='ams.student')),
            ],
        ),
        migrations.AddField(
            model_name='faculty',
            name='profile',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ams.userprofile'),
        ),
        migrations.AddField(
            model_name='department',
            name='hod',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='is_hod', to='ams.faculty'),
        ),
        migrations.AddField(
            model_name='course',
            name='department',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='courses', to='ams.department'),
        ),
        migrations.AddField(
            model_name='course',
            name='head',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='head_of_courses', to='ams.faculty'),
        ),
        migrations.AddField(
            model_name='class',
            name='cr',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='class_representatives', to='ams.student'),
        ),
        migrations.AddField(
            model_name='class',
            name='department',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='classes', to='ams.department'),
        ),
        migrations.AddField(
            model_name='class',
            name='incharge',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='incharged_class', to='ams.faculty'),
        ),
        migrations.AddField(
            model_name='batch',
            name='br',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='batch_representatives', to='ams.student'),
        ),
        migrations.AddField(
            model_name='batch',
            name='class_field',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='batches', to='ams.class'),
        ),
    ]
