from julia import CMD_HELP, BOT_ID
import os
from julia import tbot
from pymongo import MongoClient
from julia import MONGO_DB_URI
from julia.events import register
from telethon import types
from telethon.tl import functions

client = MongoClient()
client = MongoClient(MONGO_DB_URI)
db = client["missjuliarobot"]
approved_users = db.approve


async def can_approve_users(message):
    result = await tbot(
        functions.channels.GetParticipantRequest(
            channel=message.chat_id,
            user_id=message.sender_id,
        )
    )
    p = result.participant
    return isinstance(p, types.ChannelParticipantCreator) or (
        isinstance(p, types.ChannelParticipantAdmin) and p.admin_rights.add_admins
    )


async def is_register_admin(chat, user):
    if isinstance(chat, (types.InputPeerChannel, types.InputChannel)):
        return isinstance(
            (
                await tbot(functions.channels.GetParticipantRequest(chat, user))
            ).participant,
            (types.ChannelParticipantAdmin, types.ChannelParticipantCreator),
        )
    if isinstance(chat, types.InputPeerUser):
        return True


# ------ THANKS TO LONAMI ------#


async def get_user_from_event(event):
    """ Get the user from argument or replied message. """
    if event.reply_to_msg_id:
        previous_message = await event.get_reply_message()
        user_obj = await tbot.get_entity(previous_message.sender_id)
    else:
        user = event.pattern_match.group(1)

        if user.isnumeric():
            user = int(user)

        if not user:
            await event.reply("Pass the user's username, id or reply!")
            return

        if event.message.entities is not None:
            probable_user_mention_entity = event.message.entities[0]

            if isinstance(probable_user_mention_entity, MessageEntityMentionName):
                user_id = probable_user_mention_entity.user_id
                user_obj = await tbot.get_entity(user_id)
                return user_obj
        try:
            user_obj = await tbot.get_entity(user)
        except (TypeError, ValueError) as err:
            await event.reply(str(err))
            return None

    return user_obj


@register(pattern="^/approve(?: |$)(.*)")
async def approve(event):
    if event.fwd_from:
        return
    if MONGO_DB_URI is None:
        return
    chat_id = event.chat.id
    sender = event.sender_id
    reply_msg = await event.get_reply_message()
    approved_userss = approved_users.find({})

    if event.is_group:
        if not await can_approve_users(message=event):
            return
    else:
        return

    userr = await get_user_from_event(event)
    if userr:
        pass
    else:
        return
    iid = userr.id

    if await is_register_admin(event.input_chat, iid):
        await event.reply("Why will I approve an admin ?")
        return

    if iid == event.sender_id:
        await event.reply("Why are you trying to approve yourself ?")
        print("6")
        return

    if event.sender_id == BOT_ID or int(iid) == int(BOT_ID):
        await event.reply("I am not gonna approve myself")
        print("7")
        return

    chats = approved_users.find({})
    for c in chats:
        if event.chat_id == c["id"] and iid == c["user"]:
            await event.reply("This User is Already Approved")
            return

    approved_users.insert_one({"id": event.chat_id, "user": iid})
    await event.reply("Successfully Approved User")


@register(pattern="^/disapprove(?: |$)(.*)")
async def disapprove(event):
    if event.fwd_from:
        return
    if MONGO_DB_URI is None:
        return
    chat_id = event.chat.id
    sender = event.sender_id
    reply_msg = await event.get_reply_message()
    approved_userss = approved_users.find({})

    if event.is_group:
        if not await can_approve_users(message=event):
            return
    else:
        return

    userr = await get_user_from_event(event)
    if userr:
        pass
    else:
        return
    iid = userr.id

    if await is_register_admin(event.input_chat, iid):
        await event.reply("Why will I disapprove an admin ?")
        return

    if iid == event.sender_id:
        await event.reply("Why are you trying to disapprove yourself ?")
        print("6")
        return

    if event.sender_id == BOT_ID or int(iid) == int(BOT_ID):
        await event.reply("I am not gonna disapprove myself")
        print("7")
        return

    chats = approved_users.find({})
    for c in chats:
        if event.chat_id == c["id"] and iid == c["user"]:
            approved_users.delete_one({"id": event.chat_id, "user": iid})
            await event.reply("Successfully Disapproved User")
            return
    await event.reply("This User isn't approved yet")


@register(pattern="^/checkstatus(?: |$)(.*)")
async def checkst(event):
    if event.fwd_from:
        return
    if MONGO_DB_URI is None:
        return
    chat_id = event.chat.id
    sender = event.sender_id
    reply_msg = await event.get_reply_message()
    approved_userss = approved_users.find({})

    if event.is_group:
        if not await can_approve_users(message=event):
            return
    else:
        return

    userr = await get_user_from_event(event)
    if userr:
        pass
    else:
        return
    iid = userr.id

    if await is_register_admin(event.input_chat, iid):
        await event.reply("Why will check status of an admin ?")
        return

    if event.sender_id == BOT_ID or int(iid) == int(BOT_ID):
        await event.reply("I am not gonna check my status")
        print("7")
        return

    chats = approved_users.find({})
    for c in chats:
        if event.chat_id == c["id"] and iid == c["user"]:
            await event.reply("This User is Approved")
            return
    await event.reply("This user isn't Approved")


@register(pattern="^/listapproved$")
async def apprlst(event):
    # print("😁")
    if event.fwd_from:
        return
    if MONGO_DB_URI is None:
        return
    chat_id = event.chat.id
    sender = event.sender_id
    reply_msg = await event.get_reply_message()

    if event.is_group:
        if not await can_approve_users(message=event):
            return
    else:
        return

    autos = approved_users.find({})
    pp = ""
    for i in autos:
        if event.chat_id == i["id"]:
            try:
                h = await tbot.get_entity(i["user"])
                getmyass = ""
                if not h.username:
                    getmyass += f"- [{h.first_name}](tg://user?id={h.id})\n"
                else:
                    getmyass += "- @" + h.username + "\n"
                pp += str(getmyass)
            except ValueError:
                pass
    try:
        await event.reply(pp)
    except Exception:
        await event.reply("No one is approved in this chat.")


@register(pattern="^/disapproveall$")
async def disapprlst(event):
    # print("😁")
    if event.fwd_from:
        return
    if MONGO_DB_URI is None:
        return
    chat_id = event.chat.id
    sender = event.sender_id
    reply_msg = await event.get_reply_message()

    if event.is_group:
        if not await can_approve_users(message=event):
            return
    else:
        return
    autos = approved_users.find({})
    for i in autos:
        if event.chat_id == i["id"]:
            approved_users.delete_one({"id": event.chat_id})
            await event.reply("Successfully disapproved everyone in the chat.")
            return
    await event.reply("No one is approved in this chat.")
