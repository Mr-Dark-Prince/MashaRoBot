from pyrogram import filters

from EvaMariaRobot import BOT_ID, SUDOERS, USERBOT_PREFIX, app2


@app2.on_message(
    filters.command("alive", prefixes=USERBOT_PREFIX) & filters.user(SUDOERS)
)
async def alive_command_func(_, message):
    await message.delete()
    results = await app2.get_inline_bot_results(BOT_ID, "alive")
    await app2.send_inline_bot_result(
        message.chat.id, results.query_id, results.results[0].id
    )
