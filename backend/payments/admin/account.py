from django.contrib import admin


class AccountAdmin(admin.ModelAdmin):
    list_display = ('user', 'balance')
    search_fields = ['user__username', 'balance']
    ordering = ['user__username', 'balance']

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return ['user', 'balance']
        else:
            return []

    def has_add_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False
