# Generated by Django 5.1.6 on 2025-03-19 22:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ij', '0006_remove_couplagecritere_critere_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='contrainte',
            old_name='nom',
            new_name='critere_cible',
        ),
        migrations.RemoveField(
            model_name='contrainte',
            name='idCriterefk',
        ),
        migrations.AddField(
            model_name='contrainte',
            name='seuil',
            field=models.CharField(default=1, max_length=255),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='contrainte',
            name='type',
            field=models.CharField(default=1, max_length=10),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='contrainte',
            name='description',
            field=models.CharField(max_length=255),
        ),
    ]
