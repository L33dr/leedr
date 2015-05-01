# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('leaderboard', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Game',
            new_name='GameDetail',
        ),
        migrations.RemoveField(
            model_name='usergameprofile',
            name='game_user_id',
        ),
        migrations.RemoveField(
            model_name='userprofile',
            name='games',
        ),
        migrations.AddField(
            model_name='usergameprofile',
            name='user',
            field=models.ForeignKey(default='', to='leaderboard.UserProfile'),
            preserve_default=False,
        ),
    ]
