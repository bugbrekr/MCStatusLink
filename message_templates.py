import toml

templates = toml.load("config/messageTemplates.toml")
class TelegramMessage:
    playerJoin = templates.get("playerJoin")
    playerLeave = templates.get("playerLeave")

    playerMessage = templates.get("playerMessage")
    playerAdvancement = templates.get("playerAdvancement")
    playerDeath = templates.get("playerDeath")
