from django.contrib import admin
from mptt.admin import MPTTModelAdmin
from .models import Skill, Concept

class ConceptInline(admin.TabularInline):
    model = Concept
    extra = 1

class SkillAdmin(MPTTModelAdmin):
    list_display = ('name', 'parent')
    inlines = [ConceptInline]

admin.site.register(Skill, SkillAdmin)
admin.site.register(Concept) # On peut l'enregistrer aussi séparément si besoin