from django.db import models


class Product(models.Model):
    class Type(models.TextChoices):
        RANK = "RANK", "Привилегия"
        CURRENCY = "CURRENCY", "Донат-валюта"

    name = models.CharField(max_length=100, verbose_name="Название")
    slug = models.SlugField(unique=True, verbose_name="Ссылка")
    description = models.TextField(blank=True, verbose_name="Описание")
    product_type = models.CharField(
        max_length=20,
        choices=Type.choices,
        default=Type.RANK,
        verbose_name="Тип товара",
    )

    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=1,
        verbose_name="Цена, zł",
    )

    price_per_unit = models.DecimalField(
        max_digits=10,
        decimal_places=4,
        default=0.10,
        verbose_name="Цена за 1 монету, zł",
    )

    min_quantity = models.PositiveIntegerField(default=10, verbose_name="Минимум")
    max_quantity = models.PositiveIntegerField(default=10000, verbose_name="Максимум")

    image = models.ImageField(
        upload_to="products/",
        blank=True,
        null=True,
        verbose_name="Своя картинка",
    )

    image_url = models.CharField(
        max_length=255,
        blank=True,
        verbose_name="Путь к картинке",
    )

    badge = models.CharField(max_length=40, blank=True, verbose_name="Бейдж")
    accent = models.CharField(max_length=20, default="#ff3040", verbose_name="Цвет")
    commands = models.TextField(
        verbose_name="Команды выдачи",
        help_text="Одна команда на строку. {player} — ник, {quantity} — количество.",
    )

    active = models.BooleanField(default=True, verbose_name="Активен")
    featured = models.BooleanField(default=False, verbose_name="Популярный")
    sort_order = models.PositiveIntegerField(default=0, verbose_name="Сортировка")

    class Meta:
        ordering = ["sort_order", "price", "name"]
        verbose_name = "Товар"
        verbose_name_plural = "Товары"

    def __str__(self):
        return self.name

    @property
    def is_currency(self):
        return self.product_type == self.Type.CURRENCY

    @property
    def display_image(self):
        if self.image:
            return self.image.url
        return self.image_url or "/static/img/default.svg"

    def command_list(self, player, quantity=1):
        return [
            line.strip()
            .replace("{player}", player)
            .replace("{quantity}", str(quantity))
            for line in self.commands.splitlines()
            if line.strip()
        ]


class Order(models.Model):
    class Status(models.TextChoices):
        PENDING = "PENDING", "Ожидает оплаты"
        PAID = "PAID", "Оплачен"
        DELIVERED = "DELIVERED", "Выдан"
        FAILED = "FAILED", "Ошибка выдачи"
        CANCELED = "CANCELED", "Отменён"

    player = models.CharField(max_length=16, verbose_name="Игрок")
    product = models.ForeignKey(Product, on_delete=models.PROTECT, verbose_name="Товар")
    quantity = models.PositiveIntegerField(default=1, verbose_name="Количество")
    amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Сумма")
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.PENDING,
        verbose_name="Статус",
    )
    payment_id = models.CharField(max_length=120, blank=True, verbose_name="ID оплаты")
    rcon_log = models.TextField(blank=True, verbose_name="RCON лог")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Создан")
    paid_at = models.DateTimeField(null=True, blank=True, verbose_name="Оплачен")
    delivered_at = models.DateTimeField(null=True, blank=True, verbose_name="Выдан")

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"

    def __str__(self):
        return f"#{self.id} {self.player} — {self.product.name}"
