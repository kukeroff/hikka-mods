# meta developer: @CEKPET_AHAHACA

import logging
from random import choice, randint
import requests
from .. import loader, utils
from telethon import errors
from time import time

__version__ = (1, 3, 3)


@loader.tds
class TonwalletBalanceModule(loader.Module):
    """Модуль для проверки баланса Tonkeeper/Tonhub (настраивается в конфиге)"""
    strings = {"name": "ca_tonwallet",
               "config_wallet": "Твой TON-адрес",
               "config_jettons_display": "Вкл/выкл отображение жетонов",
               "config_blocked_jettons": "Заблокированные жетоны",
               "config_only_verified_jettons_display": "Вкл/выкл отображение только верифицированных создателем мода жетонов",
               "config_currency": "Валюта, в которой отображать баланс (который в скобках). Примеры: USD, RUB, UAH, EUR, BTC, ETH, ... (все, что поддерживает cryptocompare.com)",
               "keyerror": (
                   "🗿 <b>Не указан кошелек / в конфиге проблема (вероятно, currency)</b>"
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
            ),
            loader.ConfigValue(
                "currency",
                'USD',
                lambda: self.strings("config_currency"),
                validator=loader.validators.String()
            )
        )

    def jetto(self, symb, balanc, jettonaddress, requestverified):
        TON = ''
        temp = ''
        for i in requestverified['jettons']:
            if i['jettonaddress'] == jettonaddress:
                temp += f'\n{i["emoji"]} {str(round(balanc, 4))} {str(i["symbol"])}'
        if temp == '':
            if self.config["only_verified_jettons_display"]:
                TON += ''
            else:
                TON += f'\n{requestverified["not_verified"]} {str(round(balanc, 4))} {str(symb)}'
        else:
            TON = temp
        return TON

    async def walletcmd(self, message):
        """(адрес кошелька) - показать баланс кошелька"""
        start = time()
        loading = choice(
            [
                '<emoji document_id=4965313018326942268>⬇</emoji>',
                '<emoji document_id=5334885140147479028>🫥</emoji>',
                '<emoji document_id=5334704798765686555>👀</emoji>',
                '<emoji document_id=5332739932832146628>☯</emoji>',
                '<emoji document_id=5328115567314346398>🫥</emoji>'
            ]
        )
        await message.edit(f'{loading} <b>Получаю данные</b>')
        adm = '' if randint(1, 6) > 1 else requests.get('https://raw.githubusercontent.com/kukeroff/text/main/adtext').json()['text']
        args = utils.get_args_raw(message)
        args_list = args.split(" ")
        twallet = args_list[0]
        if twallet == '':
            twallet = self.config["wallet"]
        wallet = twallet
        try:
            wallets = {
                'xjet': 'EQC2tC4THShN6jkWlfhYaIAF8pwjtSPbAW1oEaxFWR1SxJet',
                'xrocket': 'EQDB3GVLWYq4TNpPEjcu_tiQfO3wkBhlpYZJCHNz4BscJPaV'
            }
            await message.edit(f'{loading} <b>Получаю данные.</b>')
            if '.' in wallet:
                wallet = requests.get(f'https://tonapi.io/v2/dns/{wallet}/resolve').json()['wallet']['address']
            if wallet.lower() == 'xjet' or wallet.lower() == 'xrocket':
                wallet = wallets[wallet.lower()]
            url = f"https://tonapi.io/v2/blockchain/accounts/{wallet}"
            response = requests.get(url).json()
            wbalance = response["balance"]
            tontousd = requests.get(f"https://min-api.cryptocompare.com/data/price?fsym=TONCOIN&tsyms={self.config['currency']}").json()
            nano = 10**9
            tontocurrency = round(tontousd[self.config['currency']] * wbalance / nano, 4)
            diamond = '<emoji document_id=5471952986970267163>💎</emoji>'
            if wallet == 'EQC2tC4THShN6jkWlfhYaIAF8pwjtSPbAW1oEaxFWR1SxJet':
                TON = (
                    f"{diamond} <b>Баланс главного кошелька</b> @xJetSwapBot:\n"
                    f"{round(wbalance / nano, 3)} TON (≈ {tontocurrency} {self.config['currency']})\n"
                )
            elif wallet == 'EQDB3GVLWYq4TNpPEjcu_tiQfO3wkBhlpYZJCHNz4BscJPaV':
                TON = (
                    f"{diamond} <b>Баланс главного кошелька</b> @xRocket:\n"
                    f"{round(wbalance / nano, 3)} TON (≈ {tontocurrency} {self.config['currency']})\n"
                )
            else:
                if tontocurrency == 0:
                    TON = (
                        f"{diamond} <b>Баланс кошелька</b> <code>{twallet}</code>:\n"
                        f"{round(wbalance / nano, 3)} TON\n"
                    )
                else:
                    TON = (
                        f"{diamond} <b>Баланс кошелька</b> <code>{twallet}</code>:\n"
                        f"{round(wbalance / nano, 3)} TON (≈ {tontocurrency} {self.config['currency']})\n"
                    )
            await message.edit(f'{loading} <b>Получаю данные..</b>')
            displayjettons = self.config["display_jettons"]
            blockedjettons = self.config["blocked_jettons"]
            if displayjettons:
                req = requests.get(f'https://tonapi.io/v2/accounts/{wallet}/jettons').json()
                req = req['balances']
                requestverified = requests.get('https://raw.githubusercontent.com/kukeroff/text/main/vj').json()
                for i in req:
                    if i['balance'] != '0':
                        symb = i["jetton"]["symbol"]
                        decim = int(i['jetton']['decimals'])
                        jettonaddress = i['jetton']['address']
                        balanc = int(i['balance']) / 10 ** decim
                        TON += '' if symb in blockedjettons else self.jetto(symb, balanc, jettonaddress, requestverified)
            TON += adm
            await message.edit(TON, parse_mode='html')
            logging.info(f'Выполнена команда wallet, время выполнения: {round(time()-start, 3)} сек.')
        except KeyError:
            await utils.answer(message, self.strings["keyerror"])
        except errors.rpcerrorlist.MessageTooLongError:
            await utils.answer(
                message, (
                    'Слишком длинное значение у сообщения, '
                    'рекомендую выключить отображение жетонов '
                    '/ включить отображение только верифицированных жетонов'
                )
            )

