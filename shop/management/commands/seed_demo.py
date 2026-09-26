from django.core.management.base import BaseCommand
from shop.models import Product


RANKS = [
    ('TIGER', 'tiger', 3, '#ff9f1c', 'START', 'lp user {player} parent set tiger'),
    ('BUNNY', 'bunny', 5, '#ff5da2', 'POPULAR', 'lp user {player} parent set bunny'),
    ('RABBIT', 'rabbit', 6, '#a56cff', '', 'lp user {player} parent set rabbit'),
    ('HYDRA', 'hydra', 10, '#35e07a', 'HOT', 'lp user {player} parent set hydra'),
    ('COBRA', 'cobra', 13, '#25d5fd', '', 'lp user {player} parent set cobra'),
    ('GOD', 'god', 17, '#ffd166', 'TOP', 'lp user {player} parent set god'),
    ('PEGAS', 'pegas', 20, '#7aa2ff', 'VIP', 'lp user {player} parent set pegas'),
    ('D.HELPER', 'd-helper', 25, '#ff3d71', 'ULTRA', 'lp user {player} parent set d.helper'),
    ('BULL', 'bull', 30, '#ff6b35', 'NEW', 'lp user {player} parent set bull'),
    ('DRACULA', 'dracula', 35, '#b11226', 'DARK', 'lp user {player} parent set dracula'),
    ('GLMODER', 'glmoder', 40, '#00c2ff', 'STAFF', 'lp user {player} parent set glmoder'),
    ('HELPER', 'helper', 45, '#57d68d', 'STAFF', 'lp user {player} parent set helper'),
    ('MODER', 'moder', 50, '#4c8dff', 'STAFF', 'lp user {player} parent set moder'),
    ('IMPERATOR', 'imperator', 60, '#ffb000', 'ELITE', 'lp user {player} parent set imperator'),
    ('MAGISTER', 'magister', 70, '#a56cff', 'ELITE', 'lp user {player} parent set magister'),
    ('MEDIA', 'media', 80, '#ff4da6', 'MEDIA', 'lp user {player} parent set media'),
    ('MLADMIN', 'mladmin', 90, '#ff2e63', 'STAFF', 'lp user {player} parent set mladmin'),
    ('MLMODER', 'mlmoder', 85, '#6a7cff', 'STAFF', 'lp user {player} parent set mlmoder'),
    ('OFFHELPER', 'offhelper', 25, '#7bd389', 'STAFF', 'lp user {player} parent set offhelper'),
    ('OFFMLMODER', 'offmlmoder', 55, '#7f8cff', 'STAFF', 'lp user {player} parent set offmlmoder'),
    ('STMODER', 'stmoder', 65, '#3a86ff', 'STAFF', 'lp user {player} parent set stmoder'),
    ('VAMPIRE', 'vampire', 75, '#8b0000', 'DARK', 'lp user {player} parent set vampire'),
]


class Command(BaseCommand):
    help = "Создаёт демо товары RuinWorld"

    def handle(self, *args, **kwargs):
        for idx, (name, slug, price, accent, badge, command) in enumerate(RANKS, start=1):
            Product.objects.update_or_create(
                slug=slug,
                defaults={
                    "name": name,
                    "description": f"Привилегия {name} для сервера RuinWorld.",
                    "product_type": Product.Type.RANK,
                    "price": price,
                    "badge": badge,
                    "accent": accent,
                    "image_url": f"/static/img/{slug}.svg",
                    "commands": command,
                    "active": True,
                    "featured": name in {"HYDRA", "GOD", "PEGAS", "DRACULA", "IMPERATOR", "VAMPIRE"},
                    "sort_order": idx,
                },
            )

        Product.objects.update_or_create(
            slug="donate-coins",
            defaults={
                "name": "DONATE COINS",
                "description": "Выбери любое количество донат-монет. Цена считается автоматически.",
                "product_type": Product.Type.CURRENCY,
                "price": 1,
                "price_per_unit": "0.10",
                "min_quantity": 10,
                "max_quantity": 10000,
                "badge": "CUSTOM",
                "accent": "#ffb703",
                "image_url": "/static/img/coins.svg",
                "commands": "points give {player} {quantity}",
                "active": True,
                "featured": True,
                "sort_order": 0,
            },
        )

        self.stdout.write(self.style.SUCCESS("Товары RuinWorld созданы/обновлены."))