from django.contrib import admin

# Register your models here.
from ai_services.models import Account


class AICustomerUsers(admin.ModelAdmin):
    list_display = ('id', 'password', 'is_superuser', 'username', 'first_name', 'last_name', 'email',
                    'is_staff', 'is_active', 'date_joined')
    list_filter = 'username',
    list_per_page = 10
    list_max_show_all = 200

    search_fields = ('username','email')


admin.site.site_header="AI Services"
admin.site.site_title = "AI Services"
admin.site.index_title = "AI Services"
#admin.site.site_url = 'http://127.0.0.1:8000/'


admin.site.register(Account, AICustomerUsers)

def has_superuser_permission(request):
    return request.user.is_active and request.user.is_superuser

# Only active superuser can access root admin site (default)
admin.site.has_permission = has_superuser_permission