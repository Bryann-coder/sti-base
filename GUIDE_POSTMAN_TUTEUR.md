# 📡 Guide Postman - Module Tuteur Intelligent

## 🔧 **Configuration Initiale**

### 1. Variables d'Environnement Postman
Créez un environnement avec ces variables :
```
BASE_URL: http://localhost:8000
TOKEN: {{auth_token}}
```

### 2. Démarrer le Serveur Django
```bash
cd /home/folongzidane/Documents/Projet/stiProjet/sti-base
python3 manage.py runserver
```

## 🔐 **Authentification**

### Étape 1: Créer un Utilisateur (Admin Django)
1. Aller sur `http://localhost:8000/admin/`
2. Créer un superuser si nécessaire :
   ```bash
   python3 manage.py createsuperuser
   ```
3. Créer un utilisateur normal dans l'interface admin

### Étape 2: Obtenir un Token d'Authentification

**POST** `{{BASE_URL}}/api-token-auth/`

**Headers:**
```
Content-Type: application/json
```

**Body (JSON):**
```json
{
    "username": "votre_username",
    "password": "votre_password"
}
```

**Réponse Attendue:**
```json
{
    "token": "9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b"
}
```

> 💡 **Copiez ce token** et ajoutez-le à vos variables d'environnement Postman

## 🤖 **Tests du Module Tuteur**

### Test 1: Première Interaction avec le Tuteur

**POST** `{{BASE_URL}}/api/tutor/chat/`

**Headers:**
```
Content-Type: application/json
Authorization: Token {{TOKEN}}
```

**Body (JSON):**
```json
{
    "message": "Bonjour, je commence ma formation en médecine"
}
```

**Réponse Attendue:**
```json
{
    "success": true,
    "data": {
        "tutor_response": "Bonjour ! Je suis votre tuteur médical...",
        "session_id": "uuid-de-la-session",
        "etoiles_gagnees": 3,
        "score_total": 3,
        "cas_clinique": "Patient avec fièvre",
        "niveau_actuel": "Niveau 1 - Bases du diagnostic"
    }
}
```

### Test 2: Interaction avec Cas Médical

**POST** `{{BASE_URL}}/api/tutor/chat/`

**Headers:**
```
Content-Type: application/json
Authorization: Token {{TOKEN}}
```

**Body (JSON):**
```json
{
    "message": "Le patient se plaint de maux de tête et de fièvre depuis 2 jours",
    "session_id": "uuid-de-la-session-precedente"
}
```

**Réponse Attendue:**
```json
{
    "success": true,
    "data": {
        "tutor_response": "Excellente observation ! La fièvre et les maux de tête sont des symptômes importants...",
        "session_id": "uuid-de-la-session",
        "etoiles_gagnees": 4,
        "score_total": 7,
        "cas_clinique": "Patient avec fièvre",
        "niveau_actuel": "Niveau 1 - Bases du diagnostic"
    }
}
```

### Test 3: Message avec Erreur Médicale

**POST** `{{BASE_URL}}/api/tutor/chat/`

**Headers:**
```
Content-Type: application/json
Authorization: Token {{TOKEN}}
```

**Body (JSON):**
```json
{
    "message": "C'est sûrement un cancer, je prescris de la chimiothérapie",
    "session_id": "uuid-de-la-session"
}
```

**Réponse Attendue:**
```json
{
    "success": true,
    "data": {
        "tutor_response": "Attention ! Il est important de ne pas sauter aux conclusions...",
        "session_id": "uuid-de-la-session",
        "etoiles_gagnees": 1,
        "score_total": 8,
        "cas_clinique": "Nouveau cas adapté",
        "niveau_actuel": "Niveau 1 - Bases du diagnostic"
    }
}
```

### Test 4: Consulter la Progression

**GET** `{{BASE_URL}}/api/tutor/progression/`

**Headers:**
```
Authorization: Token {{TOKEN}}
```

**Réponse Attendue:**
```json
{
    "success": true,
    "data": {
        "total_etoiles": 8,
        "sessions_completees": 0,
        "niveau_actuel": "Niveau 1 - Bases du diagnostic"
    }
}
```

### Test 5: Créer une Nouvelle Session

**POST** `{{BASE_URL}}/api/tutor/session/`

**Headers:**
```
Content-Type: application/json
Authorization: Token {{TOKEN}}
```

**Body (JSON):**
```json
{
    "niveau_id": "niveau_1"
}
```

**Réponse Attendue:**
```json
{
    "success": true,
    "message": "Prêt pour une nouvelle session"
}
```

### Test 6: Terminer une Session

**DELETE** `{{BASE_URL}}/api/tutor/session/uuid-de-la-session/`

**Headers:**
```
Authorization: Token {{TOKEN}}
```

**Réponse Attendue:**
```json
{
    "success": true,
    "message": "Session terminée avec succès"
}
```

## 🧪 **Scénarios de Test Avancés**

### Scénario 1: Consultation Médicale Complète

1. **Démarrer** une nouvelle session
2. **Saluer** le tuteur
3. **Présenter** les symptômes du patient
4. **Poser** des questions diagnostiques
5. **Proposer** un diagnostic
6. **Demander** des examens complémentaires
7. **Consulter** la progression
8. **Terminer** la session

### Scénario 2: Test de Détection d'Erreurs

Testez ces messages pour déclencher la détection d'erreurs :

```json
// Diagnostic prématuré
{"message": "C'est forcément un cancer"}

// Prescription sans diagnostic
{"message": "Je prescris des antibiotiques"}

// Minimisation des symptômes
{"message": "C'est juste du stress"}

// Jugement du patient
{"message": "Le patient ment sûrement"}
```

### Scénario 3: Test de Gamification

Envoyez plusieurs bonnes réponses pour accumuler des étoiles :

```json
{"message": "Je commence par examiner le patient"}
{"message": "Je prends ses constantes vitales"}
{"message": "J'écoute attentivement ses symptômes"}
{"message": "Je pose des questions précises"}
{"message": "Je formule des hypothèses diagnostiques"}
```

## 🔍 **Codes d'Erreur Possibles**

| Code | Message | Cause |
|------|---------|-------|
| 400 | Message requis | Body JSON manquant ou invalide |
| 401 | Unauthorized | Token manquant ou invalide |
| 404 | Session non trouvée | Session ID inexistant |
| 500 | Erreur serveur | Problème interne (voir logs) |

## 📊 **Collection Postman Prête à l'Emploi**

Voici une collection Postman complète :

```json
{
    "info": {
        "name": "Module Tuteur Intelligent",
        "description": "Tests complets du système tuteur médical"
    },
    "variable": [
        {
            "key": "BASE_URL",
            "value": "http://localhost:8000"
        },
        {
            "key": "TOKEN",
            "value": "votre-token-ici"
        }
    ],
    "item": [
        {
            "name": "1. Authentification",
            "request": {
                "method": "POST",
                "header": [
                    {
                        "key": "Content-Type",
                        "value": "application/json"
                    }
                ],
                "body": {
                    "mode": "raw",
                    "raw": "{\n    \"username\": \"votre_username\",\n    \"password\": \"votre_password\"\n}"
                },
                "url": {
                    "raw": "{{BASE_URL}}/api-token-auth/",
                    "host": ["{{BASE_URL}}"],
                    "path": ["api-token-auth", ""]
                }
            }
        },
        {
            "name": "2. Première Interaction",
            "request": {
                "method": "POST",
                "header": [
                    {
                        "key": "Content-Type",
                        "value": "application/json"
                    },
                    {
                        "key": "Authorization",
                        "value": "Token {{TOKEN}}"
                    }
                ],
                "body": {
                    "mode": "raw",
                    "raw": "{\n    \"message\": \"Bonjour, je commence ma formation\"\n}"
                },
                "url": {
                    "raw": "{{BASE_URL}}/api/tutor/chat/",
                    "host": ["{{BASE_URL}}"],
                    "path": ["api", "tutor", "chat", ""]
                }
            }
        },
        {
            "name": "3. Progression",
            "request": {
                "method": "GET",
                "header": [
                    {
                        "key": "Authorization",
                        "value": "Token {{TOKEN}}"
                    }
                ],
                "url": {
                    "raw": "{{BASE_URL}}/api/tutor/progression/",
                    "host": ["{{BASE_URL}}"],
                    "path": ["api", "tutor", "progression", ""]
                }
            }
        }
    ]
}
```

## 🚀 **Démarrage Rapide**

1. **Importez** cette collection dans Postman
2. **Configurez** les variables d'environnement
3. **Exécutez** "1. Authentification" pour obtenir le token
4. **Copiez** le token dans les variables
5. **Testez** les autres endpoints

## 🐛 **Dépannage**

### Problème: "Token invalide"
- Vérifiez que le token est correct
- Assurez-vous d'utiliser "Token " (avec espace) avant le token

### Problème: "Session non trouvée"
- Utilisez le session_id retourné par la première interaction
- Créez une nouvelle session si nécessaire

### Problème: "Erreur serveur 500"
- Vérifiez les logs Django
- Assurez-vous que la base de données est migrée
- Vérifiez que le service est démarré

## 📈 **Métriques à Surveiller**

- **Temps de réponse** : < 2 secondes
- **Étoiles gagnées** : 1-5 par interaction
- **Détection d'erreurs** : Fonctionnelle
- **Persistance des sessions** : Maintenue entre les appels