# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-11-11 23:24
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import mainapp.models.userProfile


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('auth', '0007_alter_validators_add_error_messages'),
    ]

    operations = [
        migrations.CreateModel(
            name='DepartmentModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=256, verbose_name='Department Title')),
            ],
            options={
                'verbose_name': 'Department',
                'verbose_name_plural': 'Departments',
            },
        ),
        migrations.CreateModel(
            name='Disciplines',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('discipline', models.CharField(max_length=255, verbose_name='Discipline')),
            ],
            options={
                'verbose_name': 'Discipline',
                'verbose_name_plural': 'Disciplines',
            },
        ),
        migrations.CreateModel(
            name='FacultyModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=256, verbose_name='Faculty Title')),
                ('faculty_address', models.CharField(blank=True, max_length=1000, null=True, verbose_name='Faculty address')),
            ],
            options={
                'verbose_name': 'Faculty',
                'verbose_name_plural': 'Faculties',
            },
        ),
        migrations.CreateModel(
            name='Para',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('week_type', models.BooleanField(default=True, verbose_name='Is week even')),
            ],
            options={
                'verbose_name': 'Class',
                'verbose_name_plural': 'Classes',
            },
        ),
        migrations.CreateModel(
            name='ParaTime',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('para_starttime', models.TimeField(blank=True, null=True, verbose_name='Starts at')),
                ('para_endtime', models.TimeField(blank=True, null=True, verbose_name='Ends')),
                ('para_position', models.IntegerField(blank=True, default=0, null=True, verbose_name='Class order')),
                ('faculty', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mainapp.FacultyModel', verbose_name='Faculty ')),
            ],
            options={
                'verbose_name': 'Class schedule',
                'verbose_name_plural': 'Class schedule',
            },
        ),
        migrations.CreateModel(
            name='ProfileModel',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('is_student', models.BooleanField(default=True, verbose_name='Student')),
                ('is_professor', models.BooleanField(default=False, verbose_name='Professor')),
                ('is_staff', models.BooleanField(default=False, verbose_name='Staff Member')),
                ('started_date', models.DateField(auto_now_add=True, verbose_name='Started Working/Studying')),
                ('middle_name', models.CharField(blank=True, default='', max_length=256, verbose_name='Middle Name')),
                ('birthday', models.DateField(blank=True, null=True, verbose_name='Date of Birth')),
                ('contact_phone', models.CharField(blank=True, max_length=55, null=True, verbose_name='Contact Phone')),
                ('photo', models.ImageField(blank=True, null=True, upload_to=mainapp.models.userProfile.user_directory_path, verbose_name='Photo')),
                ('chat_id', models.CharField(blank=True, max_length=256, null=True, verbose_name='Telegram Chat ID')),
                ('department', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='mainapp.DepartmentModel', verbose_name='Department')),
                ('faculty', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='mainapp.FacultyModel', verbose_name='Faculty')),
            ],
        ),
        migrations.CreateModel(
            name='Rooms',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('room', models.CharField(max_length=10, verbose_name='Room')),
                ('faculty', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mainapp.FacultyModel', verbose_name='Faculty')),
            ],
            options={
                'verbose_name': 'Room',
                'verbose_name_plural': 'Rooms',
            },
        ),
        migrations.CreateModel(
            name='StartSemester',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(default='1st Semester', max_length=255, null=True, verbose_name='Semester')),
                ('semesterstart', models.DateField(verbose_name='Start at')),
                ('semesterend', models.DateField(verbose_name='Ends')),
            ],
            options={
                'verbose_name': 'Semester schedule',
                'verbose_name_plural': "Semester's schedule",
            },
        ),
        migrations.CreateModel(
            name='StudentGroupModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=256, verbose_name='Group Title')),
                ('date_started', models.DateField(verbose_name='Started date')),
                ('department', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mainapp.DepartmentModel', verbose_name='Department')),
                ('leader', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='group', to='mainapp.ProfileModel', verbose_name='Leader')),
            ],
            options={
                'verbose_name': 'Student Group',
                'verbose_name_plural': 'Student Groups',
            },
        ),
        migrations.CreateModel(
            name='StudentJournalModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.CharField(blank=True, default='', max_length=55, null=True, verbose_name='Value')),
                ('date', models.DateField(verbose_name='Date')),
                ('is_module', models.BooleanField(verbose_name='Module value')),
                ('discipline', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mainapp.Disciplines', verbose_name='Discipline')),
                ('para_number', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mainapp.ParaTime', verbose_name='Class #')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Student')),
            ],
            options={
                'verbose_name': 'Student Journal',
                'verbose_name_plural': 'Student Journal',
            },
        ),
        migrations.CreateModel(
            name='WorkingDay',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dayoftheweek', models.CharField(blank=True, max_length=50, null=True)),
                ('dayoftheweeknumber', models.IntegerField(blank=True, null=True)),
            ],
            options={
                'verbose_name': 'Day',
                'verbose_name_plural': 'Days',
            },
        ),
        migrations.AddField(
            model_name='profilemodel',
            name='student_group',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='mainapp.StudentGroupModel', verbose_name='Group'),
        ),
        migrations.AddField(
            model_name='para',
            name='para_day',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='mainapp.WorkingDay', verbose_name='Working day'),
        ),
        migrations.AddField(
            model_name='para',
            name='para_group',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='mainapp.StudentGroupModel', verbose_name='Student Group'),
        ),
        migrations.AddField(
            model_name='para',
            name='para_number',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='mainapp.ParaTime', verbose_name='Class Starts/Ends'),
        ),
        migrations.AddField(
            model_name='para',
            name='para_professor',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='mainapp.ProfileModel', verbose_name='Professor'),
        ),
        migrations.AddField(
            model_name='para',
            name='para_room',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='mainapp.Rooms', verbose_name='Room'),
        ),
        migrations.AddField(
            model_name='para',
            name='para_subject',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='mainapp.Disciplines', verbose_name='Discipline'),
        ),
        migrations.AddField(
            model_name='para',
            name='semester',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='mainapp.StartSemester', verbose_name='Semester'),
        ),
        migrations.AddField(
            model_name='facultymodel',
            name='dean',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='mainapp.ProfileModel', verbose_name='Dean'),
        ),
        migrations.AddField(
            model_name='departmentmodel',
            name='faculty',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mainapp.FacultyModel', verbose_name='Faculty'),
        ),
        migrations.AddField(
            model_name='departmentmodel',
            name='leader',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='mainapp.ProfileModel', verbose_name='Head of Department'),
        ),
    ]
