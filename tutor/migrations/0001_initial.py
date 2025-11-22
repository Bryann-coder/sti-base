# Generated manually for tutor models

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='ProfilUtilisateur',
            fields=[
                ('id_profil', models.CharField(max_length=50, primary_key=True, serialize=False)),
                ('specialite', models.CharField(max_length=100)),
                ('niveau_expertise', models.CharField(max_length=50)),
                ('niveau_app', models.CharField(max_length=50)),
                ('domaine', models.CharField(max_length=100)),
                ('competences', models.JSONField(default=list)),
                ('performance_par_domaine', models.JSONField(default=dict)),
            ],
        ),
        migrations.CreateModel(
            name='Utilisateur',
            fields=[
                ('id_utilisateur', models.CharField(max_length=50, primary_key=True, serialize=False)),
                ('nom', models.CharField(max_length=100)),
                ('prenom', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=254)),
                ('date_inscription', models.DateTimeField(default=django.utils.timezone.now)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('profil', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='tutor.profilutilisateur')),
            ],
        ),
        migrations.CreateModel(
            name='Niveau',
            fields=[
                ('id_niveau', models.CharField(max_length=50, primary_key=True, serialize=False)),
                ('nom', models.CharField(max_length=100)),
                ('description', models.TextField()),
                ('ordre', models.IntegerField()),
                ('nombre_etoiles_minimum', models.IntegerField(default=20)),
                ('test_final_actif', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='Etape',
            fields=[
                ('id_etape', models.CharField(max_length=50, primary_key=True, serialize=False)),
                ('nom', models.CharField(max_length=100)),
                ('description', models.TextField()),
                ('ordre', models.IntegerField()),
                ('nombre_etoiles_max', models.IntegerField(default=5)),
                ('obligatoire', models.BooleanField(default=False)),
                ('prerequis', models.JSONField(default=list)),
                ('niveau', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='etapes', to='tutor.niveau')),
            ],
        ),
        migrations.CreateModel(
            name='CasClinique',
            fields=[
                ('id_cas', models.CharField(max_length=50, primary_key=True, serialize=False)),
                ('titre', models.CharField(max_length=200)),
                ('description', models.TextField()),
                ('contexte_clinique', models.TextField()),
                ('symptomes', models.JSONField(default=dict)),
                ('diagnostic_correct', models.CharField(max_length=200)),
                ('diagnostics_differentiels', models.JSONField(default=list)),
                ('niveau_difficulte', models.CharField(max_length=50)),
                ('etat_mental_patient', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Erreur',
            fields=[
                ('id_erreur', models.CharField(max_length=50, primary_key=True, serialize=False)),
                ('type_erreur', models.CharField(max_length=100)),
                ('description', models.TextField()),
                ('contexte', models.TextField()),
                ('gravite', models.CharField(max_length=50)),
                ('suggestion_correction', models.TextField()),
                ('corrigee', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Interaction',
            fields=[
                ('id_interaction', models.CharField(max_length=50, primary_key=True, serialize=False)),
                ('message', models.TextField()),
                ('type_message', models.CharField(choices=[('QUESTION', 'Question'), ('REPONSE', 'Réponse'), ('CORRECTION', 'Correction'), ('FEEDBACK', 'Feedback'), ('SYSTEME', 'Système')], max_length=20)),
                ('timestamp', models.DateTimeField(default=django.utils.timezone.now)),
                ('auteur', models.CharField(max_length=100)),
                ('contient_erreur', models.BooleanField(default=False)),
                ('erreurs_detectees', models.ManyToManyField(blank=True, to='tutor.erreur')),
            ],
        ),
        migrations.CreateModel(
            name='Session',
            fields=[
                ('id_session', models.CharField(max_length=50, primary_key=True, serialize=False)),
                ('date_debut', models.DateTimeField(default=django.utils.timezone.now)),
                ('date_fin', models.DateTimeField(blank=True, null=True)),
                ('score_etoiles', models.IntegerField(default=0)),
                ('etat_session', models.CharField(default='ACTIVE', max_length=50)),
                ('objectif_session', models.TextField()),
                ('premiere_fois', models.BooleanField(default=True)),
                ('utilisateur', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sessions', to='tutor.utilisateur')),
                ('niveau', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tutor.niveau')),
                ('etape', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='tutor.etape')),
                ('cas_clinique', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='tutor.casclinique')),
                ('interactions', models.ManyToManyField(blank=True, to='tutor.interaction')),
            ],
        ),
        migrations.CreateModel(
            name='StrategiePedagogique',
            fields=[
                ('id_strategie', models.CharField(max_length=50, primary_key=True, serialize=False)),
                ('nom', models.CharField(max_length=100)),
                ('type_approche', models.CharField(max_length=100)),
                ('parametres', models.JSONField(default=dict)),
                ('niveau_adaptation', models.IntegerField(default=1)),
            ],
        ),
        migrations.CreateModel(
            name='Gamification',
            fields=[
                ('id_gamification', models.CharField(max_length=50, primary_key=True, serialize=False)),
                ('points_par_etape', models.JSONField(default=dict)),
                ('seuil_passage_niveau', models.IntegerField(default=20)),
                ('recompenses', models.JSONField(default=dict)),
            ],
        ),
    ]