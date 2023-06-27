# meta developer: @CEKPET_AHAHACA

from random import choice as rch
import requests
from .. import loader, utils
from telethon.tl import types
from telethon import errors

@loader.tds
class TonwalletBalanceModule(loader.Module):
    """Модуль для проверки баланса Tonkeeper/Tonhub (настраивается в конфиге)"""
    strings = {"name": "ca_tonwallet",
                      "config_wallet": "Твой TON-адрес",
                      "config_jettons_display": "Вкл/выкл отображение жетонов",
                      "config_blocked_jettons": "Заблокированные жетоны",
                      "config_only_verified_jettons_display": "Вкл/выкл отображение только верифицированных создателем мода жетонов",
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
            ),
        loader.ConfigValue(
            "only_verified_jettons_display",
            False,
            lambda: self.strings("config_only_verified_jettons_display"),
            validator=loader.validators.Boolean()
            )
        )
    def jetto(self, symb, balanc, jettonaddress, requestverified):
        TON = ''
        temp = ''
        for i in requestverified:
            if i['jettonaddress'] == jettonaddress:
                temp += f'\n{i["emoji"]} {str(round(balanc, 4))} {str(symb)}'
        if temp == '':
            if self.config["only_verified_jettons_display"]:
                TON += ''
            else:
                TON += f'\n{str(round(balanc, 4))} {str(symb)}'
        else:
            TON = temp
        return(TON)
    async def walletcmd(self, message):
        """(адрес кошелька) - показать баланс кошелька"""
        adtext = requests.get('https://raw.githubusercontent.com/kukeroff/text/main/adtext').json()['text']
        adm = rch(
            [
                "",
                "",
                "",
                "",
                "",
                f"{adtext}"
            ]
        )
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
            if wallet == 'EQC2tC4THShN6jkWlfhYaIAF8pwjtSPbAW1oEaxFWR1SxJet':
                TON = f"<emoji document_id=5471952986970267163>💎</emoji> <b>Баланс главного кошелька</b> @xJetSwapBot:\n{round(wbalance/1000000000, 4)} TON (≈ {usdton}$)\n"
            else:
                TON = f"<emoji document_id=5471952986970267163>💎</emoji> <b>Баланс кошелька</b> <code>{wallet}</code>:\n{round(wbalance / 1000000000, 4)} TON (≈ {usdton}$)\n"
            displayjettons = self.config["display_jettons"]
            blockedjettons = self.config["blocked_jettons"]
            if displayjettons == True:
                req = requests.get(f'https://tonapi.io/v2/accounts/{wallet}/jettons').json()
                req = req['balances']
                requestverified = requests.get('https://raw.githubusercontent.com/kukeroff/text/main/vj').json()['jettons']
                for i in req:
                    if i['balance'] != '0':
                        symb = i["jetton"]["symbol"]
                        decim = int(i['jetton']['decimals'])
                        jettonaddress = i['jetton']['address']
                        balanc = int(i['balance'])
                        if decim >= 1:
                            for i in range(decim):
                                balanc /= 10
                        if symb in blockedjettons:
                            TON += ''
                        else:

                            TON += self.jetto(symb, balanc, jettonaddress, requestverified)
            TON += adm
            await message.edit(TON)
        except KeyError:
            await utils.answer(message, self.strings["keyerror"])
        except errors.rpcerrorlist.MessageTooLongError:
            await utils.answer(message, 'Слишком длинное значение у сообщения, рекомендую выключить отображение жетонов / включить отображение только верифицированных жетонов')