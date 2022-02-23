import asyncio
from time import time
from datetime import datetime
from modules.helpers.filters import command
from modules.helpers.command import commandpro
from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton


START_TIME = datetime.utcnow()
START_TIME_ISO = START_TIME.replace(microsecond=0).isoformat()
TIME_DURATION_UNITS = (
    ('week', 60 * 60 * 24 * 7),
    ('day', 60 * 60 * 24),
    ('hour', 60 * 60),
    ('min', 60),
    ('sec', 1)
)

async def _human_time_duration(seconds):
    if seconds == 0:
        return 'inf'
    parts = []
    for unit, div in TIME_DURATION_UNITS:
        amount, seconds = divmod(int(seconds), div)
        if amount > 0:
            parts.append('{} {}{}'
                         .format(amount, unit, "" if amount == 1 else "s"))
    return ', '.join(parts)
    
   

@Client.on_message(command("s") & filters.private & ~filters.edited)
async def start_(client: Client, message: Message):
    await message.reply_photo(
        photo=f"https://telegra.ph/file/69d6eac347596a636aa07.png",
        caption=f"""**━━━━━━━━━━━━━━━━━━━━━━━━
💥 ʜᴇʟʟᴏ, ɪ ᴀᴍ 𝙎𝙪𝙥𝙚𝙧𝙁𝙖𝙨𝙩 𝙑𝘾 𝙁𝙪𝙘𝙠𝙚𝙧 
ʙᴏᴛ ғᴏʀ ᴛᴇʟᴇɢʀᴀᴍ ɢʀᴏᴜᴘs ...
...
━━━━━━━━━━━━━━━━━━━━━━━━**""",
    reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "➕ ❰ repo ❱ ➕", url=f"https://github.com/guddu7866/VENOMxOPxMUSIC"),
                        InlineKeyboardButton("• 𝐂𝐎𝐍𝐓𝐀𝐂𝐓 𝐇𝐄𝐑𝐄", url=f"https://t.me/iam_your_heart4"),
                      InlineKeyboardButton("• 𝐂𝐎𝐍𝐓𝐀𝐂𝐓 𝐇𝐄𝐑𝐄", url=f"https://t.me/iam_your_heart4"),
                  ],[
                      InlineKeyboardButton("CREATER", url=f"https://t.me/iam_your_heart4")
                ]
                
           ]
        ),
    )
    
    
@Client.on_message(commandpro(["/s", "/alive", "Broken"]) & filters.group & ~filters.edited)
async def start(client: Client, message: Message):
    await message.reply_photo(
        photo=f"https://telegra.ph/file/69d6eac347596a636aa07.png",
        caption=f"""""",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "💥 𝐂𝐎𝐍𝐓𝐀𝐂𝐓 𝐇𝐄𝐑𝐄 💞", url=f"https://t.me/iam_your_heart4")
                ]
            ]
        ),
    )


@Client.on_message(commandpro(["re", "#re", "@re", "/re", "source"]) & filters.group & ~filters.edited)
async def help(client: Client, message: Message):
    await message.reply_photo(
        photo=f"https://telegra.ph/file/69d6eac347596a636aa07.png",
        caption=f"""""",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "💥 𝐂𝐎𝐍𝐓𝐀𝐂𝐓 𝐇𝐄𝐑𝐄 ᴛᴏ ɢᴇᴛ ʀᴇᴘᴏ 💞", url=f"https://github.com/guddu7866/VENOMxOPxMUSIC")
                ]
            ]
        ),
    )
