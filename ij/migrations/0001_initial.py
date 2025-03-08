# Generated by Django 5.1.6 on 2025-03-07 23:52

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Contrainte',
            fields=[
                ('idContrainte', models.AutoField(primary_key=True, serialize=False)),
                ('nom', models.CharField(max_length=50)),
                ('description', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Critere',
            fields=[
                ('idCritere', models.AutoField(primary_key=True, serialize=False)),
                ('nom', models.CharField(max_length=50)),
                ('description', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Element',
            fields=[
                ('codeElement', models.CharField(max_length=50, primary_key=True, serialize=False, unique=True)),
                ('description', models.CharField(default='Aucune description', max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Objectif',
            fields=[
                ('idObjectif', models.AutoField(primary_key=True, serialize=False)),
                ('description', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Ressource',
            fields=[
                ('codeRessource', models.CharField(max_length=50, primary_key=True, serialize=False, unique=True)),
                ('description', models.CharField(default='Aucune description', max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Couplage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('element', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ij.element')),
                ('ressource', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ij.ressource')),
            ],
        ),
        migrations.CreateModel(
            name='Solution',
            fields=[
                ('idSolution', models.AutoField(primary_key=True, serialize=False)),
                ('statut', models.TextField()),
                ('couplages', models.ManyToManyField(related_name='solutions', to='ij.couplage')),
                ('solution', models.ManyToManyField(related_name='solutions', to='ij.objectif')),
            ],
        ),
    ]
