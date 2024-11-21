from random import randint, choice
from faker import Faker
from django.core.management.base import BaseCommand
from django_seed import Seed
from feed.posts.models import Post


class Command(BaseCommand):
    help = '랜덤한 게시물 생성'
    
    def add_arguments(self, parser):
        parser.add_argument(
            "--total",
            default=2,
            type=int,
            help="몇개의 게시물을 만들지"
        )

    def handle(self, *args, **options):
        total = options.get("total")
        seeder = Seed.seeder()
        faker = Faker()
        choice_type = ['facebook', 'twitter', 'instagram', 'threads']

        seeder.add_entity(
            Post,
            total,
            {
                'title': lambda x: faker.sentence(),
                'type': lambda x: choice(choice_type),
                'content': lambda x: faker.sentence(),
                'view_count': lambda x: str(randint(1,100)),
                'like_count': lambda x: str(randint(1,100)),
                'share_count': lambda x: str(randint(1,100)),
                'created_at': lambda x: faker.date_time(),
                'updated_at': lambda x: faker.date_time(),
            }
        )
        seeder.execute()


    # content_id = models.CharField(max_length=50, unique=True)
    # type = models.CharField(max_length=50)
    # title = models.CharField(max_length=50)
    # content = models.TextField()
    # view_count = models.PositiveIntegerField(default=0)
    # like_count = models.PositiveIntegerField(default=0)
    # share_count = models.PositiveIntegerField(default=0)
    # created_at = models.DateTimeField(auto_now_add=True)
    # updated_at = models.DateTimeField(auto_now=True)
