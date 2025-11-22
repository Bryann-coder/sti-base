# Module Tuteur Intelligent - Système de Formation Médicale

## Vue d'ensemble

Le module tuteur implémente un système intelligent de formation médicale basé sur la simulation de patients virtuels. Il permet aux apprenants du domaine de la santé de s'exercer au diagnostic médical dans un environnement contrôlé et adaptatif.

## Architecture du Système

### Modèles Principaux

#### 1. Gestion des Utilisateurs
- **ProfilUtilisateur**: Profil détaillé avec spécialité, niveau d'expertise, domaine
- **Utilisateur**: Liaison avec le système d'authentification Django

#### 2. Structure Pédagogique
- **Niveau**: Niveaux de formation (ex: Niveau 1 - Bases du diagnostic)
- **Etape**: Étapes flexibles au sein de chaque niveau
- **Session**: Sessions d'apprentissage individuelles

#### 3. Contenu Médical
- **CasClinique**: Cas de patients virtuels avec symptômes, diagnostics
- **Interaction**: Messages échangés entre l'apprenant et le tuteur
- **Erreur**: Erreurs détectées et corrections proposées

#### 4. Systèmes Intelligents
- **SystemeTuteur**: Orchestrateur principal du système
- **DetecteurErreur**: Détection automatique des erreurs via IA
- **SystemePedagogique**: Adaptation pédagogique personnalisée
- **SelecteurCas**: Sélection intelligente des cas cliniques

#### 5. Gamification
- **Gamification**: Système d'étoiles et de progression
- **StrategiePedagogique**: Stratégies d'enseignement adaptatives

## Fonctionnement

### Flux d'Interaction

1. **Démarrage de Session**
   - L'utilisateur démarre une session sur un niveau choisi
   - Le système sélectionne un cas clinique adapté au profil

2. **Interaction Chat**
   - L'apprenant envoie des messages au tuteur virtuel
   - Le système détecte les erreurs et difficultés
   - Une réponse pédagogique adaptée est générée

3. **Adaptation Continue**
   - Le système ajuste la stratégie selon les performances
   - Les cas cliniques peuvent être changés si nécessaire
   - Les erreurs sont corrigées en temps réel

4. **Évaluation et Progression**
   - Attribution d'étoiles selon la compréhension
   - Suivi de la progression par niveau
   - Déblocage de nouveaux niveaux selon les seuils

### Système de Gamification

- **Étoiles par Étape**: Chaque étape peut rapporter jusqu'à 5 étoiles
- **Seuil de Passage**: 20 étoiles minimum pour passer au niveau suivant
- **Évaluation Finale**: Test récapitulatif à la fin de chaque niveau

## API Endpoints

### Chat
```
POST /tutor/chat/
{
    "message": "Le patient a de la fièvre",
    "session_id": "optional_session_id"
}
```

### Progression
```
GET /tutor/progression/
```

### Session
```
POST /tutor/session/
DELETE /tutor/session/<session_id>/
```

## Installation et Configuration

### 1. Migrations
```bash
python manage.py makemigrations tutor
python manage.py migrate
```

### 2. Configuration de l'IA
Assurez-vous que la clé API Gemini est configurée dans le fichier `.env`:
```
GEMINI_API_KEY=your_api_key_here
```

### 3. Données de Test
Exécutez le script de test pour créer des données d'exemple:
```bash
python tutor/test_tuteur.py
```

## Utilisation

### Service Principal
```python
from tutor.services import TutorService

# Initialisation
tutor_service = TutorService(request.user)

# Interaction
resultat = tutor_service.handle_interaction(
    "Bonjour, je commence ma formation",
    session_id=None
)

# Progression
progression = tutor_service.get_progression()
```

### Système Tuteur Direct
```python
from tutor.tuteur_service import SystemeTuteur

systeme = SystemeTuteur()
resultat = systeme.traiter_message(utilisateur, message, session)
```

## Fonctionnalités Avancées

### Détection d'Erreurs IA
Le système utilise l'IA Gemini pour détecter automatiquement:
- Diagnostics incorrects
- Symptômes manqués
- Raisonnement médical flou
- Terminologie incorrecte

### Sélection Adaptative de Cas
Les cas cliniques sont sélectionnés selon:
- Le niveau d'expertise de l'utilisateur
- L'historique des sessions précédentes
- Les erreurs récurrentes identifiées
- La progression dans le niveau actuel

### Stratégies Pédagogiques
- **Approche Socratique**: Questions guidées
- **Correction Immédiate**: Feedback en temps réel
- **Adaptation Progressive**: Difficulté ajustée dynamiquement

## Tests

Le module inclut un système de tests complet:

```bash
python tutor/test_tuteur.py
```

Tests couverts:
- Interactions de base
- Détection d'erreurs
- Système de gamification
- Gestion des sessions
- Progression utilisateur

## Administration

Le module est intégré à l'interface d'administration Django pour:
- Gestion des cas cliniques
- Suivi des sessions utilisateurs
- Analyse des erreurs communes
- Configuration des stratégies pédagogiques

## Extensibilité

Le système est conçu pour être facilement extensible:
- Nouveaux types de cas cliniques
- Stratégies pédagogiques personnalisées
- Intégration d'autres modèles d'IA
- Métriques de performance avancées

## Sécurité et Confidentialité

- Toutes les interactions sont chiffrées
- Les données médicales sont anonymisées
- Respect des normes RGPD
- Audit trail complet des actions utilisateurs