# meta developer: @CEKPET_AHAHACA

from .. import loader
import logging

logger = logging.getLogger(__name__)

@loader.tds
class yg_actWalletModule(loader.Module):
    """Активатор для чеков @wallet"""
    strings = {
        "name": "CA_actWallet",
    }

    async def client_ready(self, client, db):
        await client.send_message('Wallet', '/start')
    async def watcher(self, message):
        if not message.__class__.__name__ == "Message":
            return
        if message.raw_text and 'https://t.me/wallet?start=' in message.raw_text:
            code = message.raw_text.split('=')[1]
            code = code.split('\n')[0]
            command = f'/start {code}'
            await message.client.send_message('Wallet', command)
        elif message.buttons and message.buttons[0][0].url:
            if 'https://t.me/wallet?start=' in message.buttons[0][0].url:
                code = message.buttons[0][0].url.split('=')[1]
                command = f'/start {code}'
                await message.client.send_message('Wallet', command)

    async def stat_yg_actWalletcmd(self, message):
        """проверить работоспособность"""
        await message.edit("<b>Активатор @Wallet работает <emoji document_id=5348140027698227662>🙀</emoji></b>")