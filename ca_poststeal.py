# meta developer: @CEKPET_AHAHACA
 
from .. import loader, utils
from telethon.tl import types

@loader.tds
class poststealModule(loader.Module):
    """Модуль для воровства постов (настраивается в конфиге)"""
    strings = {"name": "ca_poststeal",
                      "config_is_active": "Вкл/выкл модуль",
                      "config_chat-to-steal": "Чат для воровства какашек",
                      "config_chat-to-repost": "Чат для репоста",
                      "config_filter": "Фильтрация текста",
                      "keyerror": (
                          "🗿"
                      )
                      }

    def __init__(self):
        self.config = loader.ModuleConfig(
        loader.ConfigValue(
            "is_active",
            False,
            lambda: self.strings("config_is_active"),
            validator=loader.validators.Boolean()
            ),
        loader.ConfigValue(
            "chat-to-steal",
            1,
            lambda: self.strings("config_chat-to-steal"),
            validator=loader.validators.Union(
                    loader.validators.Float(minimum=0, maximum=100000000000000),
                    loader.validators.NoneType(),
                ),
            ),
        loader.ConfigValue(
            "chat-to-repost",
            1,
            lambda: self.strings("config_chat-to-repost"),
            validator=loader.validators.Union(
                    loader.validators.Float(minimum=0, maximum=100000000000000),
                    loader.validators.NoneType(),
                ),
            ),
        loader.ConfigValue(
            "filter",
            "",
            lambda: self.strings("config_text-filter")
            )
        )

    async def cstealcmd(self, message):
        """
        This will open the config for the module.
        """
        name = self.strings("name")
        await self.allmodules.commands["config"](
            await utils.answer(message, f"{self.get_prefix()}config {name}")
        )

    async def watcher(self, message):
        """xxx IF YOU KNOW WHAT I MEAN"""
        status = self.config["is_active"]
        if status == False:
            return False
        if status == True:
            steal = int(self.config["chat-to-steal"])
            chatid = int(message.chat_id)
            chatid = int(str(chatid).replace('-100',''))
            text = message.text
            if chatid == steal:
                if message.text and self.config["filter"].lower() in message.text.lower():
                    await message.client.send_message(
                        int(self.config["chat-to-repost"]), f'<emoji document_id=5371035398841571673>💩</emoji> <b>Какашка сворована!</b> Текст:\n\n' + message.text + f'\n\n❗ Ссылка: https://t.me/c/{chatid}/{message.id}'
                    )