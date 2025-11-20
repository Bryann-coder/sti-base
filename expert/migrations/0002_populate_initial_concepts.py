from django.db import migrations

def populate_skills_and_concepts(apps, schema_editor):
    """
    Crée l'arborescence initiale des compétences et les concepts associés.
    
    NOTE : Nous importons les modèles directement au lieu d'utiliser apps.get_model()
    car nous avons besoin du TreeManager de MPTT pour calculer correctement les champs
    de l'arbre (lft, rght, etc.) lors de la création des objets Skill.
    """
    from expert.models import Skill, Concept # <-- CHANGEMENT CRUCIAL ICI

    # Le reste du code est identique, mais il fonctionnera maintenant car nous utilisons
    # le vrai gestionnaire de modèles qui comprend MPTT.

    # --- NIVEAU 1 : Compétence Racine ---
    python_basics = Skill.objects.create(name='Python - Les Bases', description='Concepts fondamentaux du langage Python.')

    # --- NIVEAU 2 : Compétences Enfants ---
    variables_skill = Skill.objects.create(
        name='Variables et Types de Données',
        parent=python_basics,
        description='Apprendre à stocker et manipuler des informations.'
    )
    
    operators_skill = Skill.objects.create(
        name='Opérateurs',
        parent=python_basics,
        description='Effectuer des calculs et des comparaisons.'
    )

    # --- PEUPLEMENT DES CONCEPTS ---
    Concept.objects.create(
        skill=variables_skill,
        name='Assignation de variable',
        explanation="En Python, une variable est comme une boîte avec une étiquette. On utilise le signe égal (=) pour mettre quelque chose dans la boîte. Par exemple, 'x = 5' met le nombre 5 dans la boîte étiquetée 'x'."
    )
    # ... (les autres créations de Concept restent identiques)
    Concept.objects.create(
        skill=variables_skill,
        name='Le type Entier (integer)',
        explanation="Un entier est un nombre sans partie décimale, comme -2, 0, ou 10. En Python, on l'appelle 'int'. C'est le type de données de base pour les nombres entiers."
    )
    Concept.objects.create(
        skill=variables_skill,
        name='Le type Chaîne de caractères (string)',
        explanation="Une chaîne de caractères est une séquence de lettres, de chiffres ou de symboles. On la définit en utilisant des guillemets simples (' ') ou doubles (\" \"). Par exemple, 'nom = \"Alice\"'."
    )
    Concept.objects.create(
        skill=operators_skill,
        name='Opérateur d\'addition (+)',
        explanation="L'opérateur plus (+) est utilisé pour additionner deux nombres. Par exemple, '5 + 3' donne 8. Il peut aussi être utilisé pour concaténer (joindre) deux chaînes de caractères : '\"hello\" + \" world\"' donne '\"hello world\"'."
    )
    Concept.objects.create(
        skill=operators_skill,
        name='Opérateur de soustraction (-)',
        explanation="L'opérateur moins (-) est utilisé pour soustraire un nombre d'un autre. Par exemple, '10 - 4' donne 6."
    )


def remove_skills_and_concepts(apps, schema_editor):
    """
    Fonction inverse pour supprimer les données. Ici, apps.get_model est sûr.
    """
    Skill = apps.get_model('expert', 'Skill')
    Skill.objects.filter(name__in=[
        'Python - Les Bases',
        'Variables et Types de Données',
        'Opérateurs'
    ]).delete()

class Migration(migrations.Migration):

    dependencies = [
        ('expert', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(populate_skills_and_concepts, remove_skills_and_concepts),
    ]