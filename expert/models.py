from django.db import models
from mptt.models import MPTTModel, TreeForeignKey

class Skill(MPTTModel):
    """
    Représente une compétence dans un arbre d'apprentissage.
    Ex: "Python Basics" -> "Variables" -> "Data Types"
    """
    name = models.CharField(max_length=200, unique=True)
    description = models.TextField(blank=True, help_text="Description de ce que couvre la compétence.")
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')

    class MPTTMeta:
        order_insertion_by = ['name']

    def __str__(self):
        return self.name

class Concept(models.Model):
    """
    Représente une unité de connaissance atomique, l'élément le plus petit que l'on enseigne et évalue.
    Ex: Le concept de 'variable assignment', le concept de 'print() function'.
    """
    skill = models.ForeignKey(Skill, on_delete=models.CASCADE, related_name='concepts')
    name = models.CharField(max_length=255)
    explanation = models.TextField(help_text="L'explication fondamentale du concept qui sera utilisée par le LLM.")

    def __str__(self):
        return f"{self.name} (in {self.skill.name})"