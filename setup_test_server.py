#!/usr/bin/env python3
"""Script pour préparer le serveur de test"""

import os
import sys
import django

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sti.settings')
django.setup()

from django.contrib.auth.models import User
from tutor.models import *
import uuid

def create_test_data():
    """Crée des données de test pour le système tuteur"""
    
    print("🔧 Création des données de test...")
    
    # 1. Créer un utilisateur de test
    user, created = User.objects.get_or_create(
        username='tuteur_test',
        defaults={
            'email': 'tuteur@test.com',
            'first_name': 'Test',
            'last_name': 'Tuteur',
            'is_staff': False,
            'is_active': True
        }
    )
    
    if created:
        user.set_password('test123')
        user.save()
        print(f"✅ Utilisateur créé: {user.username}")
    else:
        print(f"ℹ️  Utilisateur existant: {user.username}")
    
    # 2. Créer des cas cliniques de test
    cas_cliniques = [
        {
            'id_cas': 'cas_fievre_001',
            'titre': 'Patient avec fièvre et céphalées',
            'description': 'Homme de 35 ans, fièvre 38.5°C, céphalées depuis 48h',
            'contexte_clinique': 'Consultation urgences, période hivernale',
            'symptomes': {
                'fievre': '38.5°C',
                'cephalees': 'intenses, frontales',
                'fatigue': 'importante',
                'frissons': 'présents'
            },
            'diagnostic_correct': 'Syndrome grippal',
            'diagnostics_differentiels': ['COVID-19', 'Méningite', 'Sinusite'],
            'niveau_difficulte': 'FACILE',
            'etat_mental_patient': 'Anxieux mais coopératif'
        },
        {
            'id_cas': 'cas_douleur_002',
            'titre': 'Douleur thoracique aiguë',
            'description': 'Femme de 45 ans, douleur thoracique brutale',
            'contexte_clinique': 'Urgences, douleur depuis 2h',
            'symptomes': {
                'douleur_thoracique': 'intense, constrictive',
                'dyspnee': 'légère',
                'sueurs': 'profuses',
                'nausees': 'présentes'
            },
            'diagnostic_correct': 'Syndrome coronarien aigu',
            'diagnostics_differentiels': ['Embolie pulmonaire', 'Péricardite', 'Reflux gastro-œsophagien'],
            'niveau_difficulte': 'MOYEN',
            'etat_mental_patient': 'Très anxieux, douloureux'
        },
        {
            'id_cas': 'cas_pediatrie_003',
            'titre': 'Enfant avec éruption cutanée',
            'description': 'Enfant de 6 ans, éruption généralisée avec fièvre',
            'contexte_clinique': 'Cabinet pédiatrique, parents inquiets',
            'symptomes': {
                'eruption': 'maculopapuleuse généralisée',
                'fievre': '39°C',
                'toux': 'sèche',
                'conjonctivite': 'bilatérale'
            },
            'diagnostic_correct': 'Rougeole',
            'diagnostics_differentiels': ['Rubéole', 'Scarlatine', 'Exanthème viral'],
            'niveau_difficulte': 'DIFFICILE',
            'etat_mental_patient': 'Enfant grognon, parents anxieux'
        }
    ]
    
    for cas_data in cas_cliniques:
        cas, created = CasClinique.objects.get_or_create(
            id_cas=cas_data['id_cas'],
            defaults=cas_data
        )
        if created:
            print(f"✅ Cas clinique créé: {cas.titre}")
        else:
            print(f"ℹ️  Cas existant: {cas.titre}")
    
    # 3. Créer une stratégie pédagogique par défaut
    strategie, created = StrategiePedagogique.objects.get_or_create(
        id_strategie='strategie_socratique',
        defaults={
            'nom': 'Méthode Socratique',
            'type_approche': 'SOCRATIQUE',
            'parametres': {
                'questions_guidees': True,
                'feedback_immediat': True,
                'adaptation_niveau': True
            },
            'niveau_adaptation': 3
        }
    )
    
    if created:
        print("✅ Stratégie pédagogique créée")
    
    # 4. Créer le système de gamification
    gamif, created = Gamification.objects.get_or_create(
        id_gamification='gamif_default',
        defaults={
            'points_par_etape': {
                'etape_1': 5,
                'etape_2': 5,
                'etape_3': 5,
                'etape_4': 5,
                'etape_5': 5
            },
            'seuil_passage_niveau': 20,
            'recompenses': {
                'niveau_1': 'Badge Apprenti Médecin',
                'niveau_2': 'Badge Diagnostic Expert',
                'niveau_3': 'Badge Maître Clinicien'
            }
        }
    )
    
    if created:
        print("✅ Système de gamification créé")
    
    print(f"\n🎯 Données de test prêtes !")
    print(f"👤 Utilisateur test: tuteur_test / test123")
    print(f"📋 {len(cas_cliniques)} cas cliniques disponibles")
    print(f"🎮 Système de gamification configuré")

def show_api_info():
    """Affiche les informations sur l'API"""
    
    print("\n" + "="*60)
    print("🚀 SERVEUR DE TEST PRÊT")
    print("="*60)
    
    print("\n📡 ENDPOINTS DISPONIBLES:")
    print("├── POST /api-token-auth/           # Obtenir token")
    print("├── POST /api/tutor/chat/           # Chat avec tuteur")
    print("├── GET  /api/tutor/progression/    # Voir progression")
    print("├── POST /api/tutor/session/        # Nouvelle session")
    print("└── DELETE /api/tutor/session/{id}/ # Terminer session")
    
    print("\n🔐 AUTHENTIFICATION:")
    print("Username: tuteur_test")
    print("Password: test123")
    
    print("\n📝 EXEMPLES DE MESSAGES POUR POSTMAN:")
    print('• "Bonjour, je commence ma formation"')
    print('• "Le patient a de la fièvre et des maux de tête"')
    print('• "Je pense à un syndrome grippal"')
    print('• "Quels examens complémentaires recommandez-vous ?"')
    
    print("\n🧪 MESSAGES POUR TESTER LA DÉTECTION D'ERREURS:")
    print('• "C\'est forcément un cancer"')
    print('• "Je prescris des antibiotiques sans diagnostic"')
    print('• "Le patient ment sûrement"')
    
    print("\n🌐 URL DE BASE: http://localhost:8000")
    print("📖 Guide complet: GUIDE_POSTMAN_TUTEUR.md")
    
    print("\n" + "="*60)

def main():
    print("🏥 Configuration du Serveur de Test - Module Tuteur")
    print("="*60)
    
    try:
        # Créer les données de test
        create_test_data()
        
        # Afficher les informations
        show_api_info()
        
        print("\n✅ Configuration terminée avec succès !")
        print("\n🚀 Pour démarrer le serveur:")
        print("   python3 manage.py runserver")
        
    except Exception as e:
        print(f"\n❌ Erreur lors de la configuration: {e}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    main()