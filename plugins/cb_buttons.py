import pyrogram

from plugins.mxplayer.py import mxplayer_execute


@pyrogram.Client.on_callback_query()
async def formatbuttons(bot, update):
       
    if "|" in update.data:
        await mxplayer_execute(bot, update)
        
    elif "closeformat" in update.data:     
        await update.message.delete()
    
