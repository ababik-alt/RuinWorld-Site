# RuinWorld Shop V5 — RuinPay

Красивый checkout RuinPay с выбором BLIK / Карта / Перевод.

Важно: эта версия не подключена к банку или PayU и не собирает реальные платёжные реквизиты.
После подтверждения заказа запускается RCON-выдача товара.

## Установка

```powershell
cd C:\Users\Zachmyrik\Downloads\ruinworld_shop_v5_ruinpay
python -m pip install -r requirements.txt
python manage.py migrate
python manage.py seed_demo
python manage.py runserver
```

Открыть:
http://127.0.0.1:8000

Админка:
http://127.0.0.1:8000/admin/

## RCON

В `.env`:

```env
RCON_HOST=127.0.0.1
RCON_PORT=25575
RCON_PASSWORD=ТВОЙ_ПАРОЛЬ
```

В Minecraft `server.properties`:

```properties
enable-rcon=true
rcon.port=25575
rcon.password=ТВОЙ_ПАРОЛЬ
```

После изменения server.properties полностью перезапусти сервер.

## RuinPay

Поток:
магазин -> checkout -> RuinPay -> обработка -> RCON -> готово

Страница RuinPay не просит номер карты, CVV, пароль банка или настоящий BLIK-код.
