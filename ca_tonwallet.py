# meta developer: @CEKPET_AHAHACA

import requests
from .. import loader, utils
from telethon.tl import types

@loader.tds
class TonwalletBalanceModule(loader.Module):
    """Модуль для проверки баланса Tonkeeper/Tonhub (настраивается в конфиге)"""
    strings = {"name": "ca_tonwallet",
                      "config_wallet": "Твой TON-адрес",
                      "config_jettons_display": "Вкл/выкл отображение жетонов",
                      "config_blocked_jettons": "Заблокирова",
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
            ),
        loader.ConfigValue(
            "display_jettons",
            True,
            lambda: self.strings("config_jettons_display"),
            validator=loader.validators.Boolean()
            ),
        loader.ConfigValue(
            "blocked_jettons",
            [],
            lambda: self.strings("config_blocked_jettons"),
            validator=loader.validators.Series()
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
            tontousd = requests.get(
                f"https://min-api.cryptocompare.com/data/price?fsym=TONCOIN&tsyms=USD,TONCOIN"
            ).json()
            usdton = round(tontousd.get("USD", 0) * wbalance/1000000000, 6)
            TON = f"<emoji document_id=5471952986970267163>💎</emoji> <b>Баланс кошелька</b> <code>{wallet}</code>:\n{round(wbalance/1000000000, 4)} TON (≈ {usdton}$)\n"
            displayjettons = self.config["display_jettons"]
            blockedjettons = self.config["blocked_jettons"]
            if displayjettons == True:
                req = requests.get(f'https://tonapi.io/v2/accounts/{wallet}/jettons').json()
                req = req['balances']
                for i in req:
                    if i['balance'] != '0':
                        symb = i["jetton"]["symbol"]
                        decim = int(i['jetton']['decimals'])
                        balanc = int(i['balance'])
                        if decim >= 1:
                            for i in range(decim):
                                balanc /= 10
                        if symb in blockedjettons:
                            TON += ''
                        else:
                            if 'AMBR' in symb:
                                TON += f'\n<emoji document_id=5235960141966224938>🐳</emoji> {str(round(balanc, 4))} {str(symb)}'
                            elif 'SCALE' in symb:
                                TON += f'\n<emoji document_id=5237843240312384621>⛰</emoji> {str(round(balanc, 4))} {str(symb)}'
                            elif 'HEDGE' in symb:
                                TON += f'\n<emoji document_id=5235588734669303271>🦔</emoji> {str(round(balanc, 4))} {str(symb)}'
                            elif 'TAKE' in symb:
                                TON += f'\n<emoji document_id=5235599476382509889>🥰</emoji> {str(round(balanc, 4))} {str(symb)}'
                            elif 'GAIKA' in symb:
                                TON += f'\n<emoji document_id=5235564880420943862>🔩</emoji> {str(round(balanc, 4))} {str(symb)}'
                            elif 'BOLT' in symb:
                                TON += f'\n<emoji document_id=5235653472711356734>🔩</emoji> {str(round(balanc, 4))} {str(symb)}'
                            elif 'KINGY' in symb:
                                TON += f'\n<emoji document_id=5238094229611228465>🦘</emoji> {str(round(balanc, 4))} {str(symb)}'
                            elif 'MCT' in symb:
                                TON += f'\n<emoji document_id=5235715182801463938>😺</emoji> {str(round(balanc, 4))} {str(symb)}'
                            elif 'SLR' in symb:
                                TON += f'\n<emoji document_id=5235984597510008502>😊</emoji> {str(round(balanc, 4))} {str(symb)}'
                            elif 'KISS' in symb:
                                TON += f'\n<emoji document_id=5237704508573757171>💋</emoji> {str(round(balanc, 4))} {str(symb)}'
                            elif 'PET' in symb:
                                TON += f'\n<emoji document_id=5238225505286631097>🙂</emoji> {str(round(balanc, 4))} {str(symb)}'
                            elif 'X' == symb:
                                TON += f'\n<emoji document_id=5237951129890859295>❌</emoji> {str(round(balanc, 4))} {str(symb)}'
                            elif '+' == symb:
                                TON += f'\n<emoji document_id=5235837602254302764>➕</emoji> {str(round(balanc, 4))} {str(symb)}'
                            else:
                                TON += f'\n{str(round(balanc, 4))} {str(symb)}'
            await message.edit(TON)
        except KeyError:
            await utils.answer(message, self.strings["keyerror"])
        