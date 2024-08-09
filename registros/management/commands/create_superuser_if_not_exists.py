from django.core.management.base import BaseCommand
from registros.models import Usuario


class Command(BaseCommand):
    help = 'Cria um superusuário se não existir'

    def handle(self, *args, **options):
        if not Usuario.objects.filter(is_admin=True).exists():
            Usuario.objects.create_superuser(
                nome='Admin',
                email='admin@gmail.com',
                idade=7,
                password='a1234@'

            )
            self.stdout.write(self.style.SUCCESS('Superusuário criado com sucesso.'))
        else:
            self.stdout.write(self.style.SUCCESS('Já existe um superusuário.'))