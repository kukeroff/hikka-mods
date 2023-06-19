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
        "inc_args": "<b>🐳 Incorrect args</b>",
        "keyerror": (
            "🗿 <b>Maybe the coin is not in the site database or you typed the wrong"
            " name.</b>"
        ),
        "okey": "<b>👯 Successfully. Current default value: {}</b>",
    }
    strings_ru = {
        "inc_args": "<b><emoji document_id=5348140027698227662>🙀</emoji> Неккоректные аргументы</b>",
        "keyerror": (
            "<b><emoji document_id=5348140027698227662>🙀</emoji> Возможно монеты нету в базе данных сайта, или вы ввели неккоректное"
            " название.</b>"
        ),
        "okey": "<b><emoji document_id=5348140027698227662>🙀</emoji> Успешно. Текущая стандартная валюта: {}</b>",
    }
 
    async def client_ready(self, client, db):
        self.db = db
        self.client = client
 
        if "defaultvalute" not in self.db:
            self.db.set("defaultvalute", "update", True)
 
    async def рмонетаcmd(self, message: Message):
        """<название> выбрать крипту по умолчанию"""
 
        args = utils.get_args_raw(message)
        self.db.set("defaultvalute", "val", args)
        await utils.answer(message, self.strings["okey"].format(args))
 
    async def рвклвыклcmd(self, message: Message):
        """Включить/выключить автообновление курса (каждые 5 мин)"""
        current_state = self.db.get("defaultvalute", "update", True)
        new_state = not current_state
        self.db.set("defaultvalute", "update", new_state)
 
        if new_state:
            await utils.answer(message, "<b>Автообновление курса: вкл</b>")
        else:
            await utils.answer(message, "<b>Автообновление курса: выкл</b>")
 
    async def ркурсcmd(self, message: Message):
        "<кол-во> <название монеты> смотреть курс"
        args = utils.get_args_raw(message)
        tray = self.db.get("defaultvalute", "val", args)
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
            smiles = r.choice(
                [
                    "<emoji document_id=5348140027698227662>🙀</emoji>",
                    "<emoji document_id=5348175255019988816>🙀</emoji>",
                    "<emoji document_id=5348179601526892213>🙀</emoji>",
                    "<emoji document_id=5348312457750260828>🙀</emoji>"
                ]
            )
 
            try:
                try:
                    count = float(args_list[0])
                    form = (
                        "{} <b>{} {} =</b> "
                        "<b>{}$</b>\n"
                    ).format(
                        smiles,
                        count,
                        coin,
                        round(api.get("USD", 0) * count, 6),
                        round(api.get("TONCOIN", 0) * count, 6),
                    )
 
                    update_state = self.db.get("defaultvalute", "update", True)
 
                    if update_state:
                        current_time = time.strftime("%H:%M:%S")
                        form += f"\n<i>Курс обновляется каждые 5 мин.</i>\n<b><i>Последнее Обновление:</i></b> <b>{current_time}</b>"
 
                    await utils.answer(message, form)
                except KeyError:
                    await utils.answer(message, self.strings["keyerror"])
            except ValueError:
                await utils.answer(message, self.strings["inc_args"])
 
            if not update_state:
                break
 
            await asyncio.sleep(300)