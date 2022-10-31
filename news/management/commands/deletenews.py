from django.core.management.base import BaseCommand, CommandError
from ...models import Post, Category


class Command(BaseCommand):
    help = 'This command delete news from given category.'

    def add_arguments(self, parser):
        parser.add_argument('category', type=str)

    def handle(self, *args, **options):
        answer = input(f'Do you really want to delete all articles in a category {options["category"]}? yes/no')

        if answer != 'yes':
            self.stdout.write(self.style.ERROR('Cancelled'))

        try:
            category = Category.objects.get(name=options['category'])
            Post.objects.filter(categories__in=[category.id]).delete()
            self.stdout.write(self.style.SUCCESS(f'Succesfully deleted all news from category {category.name}'))
        except Category.DoesNotExist:
            self.stdout.write(self.style.ERROR(f'Could not find category {options["category"]}'))
