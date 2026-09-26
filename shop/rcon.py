from django.conf import settings
from mcrcon import MCRcon


def execute_commands(commands):
    if not settings.RCON_PASSWORD:
        raise RuntimeError("RCON_PASSWORD пуст. Заполни файл .env")

    results = []
    with MCRcon(
        settings.RCON_HOST,
        settings.RCON_PASSWORD,
        port=settings.RCON_PORT
    ) as mcr:
        for command in commands:
            response = mcr.command(command)
            results.append(f"> {command}\n{response}")

    return results
