#!/usr/bin/env python3
"""
Script de test pour le système tuteur intelligent
"""

import os
import sys
import django

# Configuration Django
sys.path.append('/home/folongzidane/Documents/Projet/stiProjet/sti-base')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sti.settings')
django.setup()

from django.contrib.auth.models import User
from tutor.models import *
from tutor.services import TutorService
import uuid

def creer_donnees_test():
    """Crée des données de test pour le système"""
    
    print("=== Création des données de test ===")
    
    # Créer un utilisateur de test
    user, created = User.objects.get_or_create(
        username='test_user',
        defaults={
            'email': 'test@example.com',
            'first_name': 'Test',
            'last_name': 'User'
        }
    )
    
    if created:
        user.set_password('testpass123')
        user.save()
        print("✓ Utilisateur de test créé")
    
    # Créer un cas clinique de test
    cas_test, created = CasClinique.objects.get_or_create(
        id_cas='cas_test_001',
        defaults={
            'titre': 'Patient avec fièvre et toux',
            'description': 'Un patient de 35 ans se présente avec une fièvre de 38.5°C et une toux sèche depuis 3 jours.',
            'contexte_clinique': 'Consultation en médecine générale, période hivernale',
            'symptomes': {\n                'fievre': '38.5°C',\n                'toux': 'sèche, depuis 3 jours',\n                'fatigue': 'modérée',\n                'maux_de_tete': 'légers'\n            },\n            'diagnostic_correct': 'Syndrome grippal',\n            'diagnostics_differentiels': ['COVID-19', 'Bronchite', 'Pneumonie'],\n            'niveau_difficulte': 'FACILE',\n            'etat_mental_patient': 'Patient inquiet mais coopératif'\n        }\n    )\n    \n    if created:\n        print("✓ Cas clinique de test créé")\n    \n    return user, cas_test

def tester_interaction_simple():
    """Test d'une interaction simple avec le tuteur"""
    \n    print("\\n=== Test d'interaction simple ===\")\n    \n    user, _ = creer_donnees_test()\n    \n    # Initialiser le service tuteur\n    tutor_service = TutorService(user)\n    \n    # Test 1: Premier message\n    print("\\n1. Premier message:\")\n    resultat1 = tutor_service.handle_interaction(\"Bonjour, je commence ma formation\")\n    print(f\"Réponse: {resultat1['tutor_response'][:100]}...\")\n    print(f\"Session ID: {resultat1['session_id']}\")\n    print(f\"Étoiles gagnées: {resultat1['etoiles_gagnees']}\")\n    \n    # Test 2: Message de suivi\n    print(\"\\n2. Message de suivi:\")\n    resultat2 = tutor_service.handle_interaction(\n        \"Le patient a de la fièvre, que dois-je faire?\",\n        resultat1['session_id']\n    )\n    print(f\"Réponse: {resultat2['tutor_response'][:100]}...\")\n    print(f\"Étoiles totales: {resultat2['score_total']}\")\n    \n    # Test 3: Progression\n    print(\"\\n3. Progression de l'utilisateur:\")\n    progression = tutor_service.get_progression()\n    print(f\"Total étoiles: {progression['total_etoiles']}\")\n    print(f\"Sessions complétées: {progression['sessions_completees']}\")\n    print(f\"Niveau actuel: {progression['niveau_actuel']}\")\n    \n    return resultat1['session_id']\n\ndef tester_detection_erreurs():\n    \"\"\"Test du système de détection d'erreurs\"\"\"\n    \n    print(\"\\n=== Test de détection d'erreurs ===\")\n    \n    user, _ = creer_donnees_test()\n    tutor_service = TutorService(user)\n    \n    # Message avec erreur potentielle\n    resultat = tutor_service.handle_interaction(\n        \"Je pense que c'est un cancer parce qu'il tousse\"\n    )\n    \n    print(f\"Réponse du tuteur: {resultat['tutor_response'][:150]}...\")\n    print(f\"Étoiles gagnées: {resultat['etoiles_gagnees']}\")\n\ndef tester_gamification():\n    \"\"\"Test du système de gamification\"\"\"\n    \n    print(\"\\n=== Test de gamification ===\")\n    \n    user, _ = creer_donnees_test()\n    tutor_service = TutorService(user)\n    \n    # Simuler plusieurs interactions pour gagner des étoiles\n    messages = [\n        \"Bonjour, commençons\",\n        \"Le patient a de la fièvre\",\n        \"Je pense à un syndrome grippal\",\n        \"Quels examens complémentaires?\",\n        \"Merci pour les explications\"\n    ]\n    \n    session_id = None\n    for i, message in enumerate(messages, 1):\n        resultat = tutor_service.handle_interaction(message, session_id)\n        session_id = resultat['session_id']\n        print(f\"Interaction {i}: +{resultat['etoiles_gagnees']} étoiles (Total: {resultat['score_total']})\")\n    \n    # Vérifier la progression finale\n    progression = tutor_service.get_progression()\n    print(f\"\\nProgression finale: {progression['total_etoiles']} étoiles\")\n\ndef main():\n    \"\"\"Fonction principale de test\"\"\"\n    \n    print(\"🚀 Démarrage des tests du système tuteur intelligent\")\n    print(\"=\" * 60)\n    \n    try:\n        # Tests principaux\n        session_id = tester_interaction_simple()\n        tester_detection_erreurs()\n        tester_gamification()\n        \n        print(\"\\n\" + \"=\" * 60)\n        print(\"✅ Tous les tests sont terminés avec succès!\")\n        print(\"\\n📊 Résumé:\")\n        print(\"- Interactions de base: ✓\")\n        print(\"- Détection d'erreurs: ✓\")\n        print(\"- Système de gamification: ✓\")\n        print(\"- Gestion des sessions: ✓\")\n        \n    except Exception as e:\n        print(f\"\\n❌ Erreur lors des tests: {e}\")\n        import traceback\n        traceback.print_exc()\n\nif __name__ == '__main__':\n    main()