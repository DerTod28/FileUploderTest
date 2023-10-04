from typing import Any, Optional

from django.core.management.base import BaseCommand
from django.contrib.auth.models import User


class Command(BaseCommand):
    def handle(self, *args: Any, **options: Any) -> Optional[str]:
        if User.objects.filter(username='picasso').exists():
            return 'Admin "picasso" already exists'
        user = User.objects.create_user('picasso', password='picasso')
        user.is_superuser = True
        user.is_staff = True
        user.save()
        return 'Admin "picasso" created'
