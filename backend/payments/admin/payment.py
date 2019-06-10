from django.contrib import admin


class PaymentAdmin(admin.ModelAdmin):
    list_display = (
        'created', 'sender', 'receiver', 'amount')
    search_fields = [
        'created', 'sender__username', 'receiver__username', 'amount']
    ordering = ['created', 'sender__username', 'receiver__username', 'amount']

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return ['sender', 'receiver', 'amount']
        else:
            return []

    def has_delete_permission(self, request, obj=None):
        return False
