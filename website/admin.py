from django.contrib import admin
from reversion.helpers import patch_admin
from reversion_compare.helpers import patch_admin as compare_patch_admin

from models import Page, Element


def remove_from_admin(admin_class, fields):
    fieldsets = []

    for fieldset in admin_class.fieldsets:
        if fieldset[1]['fields'] in fields:
            pass
        else:
            fieldsets.append(fieldset)
    return tuple(fieldsets)


class ProtectedAdmin():

    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser


class ElementInline(ProtectedAdmin, admin.TabularInline):
    model = Element

    def get_actions(self, request):
        actions = super(ElementInline, self).get_actions(request)
        del actions['delete_selected']
        return actions


class PageAdmin(ProtectedAdmin, admin.ModelAdmin):
    inlines = [
        ElementInline
    ]
    fields = (
        "title",
        "url",
    )

    def get_actions(self, request):
        actions = super(PageAdmin, self).get_actions(request)
        del actions['delete_selected']
        return actions


class ElementAdmin(ProtectedAdmin, admin.ModelAdmin):

    def get_actions(self, request):
        actions = super(ElementAdmin, self).get_actions(request)
        del actions['delete_selected']
        return actions


admin.site.register(Page, PageAdmin)
admin.site.register(Element, ElementAdmin)

models_needing_patching = [
    Page,
    Element,
]

map(patch_admin, models_needing_patching)
map(compare_patch_admin, models_needing_patching)
