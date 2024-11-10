# Generated by Django 2.2.28 on 2024-11-08 07:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vote', '0003_auto_20181124_1748'),
    ]

    operations = [
        migrations.AddField(
            model_name='vote',
            name='party_uniformity',
            field=models.FloatField(blank=True, help_text="A party uniformity score based on the percent of each party voting yes. Null for votes that aren't yes/no (like election of the speaker, quorum calls).", null=True),
        ),
    ]
