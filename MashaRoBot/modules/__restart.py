import os
import sys
from MashaRoBot.helper_extra.heroku_helpo import HerokuHelper
import heroku3
import requests
from MashaRoBot.events import register
from MashaRoBot import HEROKU_API_KEY, HEROKU_APP_NAME, OWNER_ID
Heroku = heroku3.from_key(HEROKU_API_KEY)

@register(pattern="^/restart$")
async def _(event):
    if event.fwd_from:
        return
    if event.sender_id == OWNER_ID:
        pass
    else:
        return
    await event.edit("**Masha Restarted🤷**")
    try:
        herokuHelper = HerokuHelper(HEROKU_APP_NAME, HEROKU_API_KEY)
        herokuHelper.restart()
    except:
        await borg.disconnect()
        os.execl(sys.executable, sys.executable, *sys.argv)
