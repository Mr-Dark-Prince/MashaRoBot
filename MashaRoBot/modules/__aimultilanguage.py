# credits @RoseLoverX @InukaASiTH
# ported to masha @Mr_dark_prince
from MashaRoBot import OWNER_ID, BOT_ID
from MashaRoBot import telethn as tbot
import MashaRoBot.modules.sql.aihelp_sql as sql
import MashaRoBot.modules.sql.chatbot_sql as ly
from google_trans_new import google_translator
translator = google_translator()
import requests


from telethon import events
from MashaRoBot.events import register

string = (
  "I belong To Mr_dark_prince!",
  "Im Fairly Yound And Was Made by mr_dark_prince!",
)


async def can_change_info(message):
    result = await tbot(
        functions.channels.GetParticipantRequest(
            channel=message.chat_id,
            user_id=message.sender_id,
        )
    )
    p = result.participant
    return isinstance(p, types.ChannelParticipantCreator) or (
        isinstance(p, types.ChannelParticipantAdmin) and p.admin_rights.change_info
    )


@register(pattern="^/yeschat$")
async def _(event):
    if event.is_group:
        if not event.sender_id == OWNER_ID:
           if not await can_change_info(message=event):
              return
    else:
        return
    chat = event.chat
    is_chat = sql.is_chat(chat.id)
    k = ly.is_chat(chat.id)
    if k:
        ly.rem_chat(chat.id)
    if not is_chat:
        ses_id = 'null'
        expires = 'null'
        sql.set_ses(chat.id, ses_id, expires)
        await event.reply("AI successfully enabled for this chat!")
        return
    await event.reply("AI Bot is already enabled for this chat!")
    return ""


@register(pattern="^/nochat$")
async def _(event):
    if event.is_group:
        if not event.sender_id == OWNER_ID:
          return
    else:
        return
    chat = event.chat
    is_chat = sql.is_chat(chat.id)
    if not is_chat:
        await event.reply("AI isn't enabled here in the first place!")
        return
    sql.rem_chat(chat.id)
    await event.reply("AI Bot disabled successfully!")


@tbot.on(events.NewMessage(pattern=None))
async def _(event):
  if event.is_group:
        pass
  else:
        return
  prof = str(event.text)
  
  if not "Masha" in prof:
    if not "masha" in prof:
      reply_msg = await event.get_reply_message()
      if not reply_msg.sender_id == BOT_ID:
           return
  chat = event.chat
  msg = prof
  is_chat = sql.is_chat(chat.id)
  if not is_chat:
        return
  if msg.startswith("/") or msg.startswith("@"):
    return
  lan = translator.detect(msg)
  if not "en" in lan and not lan == "":
     test = translator.translate(msg, lang_tgt="en")
  else:
     test = msg
  
  url = "https://iamai.p.rapidapi.com/ask"
  r = ('\n    \"consent\": true,\n    \"ip\": \"::1\",\n    \"question\": \"{}\"\n').format(test)
  k = f"({r})"
  new_string = k.replace("(", "{")
  lol = new_string.replace(")","}")
  payload = lol
  headers = {
    'content-type': "application/json",
    'x-forwarded-for': "<user's ip>",
    'x-rapidapi-key': "33b8b1a671msh1c579ad878d8881p173811jsn6e5d3337e4fc",
    'x-rapidapi-host': "iamai.p.rapidapi.com"
    }

  response = requests.request("POST", url, data=payload, headers=headers)
  lodu = response.json()
  result = (lodu['message']['text'])
  if "Thergiakis" in result:
   pro = random.choice(string)
   try:
      async with tbot.action(event.chat_id, 'typing'):
           await event.reply(pro)
   except CFError as e:
           print(e)
  elif "Ann" in result:
   pro = "Yeah, My name is Masha"
   try:
      async with tbot.action(event.chat_id, 'typing'):
           await event.reply(pro)
   except CFError as e:
           print(e)
  else:
    if not "en" in lan and not lan == "":
      finale = translator.translate(result, lang_tgt=lan[0])
    else:
      finale = result
    try:
      async with tbot.action(event.chat_id, 'typing'):
           await event.reply(finale)
    except CFError as e:
           await event.reply(lodu)
