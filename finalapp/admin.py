from django.contrib import admin
from .models import hellman_encrypt,saved_keys,profile

admin.site.register(profile)
admin.site.register(hellman_encrypt)
admin.site.register(saved_keys)
