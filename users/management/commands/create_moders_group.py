from django.core.management import BaseCommand
from django.contrib.auth.models import Group
from django.contrib.auth.models import Permission


class Command(BaseCommand):

    def handle(self, *args, **options):
        moderators_group = Group.objects.create(name='Product moderators')

        delete_product_permission = Permission.objects.get(codename='delete_product')
        can_unpublish_product = Permission.objects.get(codename='can_unpublish_product')
        moderators_group.permissions.add(can_unpublish_product, delete_product_permission)
