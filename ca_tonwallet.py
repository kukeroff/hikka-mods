# meta developer: @CEKPET_AHAHACA

import requests
from .. import loader, utils
from telethon.tl import types

@loader.tds
class TonwalletBalanceModule(loader.Module):
    """Модуль для проверки баланса Tonkeeper/Tonhub (настраивается в конфиге)"""
    strings = {"name": "ca_tonwallet",
                      "config_wallet": "Твой TON-адрес",
                      "keyerror": (
                          "🗿 <b>Ну ты кошелек то введи, моя твоя не понимать</b>"
                      )
                      }

    def __init__(self):
        self.config = loader.ModuleConfig(
        loader.ConfigValue(
            "wallet",
            "EQAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAM9c",
            lambda: self.strings("config_wallet")
            )
        )

    async def walletcmd(self, message):
        """(адрес кошелька) - показать баланс кошелька"""
        args = utils.get_args_raw(message)
        args_list = args.split(" ")
        twallet = args_list[0]
        if twallet != '':
            wallet = twallet
        else:
            wallet = self.config["wallet"]
        try:
            url = f"https://tonapi.io/v2/blockchain/accounts/{wallet}"
            response = requests.get(url).json()
            wbalance = response["balance"]
            TON = f"<emoji document_id=5471952986970267163>💎</emoji> <b>Баланс кошелька</b> <code>{wallet}</code>:\n{round(wbalance/1000000000, 4)} TON"
            await message.edit(TON)
        except KeyError:
            await utils.answer(message, self.strings["keyerror"])
        