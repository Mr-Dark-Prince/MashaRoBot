from telethon.tl.types import MessageMediaPhoto
import os, urllib, requests, asyncio
from MashaRoBot import telethn as borg
MASHA = "quickstart-QUdJIGlzIGNvbWluZy4uLi4K"
@borg.on(pattern="/toonify")
async def _(event):
    
               
    reply = await event.get_reply_message()
    if not reply:#By @Danish_00
#Fixed By a NOOB
        return await event.edit(
           "Reply to any image or non animated sticker !"
        )
    devent = await event.edit("Downloading the file😅😁😁....")
    media = await event.client.download_media(reply)
    if not media.endswith(("png", "jpg", "webp")):
        return await event.edit(
             "Reply to any image or non animated sticker !"
        )#By @Danish_00
#Fixed By a NOOB
    devent = await event.edit("Toonifying image 🤪🤣🤓...")#hehehhehehhe
    r = requests.post(
        "https://api.deepai.org/api/toonify",
        files={
            "image": open(media, "rb"),
        },
        headers={"api-key": MASHA},
    )#By @Danish_00
#Fixed By a NOOB
    os.remove(media)
    if "status" in r.json():
        return await devent.edit( r.json()["status"])
    r_json = r.json()["output_url"]
    pic_id = r.json()["id"]
    
    link = f"https://api.deepai.org/job-view-file/{pic_id}/inputs/image.jpg"
    result = f"{r_json}"
    
    await devent.delete()
    await borg.send_message(#hehehhehehehehheh
        event.chat_id,
        file=result
    )
