from django.contrib import admin
from .models import *

@admin.register(ProfilUtilisateur)
class ProfilUtilisateurAdmin(admin.ModelAdmin):
    list_display = ['id_profil', 'specialite', 'niveau_expertise', 'domaine']
    search_fields = ['specialite', 'domaine']

@admin.register(Utilisateur)
class UtilisateurAdmin(admin.ModelAdmin):
    list_display = ['id_utilisateur', 'nom', 'prenom', 'email', 'date_inscription']
    search_fields = ['nom', 'prenom', 'email']
    list_filter = ['date_inscription']

@admin.register(Niveau)
class NiveauAdmin(admin.ModelAdmin):
    list_display = ['id_niveau', 'nom', 'ordre', 'nombre_etoiles_minimum']
    list_filter = ['test_final_actif']
    ordering = ['ordre']

@admin.register(Etape)
class EtapeAdmin(admin.ModelAdmin):
    list_display = ['id_etape', 'nom', 'niveau', 'ordre', 'nombre_etoiles_max']
    list_filter = ['niveau', 'obligatoire']
    ordering = ['niveau', 'ordre']

@admin.register(CasClinique)
class CasCliniqueAdmin(admin.ModelAdmin):
    list_display = ['id_cas', 'titre', 'niveau_difficulte']
    list_filter = ['niveau_difficulte']
    search_fields = ['titre', 'description']

@admin.register(Session)
class SessionAdmin(admin.ModelAdmin):
    list_display = ['id_session', 'utilisateur', 'niveau', 'score_etoiles', 'etat_session', 'date_debut']
    list_filter = ['etat_session', 'niveau', 'date_debut']
    search_fields = ['utilisateur__nom', 'utilisateur__prenom']

@admin.register(Interaction)
class InteractionAdmin(admin.ModelAdmin):
    list_display = ['id_interaction', 'auteur', 'type_message', 'timestamp', 'contient_erreur']
    list_filter = ['type_message', 'contient_erreur', 'timestamp']
    search_fields = ['message', 'auteur']

@admin.register(Erreur)
class ErreurAdmin(admin.ModelAdmin):
    list_display = ['id_erreur', 'type_erreur', 'gravite', 'corrigee']
    list_filter = ['type_erreur', 'gravite', 'corrigee']
    search_fields = ['description']

@admin.register(StrategiePedagogique)
class StrategiePedagogiqueAdmin(admin.ModelAdmin):
    list_display = ['id_strategie', 'nom', 'type_approche', 'niveau_adaptation']
    list_filter = ['type_approche']

@admin.register(Gamification)
class GamificationAdmin(admin.ModelAdmin):
    list_display = ['id_gamification', 'seuil_passage_niveau']
    list_filter = ['seuil_passage_niveau']
