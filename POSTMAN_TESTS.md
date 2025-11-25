# 🧪 TESTS POSTMAN - SYSTÈME TUTEUR MÉDICAL

## 📋 Configuration de base

**Base URL:** `http://localhost:8000`

## 🔐 1. INSCRIPTION UTILISATEUR

**Endpoint:** `POST /api/user/register/`

**Headers:**
```
Content-Type: application/json
```

**Body (JSON):**
```json
{
    "username": "medecin_test",
    "email": "medecin@test.com",
    "first_name": "Dr. Jean",
    "last_name": "Dupont",
    "password": "motdepasse123",
    "specialite": "Médecine Générale",
    "niveau_expertise": "DEBUTANT"
}
```

**Réponse attendue:**
```json
{
    "success": true,
    "message": "Utilisateur créé avec succès",
    "user_id": 1,
    "username": "medecin_test",
    "token": "9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b"
}
```

---

## 🔑 2. CONNEXION UTILISATEUR

**Endpoint:** `POST /api/user/login/`

**Headers:**
```
Content-Type: application/json
```

**Body (JSON):**
```json
{
    "username": "medecin_test",
    "password": "motdepasse123"
}
```

**Réponse attendue:**
```json
{
    "success": true,
    "message": "Connexion réussie",
    "user_id": 1,
    "username": "medecin_test",
    "token": "9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b",
    "profile": {
        "specialite": "Médecine Générale",
        "niveau_expertise": "DEBUTANT",
        "domaine": "Santé"
    }
}
```

---

## 👤 3. PROFIL UTILISATEUR

**Endpoint:** `GET /api/user/profile/`

**Headers:**
```
Content-Type: application/json
Authorization: Token 9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b
```

**Réponse attendue:**
```json
{
    "success": true,
    "profile": {
        "username": "medecin_test",
        "email": "medecin@test.com",
        "first_name": "Dr. Jean",
        "last_name": "Dupont",
        "specialite": "Médecine Générale",
        "niveau_expertise": "DEBUTANT",
        "domaine": "Santé",
        "date_creation": "2024-11-24T10:30:00Z"
    }
}
```

---

## 🏥 4. DÉMARRER UNE CONSULTATION

**Endpoint:** `POST /api/tutor/chat/`

**Headers:**
```
Content-Type: application/json
Authorization: Token 9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b
```

**Body (JSON):**
```json
{
    "message": "Bonjour, comment vous sentez-vous aujourd'hui ?"
}
```

**Réponse attendue:**
```json
{
    "success": true,
    "data": {
        "tutor_response": "Bonjour Docteur. Je ne me sens pas très bien aujourd'hui. J'ai surtout l'impression d'être très fatigué et j'ai mal à la tête...",
        "session_id": "session_123456",
        "etoiles_gagnees": 3,
        "score_total": 3,
        "cas_clinique": "Patient avec symptômes généraux",
        "niveau_actuel": "Consultations de base",
        "fin_consultation": false
    }
}
```

---

## 💬 5. CONTINUER LA CONSULTATION

**Endpoint:** `POST /api/tutor/chat/`

**Headers:**
```
Content-Type: application/json
Authorization: Token 9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b
```

**Body (JSON):**
```json
{
    "message": "Depuis quand avez-vous ces symptômes ?",
    "session_id": "session_123456"
}
```

**Réponse attendue:**
```json
{
    "success": true,
    "data": {
        "tutor_response": "Cela a commencé il y a environ deux jours. J'ai pensé que c'était juste une mauvaise nuit de sommeil...",
        "session_id": "session_123456",
        "etoiles_gagnees": 4,
        "score_total": 7,
        "cas_clinique": "Patient avec symptômes généraux",
        "niveau_actuel": "Consultations de base",
        "fin_consultation": false
    }
}
```

---

## 🩺 6. POSER UNE QUESTION MÉDICALE

**Endpoint:** `POST /api/tutor/chat/`

**Headers:**
```
Content-Type: application/json
Authorization: Token 9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b
```

**Body (JSON):**
```json
{
    "message": "Avez-vous de la fièvre ?",
    "session_id": "session_123456"
}
```

**Réponse attendue:**
```json
{
    "success": true,
    "data": {
        "tutor_response": "Oui, j'ai l'impression d'avoir un peu chaud, mais je n'ai pas pris ma température...",
        "session_id": "session_123456",
        "etoiles_gagnees": 4,
        "score_total": 11,
        "cas_clinique": "Patient avec symptômes généraux",
        "niveau_actuel": "Consultations de base",
        "fin_consultation": false
    }
}
```

---

## ❌ 7. TEST ERREUR MÉDICALE

**Endpoint:** `POST /api/tutor/chat/`

**Headers:**
```
Content-Type: application/json
Authorization: Token 9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b
```

**Body (JSON):**
```json
{
    "message": "C'est sûrement un cancer !",
    "session_id": "session_123456"
}
```

**Réponse attendue:**
```json
{
    "success": true,
    "data": {
        "tutor_response": "Non, je ne pense pas que ce soit un cancer ! C'est une conclusion beaucoup trop hâtive... (Petit conseil : En tant que futur médecin, il est crucial d'éviter de sauter trop vite à des conclusions alarmantes...)",
        "session_id": "session_123456",
        "etoiles_gagnees": 1,
        "score_total": 12,
        "cas_clinique": "Patient avec symptômes généraux",
        "niveau_actuel": "Consultations de base",
        "fin_consultation": false
    }
}
```

---

## 🏁 8. TERMINER LA CONSULTATION

**Endpoint:** `POST /api/tutor/chat/`

**Headers:**
```
Content-Type: application/json
Authorization: Token 9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b
```

**Body (JSON):**
```json
{
    "message": "Je pense que vous avez une grippe saisonnière",
    "session_id": "session_123456"
}
```

**Réponse attendue:**
```json
{
    "success": true,
    "data": {
        "tutor_response": "C'est une hypothèse raisonnable compte tenu de mes symptômes...",
        "session_id": "session_123456",
        "etoiles_gagnees": 4,
        "score_total": 16,
        "cas_clinique": "Patient avec symptômes généraux",
        "niveau_actuel": "Consultations de base",
        "fin_consultation": true,
        "diagnostic_correct": true,
        "feedback_pedagogique": "Bonne démarche diagnostique. Vous avez bien exploré les symptômes..."
    }
}
```

---

## 📊 9. PROGRESSION UTILISATEUR

**Endpoint:** `GET /api/tutor/progression/`

**Headers:**
```
Content-Type: application/json
Authorization: Token 9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b
```

**Réponse attendue:**
```json
{
    "success": true,
    "data": {
        "total_etoiles": 16,
        "sessions_completees": 1,
        "niveau_actuel": "Consultations de base"
    }
}
```

---

## 🚪 10. DÉCONNEXION

**Endpoint:** `POST /api/user/logout/`

**Headers:**
```
Content-Type: application/json
Authorization: Token 9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b
```

**Réponse attendue:**
```json
{
    "success": true,
    "message": "Déconnexion réussie"
}
```

---

## 🔧 DÉMARRAGE DU SERVEUR

Avant de tester, démarrez le serveur Django :

```bash
cd /home/folongzidane/Documents/Projet/stiProjet/sti-base
.venv/bin/python manage.py runserver
```

Le serveur sera accessible sur `http://localhost:8000`

---

## 📝 NOTES IMPORTANTES

1. **Token d'authentification** : Récupérez le token lors de l'inscription/connexion et utilisez-le dans tous les appels authentifiés
2. **Session ID** : Conservez le session_id retourné pour continuer la même consultation
3. **Gestion d'erreurs** : Le système détecte automatiquement les erreurs médicales et adapte les réponses
4. **Fin de consultation** : Détectée automatiquement par des mots-clés ou un diagnostic final

---

## 🎯 SÉQUENCE DE TEST RECOMMANDÉE

1. Inscription → Récupérer le token
2. Connexion → Vérifier le profil
3. Démarrer consultation → Récupérer session_id
4. Poser 3-4 questions médicales
5. Tester une erreur médicale
6. Terminer avec un diagnostic
7. Vérifier la progression
8. Déconnexion