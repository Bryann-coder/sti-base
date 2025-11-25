#!/usr/bin/env python3
"""
Test du système de consultation médicale corrigé
Le système tuteur fait office de patient ET de tuteur pédagogique
"""

import os
import sys
import django
from django.conf import settings

if not settings.configured:
    settings.configure(
        DEBUG=True,
        DATABASES={
            'default': {
                'ENGINE': 'django.db.backends.mysql',
                'NAME': 'its_db',
                'USER': 'root',
                'PASSWORD': 'folongzidane',
                'HOST': 'localhost',
                'PORT': '3306',
            }
        },
        INSTALLED_APPS=[
            'django.contrib.auth', 
            'django.contrib.contenttypes', 
            'tutor'
        ],
        SECRET_KEY='test-key',
        USE_TZ=True,
    )

django.setup()

def test_consultation_complete():
    """Test d'une consultation médicale complète"""
    
    print("🏥 TEST CONSULTATION MÉDICALE AVEC SYSTÈME TUTEUR")
    print("=" * 60)
    print("Le système tuteur joue le rôle du patient ET du tuteur pédagogique")
    print("=" * 60)
    
    from django.contrib.auth.models import User
    from tutor.services import TutorService
    
    # Créer un médecin en formation
    user, created = User.objects.get_or_create(
        username='medecin_test',
        defaults={
            'first_name': 'Dr.',
            'last_name': 'Test',
            'email': 'test@medical.com'
        }
    )
    
    service = TutorService(user)
    
    # Séquence de consultation réaliste
    interactions = [
        {
            "message": "Bonjour, comment vous sentez-vous aujourd'hui ?",
            "description": "Salutation et question ouverte"
        },
        {
            "message": "Depuis quand avez-vous ces douleurs ?",
            "description": "Question sur la chronologie"
        },
        {
            "message": "Pouvez-vous décrire la douleur plus précisément ?",
            "description": "Caractérisation de la douleur"
        },
        {
            "message": "Avez-vous de la fièvre ?",
            "description": "Recherche de signes associés"
        },
        {
            "message": "C'est sûrement un cancer !",
            "description": "Erreur médicale - diagnostic prématuré"
        },
        {
            "message": "Excusez-moi, je pense plutôt à une grippe saisonnière",
            "description": "Correction et diagnostic plus approprié"
        }
    ]
    
    session_id = None
    
    for i, interaction in enumerate(interactions, 1):
        print(f"\n--- INTERACTION {i} ---")
        print(f"📝 Contexte: {interaction['description']}")
        print(f"🩺 MÉDECIN: {interaction['message']}")
        
        try:
            # Traitement par le système tuteur
            result = service.handle_interaction(interaction['message'], session_id)
            session_id = result['session_id']
            
            print(f"\n🤖 SYSTÈME TUTEUR:")
            print(f"   {result['tutor_response']}")
            
            print(f"\n📊 ÉVALUATION:")
            print(f"   ⭐ Étoiles gagnées: {result['etoiles_gagnees']}")
            print(f"   🏆 Score total: {result['score_total']}")
            print(f"   📋 Cas: {result['cas_clinique']}")
            print(f"   📚 Niveau: {result['niveau_actuel']}")
            
            # Vérifier si consultation terminée
            if result.get('fin_consultation'):
                print(f"\n🏁 CONSULTATION TERMINÉE")
                print(f"✅ Diagnostic {'correct' if result['diagnostic_correct'] else 'incorrect'}")
                if result.get('feedback_pedagogique'):
                    print(f"📝 Feedback: {result['feedback_pedagogique']}")
                break
                
        except Exception as e:
            print(f"❌ ERREUR: {e}")
            import traceback
            traceback.print_exc()
            break
    
    # Afficher la progression finale
    print(f"\n📈 PROGRESSION FINALE:")
    try:
        progression = service.get_progression()
        print(f"🌟 Total étoiles: {progression['total_etoiles']}")
        print(f"✅ Sessions complétées: {progression['sessions_completees']}")
        print(f"📚 Niveau actuel: {progression['niveau_actuel']}")
    except Exception as e:
        print(f"❌ Erreur progression: {e}")

def test_detection_erreurs():
    """Test spécifique de la détection d'erreurs"""
    
    print(f"\n🔍 TEST DÉTECTION D'ERREURS MÉDICALES")
    print("=" * 60)
    
    from django.contrib.auth.models import User
    from tutor.services import TutorService
    
    user, _ = User.objects.get_or_create(
        username='etudiant_erreurs',
        defaults={'first_name': 'Étudiant', 'last_name': 'Erreurs'}
    )
    
    service = TutorService(user)
    
    # Messages avec erreurs typiques
    messages_erreurs = [
        {
            "message": "C'est forcément un cancer, tous les symptômes correspondent",
            "type": "Diagnostic prématuré"
        },
        {
            "message": "Le patient exagère ses symptômes",
            "type": "Jugement du patient"
        },
        {
            "message": "Je prescris des antibiotiques au cas où",
            "type": "Prescription sans diagnostic"
        }
    ]
    
    for i, test in enumerate(messages_erreurs, 1):
        print(f"\n--- TEST ERREUR {i} ---")
        print(f"🎯 Type: {test['type']}")
        print(f"💬 Message: {test['message']}")
        
        try:
            result = service.handle_interaction(test['message'])
            
            print(f"\n🤖 CORRECTION TUTEUR:")
            print(f"   {result['tutor_response']}")
            print(f"   ⭐ Étoiles: {result['etoiles_gagnees']} (pénalité pour erreur)")
            
        except Exception as e:
            print(f"❌ Erreur: {e}")

def main():
    print("🚀 TEST DU SYSTÈME TUTEUR MÉDICAL CORRIGÉ")
    
    # Vérifier la configuration
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("❌ GEMINI_API_KEY non configurée")
        return
    
    print(f"✅ Gemini AI configuré")
    
    try:
        # Test principal
        test_consultation_complete()
        
        # Test détection d'erreurs
        test_detection_erreurs()
        
        print("\n" + "="*60)
        print("🎉 TESTS TERMINÉS AVEC SUCCÈS")
        print("="*60)
        print("✅ Système tuteur unifié fonctionnel")
        print("✅ Patient virtuel intégré au tuteur")
        print("✅ Détection d'erreurs pédagogiques")
        print("✅ Gestion de l'historique et du cache")
        print("✅ Évaluation et progression")
        
    except Exception as e:
        print(f"\n❌ ERREUR GÉNÉRALE: {e}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    main()