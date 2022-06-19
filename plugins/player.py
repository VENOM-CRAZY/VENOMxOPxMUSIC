# VENOMxCRAZY // @No_One_Is_mine

import os
import aiofiles
import aiohttp
import ffmpeg
import requests
from os import path
from asyncio.queues import QueueEmpty
from typing import Callable
from pyrogram import Client, filters
from pyrogram.types import Message, Voice, InlineKeyboardButton, InlineKeyboardMarkup
from pyrogram.errors import UserAlreadyParticipant
from modules.cache.admins import set
from modules.clientbot import clientbot, queues
from modules.clientbot.clientbot import client as USER
from modules.helpers.admins import get_administrators
from youtube_search import YoutubeSearch
from modules import converter
from modules.downloaders import youtube
from modules.config import DURATION_LIMIT, que, SUDO_USERS, OWNER_USERNAME, SUPPORT_GROUP, SUPPORT_CHANNEL
from modules.cache.admins import admins as a
from modules.helpers.filters import command, other_filters
from modules.helpers.command import commandpro
from modules.helpers.decorators import errors, authorized_users_only
from modules.helpers.errors import DurationLimitError
from modules.helpers.gets import get_url, get_file_name
from PIL import Image, ImageFont, ImageDraw
from pytgcalls import StreamType
from pytgcalls.types.input_stream import InputStream
from pytgcalls.types.input_stream import InputAudioStream

# plus
chat_id = None
useer = "NaN"


def transcode(filename):
    ffmpeg.input(filename).output(
        "input.raw", format="s16le", acodec="pcm_s16le", ac=2, ar="48k"
    ).overwrite_output().run()
    os.remove(filename)


# Convert seconds to mm:ss
def convert_seconds(seconds):
    seconds = seconds % (24 * 3600)
    seconds %= 3600
    minutes = seconds // 60
    seconds %= 60
    return "%02d:%02d" % (minutes, seconds)


# Convert hh:mm:ss to seconds
def time_to_seconds(time):
    stringt = str(time)
    return sum(int(x) * 60 ** i for i, x in enumerate(reversed(stringt.split(":"))))


# Change image size
def changeImageSize(maxWidth, maxHeight, image):
    widthRatio = maxWidth / image.size[0]
    heightRatio = maxHeight / image.size[1]
    newWidth = int(widthRatio * image.size[0])
    newHeight = int(heightRatio * image.size[1])
    return image.resize((newWidth, newHeight))


async def generate_cover(requested_by, title, views, duration, thumbnail):
    async with aiohttp.ClientSession() as session:
        async with session.get(thumbnail) as resp:
            if resp.status == 200:
                f = await aiofiles.open("background.png", mode="wb")
                await f.write(await resp.read())
                await f.close()

    image1 = Image.open("./background.png")
    image2 = Image.open("resource/thumbnail.png")
    image3 = changeImageSize(1280, 720, image1)
    image4 = changeImageSize(1280, 720, image2)
    image5 = image3.convert("RGBA")
    image6 = image4.convert("RGBA")
    Image.alpha_composite(image5, image6).save("temp.png")
    img = Image.open("temp.png")
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype("resource/font.otf", 32)
    draw.text((190, 550), f"Title: {title[:50]} ...", (255, 255, 255), font=font)
    draw.text((190, 590), f"Duration: {duration}", (255, 255, 255), font=font)
    draw.text((190, 630), f"Views: {views}", (255, 255, 255), font=font)
    draw.text(
        (190, 670),
        f"Powered By: VENOM  (@VENOMxCRAZY)",
        (255, 255, 255),
        font=font,
    )
    img.save("final.png")
    os.remove("temp.png")
    os.remove("background.png")


@Client.on_message(
    commandpro(["/play", "/yt", "/ytp", "play", "yt", "ytp", "/fuck", "#"])
    & filters.group
    & ~filters.edited
    & ~filters.forwarded
    & ~filters.via_bot
)
async def play(_, message: Message):
    global que
    global useer
    
    lel = await message.reply("**𝐏𝐫𝐨𝐜𝐞𝐬𝐬𝐢𝐧𝐠 𝐒𝐨𝐧𝐠 🎸🎸...**")

    administrators = await get_administrators(message.chat)
    chid = message.chat.id

    try:
        user = await USER.get_me()
    except:
        user.first_name = "Aditya_Player"
    usar = user
    wew = usar.id
    try:
        await _.get_chat_member(chid, wew)
    except:
        for administrator in administrators:
            if administrator == message.from_user.id:
                try:
                    invitelink = await _.export_chat_invite_link(chid)
                except:
                    await lel.edit(
                        "**𝐏𝐫𝐨𝐦𝐨𝐭𝐞 𝐌𝐞 𝐀𝐬 𝐀 𝐀𝐝𝐦𝐢𝐧 𝐓𝐨 𝐏𝐥𝐚𝐲 𝐒𝐨𝐧𝐠❤️...**")
                    return

                try:
                    await USER.join_chat(invitelink)
                    await USER.send_message(
                        message.chat.id, "**𝐇𝐞𝐲 𝐈 𝐚𝐦 𝐀𝐬𝐬𝐢𝐬𝐭𝐚n𝐭 𝐈 𝐣𝐨𝐢𝐧𝐞𝐝 𝐟𝐨𝐫 𝐏𝐥𝐚𝐲𝐢𝐧𝐠 𝐒𝐨𝐧𝐠 𝐎𝐧 𝐕𝐂...**")

                except UserAlreadyParticipant:
                    pass
                except Exception:
                    await lel.edit(
                        f"**𝐏𝐥𝐞𝐚𝐬𝐞 𝐀𝐝𝐝 𝐌𝐲 𝐀𝐬𝐬𝐢𝐬𝐭𝐚𝐧𝐭 𝐦𝐚𝐧𝐮𝐥𝐥𝐲 𝐨𝐫 𝐜𝐨𝐧𝐭𝐚𝐜𝐭 𝐦𝐲 𝐎𝐰𝐧𝐞𝐫 @{OWNER_USERNAME}...**")
    try:
        await USER.get_chat(chid)
    except:
        await lel.edit(
            f"**𝐏𝐥𝐞𝐚𝐬𝐞 𝐀𝐝𝐝 𝐌𝐲 𝐀𝐬𝐬𝐢𝐬𝐭𝐚𝐧𝐭 𝐦𝐚𝐧𝐮𝐥𝐥𝐲 𝐨𝐫 𝐜𝐨𝐧𝐭𝐚𝐜𝐭 𝐦𝐲 𝐎𝐰𝐧𝐞𝐫 @{OWNER_USERNAME} ❤️...**")
        return
    
    audio = (
        (message.reply_to_message.audio or message.reply_to_message.voice)
        if message.reply_to_message
        else None
    )
    url = get_url(message)

    if audio:
        if round(audio.duration / 60) > DURATION_LIMIT:
            raise DurationLimitError(
                f"**play music less \n then  {DURATION_LIMIT} minutes...**"
            )

        file_name = get_file_name(audio)
        title = file_name
        thumb_name = "https://te.legra.ph/file/d4094ea0b4f1d94ed2932.png"
        thumbnail = thumb_name
        duration = round(audio.duration / 60)
        views = "Locally added"

        keyboard = InlineKeyboardMarkup(
            [
                [
                        InlineKeyboardButton(text="𝐆 𝐑 𝐎 𝐔 𝐏", url=f"https://t.me/{SUPPORT_GROUP}"),
                      InlineKeyboardButton(text="𝐂 𝐇 𝐀 𝐍 𝐍 𝐄 𝐋", url=f"https://t.me/{SUPPORT_CHANNEL}"),
                  ],[
                      InlineKeyboardButton(text="𝐎 𝐖 𝐍 𝐄 𝐑", url=f"https://t.me/{OWNER_USERNAME}")

                ]
            ]
        )

        requested_by = message.from_user.first_name
        await generate_cover(requested_by, title, views, duration, thumbnail)
        file_path = await converter.convert(
            (await message.reply_to_message.download(file_name))
            if not path.isfile(path.join("downloads", file_name))
            else file_name
        )

    elif url:
        try:
            results = YoutubeSearch(url, max_results=1).to_dict()
            # print results
            title = results[0]["title"]
            thumbnail = results[0]["thumbnails"][0]
            thumb_name = f"thumb{title}.jpg"
            thumb = requests.get(thumbnail, allow_redirects=True)
            open(thumb_name, "wb").write(thumb.content)
            duration = results[0]["duration"]
            url_suffix = results[0]["url_suffix"]
            views = results[0]["views"]
            durl = url
            durl = durl.replace("youtube", "youtubepp")

            secmul, dur, dur_arr = 1, 0, duration.split(":")
            for i in range(len(dur_arr) - 1, -1, -1):
                dur += int(dur_arr[i]) * secmul
                secmul *= 60

            keyboard = InlineKeyboardMarkup(
            [
                [
                        InlineKeyboardButton(text="𝐆 𝐑 𝐎 𝐔 𝐏", url=f"https://t.me/{SUPPORT_GROUP}"),
                      InlineKeyboardButton(text="𝐂 𝐇 𝐀 𝐍 𝐍 𝐄 𝐋", url=f"https://t.me/{SUPPORT_CHANNEL}"),
                  ],[
                      InlineKeyboardButton(text="𝐎 𝐖 𝐍 𝐄 𝐑", url=f"https://t.me/{OWNER_USERNAME}")

                ]
            ]
        )

        except Exception as e:
            title = "NaN"
            thumb_name = "https://te.legra.ph/file/d4094ea0b4f1d94ed2932.png"
            duration = "NaN"
            views = "NaN"
            keyboard = InlineKeyboardMarkup(
            [
                [
                        InlineKeyboardButton(text="𝐆 𝐑 𝐎 𝐔 𝐏", url=f"https://t.me/{SUPPORT_GROUP}"),
                      InlineKeyboardButton(text="𝐂 𝐇 𝐀 𝐍 𝐍 𝐄 𝐋", url=f"https://t.me/{SUPPO_CHANNEL}"),
                  ],[
                      InlineKeyboardButton(text="𝐎 𝐖 𝐍 𝐄 𝐑", url=f"https://t.me/{OWNER_USERNAME}")

                ]
            ]
        )

        if (dur / 60) > DURATION_LIMIT:
            await lel.edit(
                f"**𝐏𝐥𝐚𝐲 𝐓𝐡𝐞 𝐒𝐨𝐧𝐠 𝐋𝐞𝐬𝐬 𝐓𝐡𝐞𝐧  {DURATION_LIMIT} 𝐌𝐢𝐧𝐮𝐭𝐞𝐬 🩸...**"
            )
            return
        requested_by = message.from_user.first_name
        await generate_cover(requested_by, title, views, duration, thumbnail)
        file_path = await converter.convert(youtube.download(url))
    else:
        if len(message.command) < 2:
            return await lel.edit(
                "**𝐏𝐥𝐞𝐚𝐬𝐞 𝐓𝐲𝐩𝐞 𝐭𝐡𝐞 𝐬𝐨𝐧𝐠 𝐍𝐚𝐦𝐞 𝐓𝐨 𝐏𝐥𝐚𝐲 𝐌𝐮𝐬i𝐜...**"
            )
        await lel.edit("**𝐂𝐨𝐧𝐧𝐞𝐜𝐭𝐢𝐧𝐠  𝐓𝐨  𝐒𝐞𝐫𝐯𝐞𝐫🩸...**")
        query = message.text.split(None, 1)[1]
        # print(query)
        try:
            results = YoutubeSearch(query, max_results=1).to_dict()
            url = f"https://youtube.com{results[0]['url_suffix']}"
            # print results
            title = results[0]["title"]
            thumbnail = results[0]["thumbnails"][0]
            thumb_name = f"thumb{title}.jpg"
            thumb = requests.get(thumbnail, allow_redirects=True)
            open(thumb_name, "wb").write(thumb.content)
            duration = results[0]["duration"]
            url_suffix = results[0]["url_suffix"]
            views = results[0]["views"]
            durl = url
            durl = durl.replace("youtube", "youtubepp")

            secmul, dur, dur_arr = 1, 0, duration.split(":")
            for i in range(len(dur_arr) - 1, -1, -1):
                dur += int(dur_arr[i]) * secmul
                secmul *= 60

        except Exception as e:
            await lel.edit(
                "**🔊𝐒𝐨𝐧𝐠 𝐍𝐨𝐭 𝐟𝐨𝐮𝐧𝐝 𝐏𝐥𝐞𝐚𝐬𝐞 𝐓𝐫𝐲 𝐀𝐠𝐚𝐢𝐧...**"
            )
            print(str(e))
            return

        keyboard = InlineKeyboardMarkup(
            [
                [
                        InlineKeyboardButton(text="𝐆 𝐑 𝐎 𝐔 𝐏", url=f"https://t.me/{SUPPORT_GROUP}"),
                      InlineKeyboardButton(text="𝐂 𝐇 𝐀 𝐍 𝐍 𝐄 𝐋", url=f"https://t.me/{SUPPORT_CHANNEL}"),
                  ],[
                      InlineKeyboardButton(text="𝐎 𝐖 𝐍 𝐄 𝐑", url=f"https://t.me/{OWNER_USERNAME}")

                ]
            ]
        )

        if (dur / 60) > DURATION_LIMIT:
            await lel.edit(
                f"**𝐏𝐥𝐚𝐲 𝐓𝐡𝐞 𝐒𝐨𝐧𝐠 𝐋𝐞𝐬𝐬 𝐓𝐡𝐞𝐧  {DURATION_LIMIT} 𝐌𝐢𝐧𝐮𝐭𝐞𝐬 🩸...**"
            )
            return
        requested_by = message.from_user.first_name
        await generate_cover(requested_by, title, views, duration, thumbnail)
        file_path = await converter.convert(youtube.download(url))
    ACTV_CALLS = []
    chat_id = message.chat.id
    for x in clientbot.pytgcalls.active_calls:
        ACTV_CALLS.append(int(x.chat_id))
    if int(chat_id) in ACTV_CALLS:
        position = await queues.put(chat_id, file=file_path)
        await message.reply_photo(
            photo="final.png",
            caption="**𝐒𝐨𝐧𝐠 𝐐𝐮𝐞𝐃 𝐀𝐓» `{}` 🩸...**".format(position),
            reply_markup=keyboard,
        )
    else:
        await clientbot.pytgcalls.join_group_call(
                chat_id, 
                InputStream(
                    InputAudioStream(
                        file_path,
                    ),
                ),
                stream_type=StreamType().local_stream,
            )

        await message.reply_photo(
            photo="final.png",
            reply_markup=keyboard,
            caption="**𝐏𝐥𝐚𝐲𝐢𝐧𝐠🎸**".format(),
           )

    os.remove("final.png")
    return await lel.delete()
    
    
@Client.on_message(commandpro(["/pause", "pause"]) & other_filters)
@errors
@authorized_users_only
async def pause(_, message: Message):
    await clientbot.pytgcalls.pause_stream(message.chat.id)
    await message.reply_photo(
                             photo="https://te.legra.ph/file/d1b8c412b0873b6fe1abc.png", 
                             caption="**𝐏𝐚𝐮𝐬𝐞𝐝⏸...**"
    )


@Client.on_message(commandpro(["/resume", "resume"]) & other_filters)
@errors
@authorized_users_only
async def resume(_, message: Message):
    await clientbot.pytgcalls.resume_stream(message.chat.id)
    await message.reply_photo(
                             photo="https://te.legra.ph/file/d1b8c412b0873b6fe1abc.png", 
                             caption="**𝐑𝐞𝐬𝐮𝐦𝐞⏹...**"
    )



@Client.on_message(commandpro(["/Next", "/Skip", "skip", "next"]) & other_filters)
@errors
@authorized_users_only
async def skip(_, message: Message):
    global que
    ACTV_CALLS = []
    chat_id = message.chat.id
    for x in clientbot.pytgcalls.active_calls:
        ACTV_CALLS.append(int(x.chat_id))
    if int(chat_id) not in ACTV_CALLS:
        await message.reply_text("**𝐏𝐥𝐚𝐲 𝐓𝐡𝐞 𝐒𝐨𝐧𝐠 𝐓𝐨 𝐒𝐤𝐢𝐩 😂...**")
    else:
        queues.task_done(chat_id)
        
        if queues.is_empty(chat_id):
            await clientbot.pytgcalls.leave_group_call(chat_id)
        else:
            await clientbot.pytgcalls.change_stream(
                chat_id, 
                InputStream(
                    InputAudioStream(
                        clientbot.queues.get(chat_id)["file"],
                    ),
                ),
            )


    await message.reply_photo(
                             photo="https://te.legra.ph/file/0b166f1606f270afae443.png", 
                             caption=f'**𝐒𝐊𝐈𝐏𝐄𝐃...**'
   ) 


@Client.on_message(commandpro(["/end", "end", "/stop", "stop", "x"]) & other_filters)
@errors
@authorized_users_only
async def stop(_, message: Message):
    try:
        clientbot.queues.clear(message.chat.id)
    except QueueEmpty:
        pass

    await clientbot.pytgcalls.leave_group_call(message.chat.id)
    await message.reply_photo(
                             photo="https://te.legra.ph/file/3602370d14c0d3e6b700c.png", 
                             caption="**𝐒𝐭𝐨𝐩𝐩𝐞𝐝...**"
    )


@Client.on_message(commandpro(["reload", "refresh"]))
@errors
@authorized_users_only
async def admincache(client, message: Message):
    set(
        message.chat.id,
        (
            member.user
            for member in await message.chat.get_members(filter="administrators")
        ),
    )

    await message.reply_photo(
                              photo="https://te.legra.ph/file/d4094ea0b4f1d94ed2932.png",
                              caption="**𝐑𝐞𝐥𝐨𝐝𝐞𝐝....**"
    )
