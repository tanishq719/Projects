# Generated by Django 3.0.3 on 2020-06-09 03:57

import django.contrib.postgres.fields.jsonb
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Dislikes',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'db_table': 'dislikes',
            },
        ),
        migrations.CreateModel(
            name='Image',
            fields=[
                ('img_id', models.IntegerField(primary_key=True, serialize=False)),
                ('link_to_img', models.CharField(max_length=100)),
            ],
            options={
                'db_table': 'image',
            },
        ),
        migrations.CreateModel(
            name='Likes',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'db_table': 'likes',
            },
        ),
        migrations.CreateModel(
            name='Reply',
            fields=[
                ('reply_id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('creation_date', models.DateField(auto_now_add=True)),
                ('edit_date', models.DateTimeField(auto_now=True)),
                ('like_count', models.IntegerField(blank=True, default=0)),
                ('dislike_count', models.IntegerField(blank=True, default=0)),
                ('reply_count', models.IntegerField(blank=True, default=0)),
                ('txt_body', models.TextField()),
            ],
            options={
                'db_table': 'reply',
            },
        ),
        migrations.CreateModel(
            name='Thread',
            fields=[
                ('th_id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=200)),
                ('view_count', models.IntegerField(blank=True, default=0)),
                ('body', models.OneToOneField(db_column='body', on_delete=django.db.models.deletion.CASCADE, related_name='attached_to', to='discussions.Reply')),
                ('t_creator', models.ForeignKey(blank=True, db_column='t_creator', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='created_thread', to='users.Users')),
            ],
            options={
                'db_table': 'thread',
            },
        ),
        migrations.CreateModel(
            name='Group_closes_reply',
            fields=[
                ('reply_id', models.OneToOneField(db_column='reply_id', on_delete=django.db.models.deletion.CASCADE, primary_key=True, related_name='reply_closed_by', serialize=False, to='discussions.Reply')),
                ('reason', django.contrib.postgres.fields.jsonb.JSONField()),
            ],
            options={
                'db_table': 'grp_closes_reply',
            },
        ),
        migrations.CreateModel(
            name='Grp_closes_thread',
            fields=[
                ('th_id', models.OneToOneField(db_column='th_id', on_delete=django.db.models.deletion.DO_NOTHING, primary_key=True, related_name='thread_closed_by', serialize=False, to='discussions.Thread')),
                ('reason', django.contrib.postgres.fields.jsonb.JSONField()),
            ],
            options={
                'db_table': 'group_close_thread',
            },
        ),
        migrations.CreateModel(
            name='User_delete_reply',
            fields=[
                ('reply_id', models.OneToOneField(db_column='reply_id', on_delete=django.db.models.deletion.DO_NOTHING, primary_key=True, related_name='reply_deleted_by', serialize=False, to='discussions.Reply')),
            ],
            options={
                'db_table': 'user_delete_reply',
            },
        ),
    ]
