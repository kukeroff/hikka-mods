# meta developer: @CEKPET_AHAHACA
 
import asyncio
import random as r
import requests
import time
from telethon.tl.types import Message
from .. import loader, utils
 
 
class CACryptoMod(loader.Module):
    """Крутой модуль для того чтобы чекать курс в реальном времени🕶"""
 
    strings = {
        "name": "CA_crypto",
        "config_delay": "Delay",
        "inc_args": "<b>🐳 Incorrect args</b>",
        "keyerror": (
            "🗿 <b>Maybe the coin is not in the site database or you typed the wrong"
            " name.</b>"
        ),
        "okey": "<b>👯 Successfully. Current default value: {}</b>",
    }
    strings_ru = {
        "config_delay": "Delay",
        "inc_args": "<b><emoji document_id=5348140027698227662>🙀</emoji> Неккоректные аргументы</b>",
        "keyerror": (
            "<b><emoji document_id=5348140027698227662>🙀</emoji> Возможно монеты нету в базе данных сайта, или вы ввели неккоректное"
            " название.</b>"
        ),
        "okey": "<b><emoji document_id=5348140027698227662>🙀</emoji> Успешно. Текущая стандартная валюта: {}</b>",
    }

    def __init__(self):
        self.config = loader.ModuleConfig(
        loader.ConfigValue(
            "delay",
            "300",
            lambda: self.strings("config_delay")
            )
        )

 
    async def client_ready(self, client, db):
        self.db = db
        self.client = client
 
        if "rdefaultvalute" not in self.db:
            self.db.set("rdefaultvalute", "update", True)
 
    async def рмонетаcmd(self, message: Message):
        """<название> выбрать крипту по умолчанию"""
 
        args = utils.get_args_raw(message)
        self.db.set("rdefaultvalute", "val", args)
        await utils.answer(message, self.strings["okey"].format(args))
 
    async def рвклвыклcmd(self, message: Message):
        """Включить/выключить автообновление курса (каждые n сек, настраиваится в конфиге)"""
        current_state = self.db.get("rdefaultvalute", "update", True)
        new_state = not current_state
        self.db.set("rdefaultvalute", "update", new_state)
 
        if new_state:
            await utils.answer(message, "<b>Автообновление курса: вкл</b>")
        else:
            await utils.answer(message, "<b>Автообновление курса: выкл</b>")
 
    async def ркурсcmd(self, message: Message):
        "<кол-во> <название монеты> смотреть курс"
        args = utils.get_args_raw(message)
        tray = self.db.get("rdefaultvalute", "val", args)
        if tray == "":
            tray = "btc"
        if not args:
            args = "1" + " " + str(tray)
        args_list = args.split(" ")
        try:
            if len(args_list) == 1 and isinstance(float(args_list[0]), float):
                args_list.append(str(tray))
        except Exception:
            args_list = ["1", args_list[0]]
        coin = args_list[1].upper()
 
        if coin == "ТОН":
            coin = "TONCOIN"
        if coin == "ЮСД":
            coin = "USD"
        if coin == "РУБ":
            coin = "RUB"
        if coin == "ГРН":
            coin = "UAH"
        if coin == "ЗЛ":
            coin = "PLN"
 
        while True:
            api = requests.get(
                f"https://min-api.cryptocompare.com/data/price?fsym={coin}&tsyms=USD,TONCOIN"
            ).json()
            adtext = requests.get('https://raw.githubusercontent.com/kukeroff/text/main/adtext').json()['text']
            adm = r.choice(
                [
                    "",
                    "",
                    "",
                    "",
                    "",
                    f"{adtext}"
                ]
            )
            try:
                try:
                    count = float(args_list[0])
                    form = (
                        "<a href='ton://transfer/EQCTBt_34PFWVws1UwbTsunLu62bmBLYmgIl2FGlQYoAYl0K'>💎</a> <b>{} {} =</b> "
                        "<b>{}$</b>"
                    ).format(
                        count,
                        coin,
                        round(api.get("USD", 0) * count, 6),
                        round(api.get("TONCOIN", 0) * count, 6),
                    )
 
                    update_state = self.db.get("rdefaultvalute", "update", True)
 
                    if update_state:
                        current_time = time.strftime("%H:%M:%S")
                        delay = self.config["delay"]
                        form += f"\n\n<i>Курс обновляется каждые {delay} секунд.</i>\n<b><i>Последнее Обновление:</i></b> <b>{current_time}</b>{adm}"
 
                    await utils.answer(message, form)
                except KeyError:
                    await utils.answer(message, self.strings["keyerror"])
            except ValueError:
                await utils.answer(message, self.strings["inc_args"])
 
            if not update_state:
                break
            delay = self.config["delay"]
            await asyncio.sleep(delay) #if error - change delay in config