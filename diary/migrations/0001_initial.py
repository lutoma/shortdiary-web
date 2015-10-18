# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone
from django.conf import settings
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='DiaryUser',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(default=django.utils.timezone.now, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(help_text='Required. 30 characters or fewer. Letters, digits and @/./+/-/_ only.', unique=True, max_length=30, verbose_name='username', validators=[django.core.validators.RegexValidator('^[\\w.@+-]+$', 'Enter a valid username.', 'invalid')])),
                ('first_name', models.CharField(max_length=30, verbose_name='first name', blank=True)),
                ('last_name', models.CharField(max_length=30, verbose_name='last name', blank=True)),
                ('email', models.EmailField(max_length=75, verbose_name='email address', blank=True)),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('invites_left', models.IntegerField(default=5, verbose_name='invites left')),
                ('last_seen_at', models.DateTimeField(null=True, verbose_name='last seen at', blank=True)),
                ('mail_verified', models.BooleanField(default=False, verbose_name='email verified?')),
                ('language', models.CharField(default=b'en_US', max_length=5, verbose_name='language')),
                ('geolocation_enabled', models.BooleanField(default=True, verbose_name='Post location enabled')),
                ('groups', models.ManyToManyField(related_query_name='user', related_name='user_set', to='auth.Group', blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of his/her group.', verbose_name='groups')),
                ('invited_by', models.ForeignKey(related_name=b'user_invited_by', verbose_name='invited by', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
                ('user_permissions', models.ManyToManyField(related_query_name='user', related_name='user_set', to='auth.Permission', blank=True, help_text='Specific permissions for this user.', verbose_name='user permissions')),
            ],
            options={
                'abstract': False,
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='created at')),
                ('gateway', models.CharField(max_length=200, verbose_name='payment gateway')),
                ('gateway_identifier', models.CharField(max_length=500, verbose_name='identifier of this payment at payment gateway')),
                ('amount', models.IntegerField(verbose_name='amount paid')),
                ('currency', models.CharField(max_length=3, verbose_name='currency')),
                ('valid_from', models.DateTimeField(verbose_name='payment valid from')),
                ('valid_until', models.DateTimeField(verbose_name='payment valid until')),
                ('recurring', models.BooleanField(verbose_name='recurring')),
                ('user', models.ForeignKey(verbose_name='paying user', to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date', models.DateField(verbose_name=b'date')),
                ('text', models.TextField(max_length=350, verbose_name='text')),
                ('mood', models.IntegerField(verbose_name='mood')),
                ('image', models.ImageField(upload_to=b'postimages/%d%m%y/', verbose_name='image', blank=True)),
                ('public', models.BooleanField(default=False, verbose_name='public')),
                ('part_of', models.CharField(max_length=600, null=True, verbose_name='part of', blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='created at')),
                ('last_changed_at', models.DateTimeField(auto_now=True, verbose_name='last changed at')),
                ('sent', models.BooleanField(default=False, verbose_name='mail sent?')),
                ('location_lat', models.DecimalField(null=True, verbose_name='Location latitude', max_digits=16, decimal_places=12, blank=True)),
                ('location_lon', models.DecimalField(null=True, verbose_name='Location longitude', max_digits=16, decimal_places=12, blank=True)),
                ('location_verbose', models.CharField(max_length=400, verbose_name='Location name', blank=True)),
                ('natural_language', models.CharField(max_length=5, null=True, verbose_name='Natural language', blank=True)),
                ('author', models.ForeignKey(verbose_name='author', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'post',
                'verbose_name_plural': 'posts',
            },
            bases=(models.Model,),
        ),
    ]
