# Generated by Django 2.2.24 on 2021-07-05 17:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0005_community_communitymessage_communitymessageboard'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='email_reconfirmed_at',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='pending_email_reconfirmation',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
