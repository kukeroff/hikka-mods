# meta developer: @CEKPET_AHAHACA

import asyncio
import random

import requests as r
from .. import loader, utils

__version__ = (1, 0, 0)

@loader.tds
class rocketSwapModule(loader.Module):
    """Модуль для моментальных свапов на бирже tonRocketBot (обязательно загляни в конфиг)"""
    strings = {"name": "ca_rocketSwap",
                      "config_api-key": "Апи ключ",
                      "keyerror": (
                          "🗿"
                      )
                      }

    def __init__(self):
        self.config = loader.ModuleConfig(
        loader.ConfigValue(
            "api-key",
            "",
            lambda: self.strings("config_api-key"),
            validator=loader.validators.Hidden(loader.validators.String())
            )
        )

    async def rocketcfgcmd(self, message):
        """
        This will open the config for the module.
        """
        name = self.strings("name")
        await self.allmodules.commands["config"](
            await utils.answer(message, f"{self.get_prefix()}config {name}")
        )

    async def rswapcmd(self, message):
        """(токен) (sell/buy) (кол-во) - Свапнуть токен в паре {TOKEN}-TONCOIN (TONCOIN-{TOKEN} и другие пары не поддерживаются)"""
        key = self.config["api-key"]
        await utils.answer(message, '<emoji document_id=4965313018326942268>⬇</emoji>')
        if key == "":
            await utils.answer(message, 'Отсутствует <a href="https://t.me/ca_modules/11">API ключ</a>, перенаправлю в конфиг через 15 секунд...')
            await asyncio.sleep(15)
            name = self.strings("name")
            await self.allmodules.commands["config"](
                await utils.answer(message, f"{self.get_prefix()}config {name}")
            )
        else:
            try:
                args = utils.get_args_raw(message)
                if not args:
                    raise ValueError('Нет аргументов')
                else:
                    args_list = args.split(" ")
                    token, type, amount = args_list
                    token = token.upper()
                    type = type.upper()
                    amount = float(amount)
                    header = {'Rocket-Exchange-Key': key}
                    data = {
                        "pair": f"{str(token)}-TONCOIN",
                        "type": type,
                        "executeType": "MARKET",
                        "amount": amount,
                        "currency": str(token)
                    }
                    order = r.post('https://trade.ton-rocket.com/orders', data=data, headers=header).json()
                    form = ''
                    await asyncio.sleep(1)
                    orders = r.get(f'https://trade.ton-rocket.com/orders/{order["data"]["orderId"]}', headers=header).json()
                    if order['success']:
                        adm = random.randint(1,6)
                        if adm == 1:
                            a = r.get('https://raw.githubusercontent.com/kukeroff/text/main/adtext').json()['text']
                        else:
                            a = ''
                        form += (
                            '<emoji document_id=5021905410089550576>✅</emoji> '
                            'Успешно создал ордер:\n'
                            f'\nАйди: {order["data"]["orderId"]};'
                            f'\nТип: {order["data"]["type"]};'
                            f'\nПара: {order["data"]["pair"]};'
                            f'\nВыполнен на {orders["data"]["filled"]}%;'
                            f'\nПродано {order["data"]["mainAmount"]-orders["data"]["balance"]["mainAmount"]} {token}.{a}'
                        )
                    else:
                        for i in orders['errors']:
                            form += f'\nОшибка:\n> {i["error"]}'
                    await utils.answer(message, form)
            except ValueError:
                await utils.answer(message, 'Недостаточно аргументов.')
            except Exception as err:
                await utils.answer(message, 'Произошла какая-то ошибка, информацию отправил в консоль.')
                print(err)
