#!/usr/bin/env python3
"""
Test interactif du système de consultation médicale
L'utilisateur pose ses propres questions au système tuteur
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

def test_consultation_interactive():
    """Test interactif où l'utilisateur pose ses propres questions"""
    
    print("🏥 CONSULTATION MÉDICALE INTERACTIVE")
    print("=" * 60)
    print("Vous êtes un médecin en formation.")
    print("Le système tuteur joue le rôle du patient ET vous guide pédagogiquement.")
    print("Posez vos questions librement au patient.")
    print("Tapez 'quit' pour quitter.")
    print("=" * 60)
    
    from django.contrib.auth.models import User
    from tutor.services import TutorService
    
    # Créer un médecin en formation
    user, created = User.objects.get_or_create(
        username='medecin_interactif',
        defaults={
            'first_name': 'Dr.',
            'last_name': 'Interactif',
            'email': 'interactif@medical.com'
        }
    )
    
    if created:
        print(f"✅ Nouveau médecin créé: Dr. {user.last_name}")
    else:
        print(f"👨⚕️ Connexion: Dr. {user.last_name}")
    
    service = TutorService(user)
    session_id = None
    interaction_count = 0
    
    print(f"\n🏥 Un nouveau patient arrive dans votre cabinet...")
    print(f"📋 Cas assigné automatiquement selon votre niveau")
    print(f"\n{'='*60}")
    
    while True:
        try:
            # Saisie de la question du médecin
            print(f"\n--- INTERACTION {interaction_count + 1} ---")
            question = input("🩺 Vous (Médecin): ").strip()
            
            # Vérifier si l'utilisateur veut quitter
            if question.lower() in ['quit', 'exit', 'quitter', 'q']:
                print("👋 Consultation interrompue. Au revoir !")
                break
            
            if not question:
                print("⚠️ Veuillez poser une question au patient.")
                continue
            
            interaction_count += 1
            
            # Traitement par le système tuteur
            print("🤖 Traitement en cours...")
            result = service.handle_interaction(question, session_id)
            session_id = result['session_id']
            
            # Affichage de la réponse du système tuteur
            print(f"\n🤒 SYSTÈME TUTEUR (Patient + Pédagogie):")
            print(f"   {result['tutor_response']}")
            
            # Affichage des métriques de performance
            print(f"\n📊 ÉVALUATION DE VOTRE QUESTION:")
            print(f"   ⭐ Étoiles gagnées: {result['etoiles_gagnees']}")
            print(f"   🏆 Score total session: {result['score_total']}")
            print(f"   📋 Cas clinique: {result['cas_clinique']}")
            print(f"   📚 Votre niveau: {result['niveau_actuel']}")
            
            # Vérifier si la consultation est terminée
            if result.get('fin_consultation'):
                print(f"\n🏁 CONSULTATION TERMINÉE !")
                print("=" * 60)
                
                if result.get('diagnostic_correct'):
                    print("🎉 FÉLICITATIONS ! Diagnostic correct !")
                else:
                    print("❌ Diagnostic incorrect ou incomplet")
                
                print(f"📈 Score final: {result['score_total']} étoiles")
                
                if result.get('feedback_pedagogique'):
                    print(f"\n📝 FEEDBACK PÉDAGOGIQUE FINAL:")
                    print(f"   {result['feedback_pedagogique']}")
                
                # Demander si l'utilisateur veut recommencer
                recommencer = input("\n🔄 Voulez-vous commencer une nouvelle consultation ? (o/n): ").strip().lower()
                if recommencer in ['o', 'oui', 'y', 'yes']:
                    session_id = None
                    interaction_count = 0
                    print(f"\n🆕 NOUVELLE CONSULTATION")
                    print("=" * 60)
                    continue
                else:
                    break
            
            print("-" * 40)
            
        except KeyboardInterrupt:
            print("\n\n👋 Consultation interrompue par l'utilisateur.")
            break
        except Exception as e:
            print(f"\n❌ ERREUR: {e}")
            print("Veuillez réessayer ou tapez 'quit' pour quitter.")
            import traceback
            traceback.print_exc()

def afficher_aide():
    """Affiche l'aide pour l'utilisateur"""
    print("\n💡 CONSEILS POUR UNE BONNE CONSULTATION:")
    print("- Commencez par une salutation: 'Bonjour, comment vous sentez-vous ?'")
    print("- Posez des questions ouvertes puis précises")
    print("- Explorez les symptômes: durée, intensité, facteurs déclenchants")
    print("- Recherchez les signes associés: fièvre, douleurs, etc.")
    print("- Terminez par un diagnostic: 'Je pense que vous avez...'")
    print("- Le système vous guidera et corrigera vos erreurs")

def main():
    print("🚀 SYSTÈME DE CONSULTATION MÉDICALE INTERACTIVE")
    
    # Vérifier la configuration Gemini
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("❌ GEMINI_API_KEY non configurée dans les variables d'environnement")
        return
    
    print(f"✅ Gemini AI configuré (clé: {api_key[:10]}...)")
    
    # Afficher l'aide
    afficher_aide()
    
    # Demander si l'utilisateur veut commencer
    print("\n" + "="*60)
    commencer = input("🏥 Prêt à commencer la consultation ? (o/n): ").strip().lower()
    
    if commencer in ['o', 'oui', 'y', 'yes']:
        try:
            test_consultation_interactive()
        except Exception as e:
            print(f"\n❌ ERREUR GÉNÉRALE: {e}")
            import traceback
            traceback.print_exc()
    else:
        print("👋 À bientôt pour votre formation médicale !")

if __name__ == '__main__':
    main()