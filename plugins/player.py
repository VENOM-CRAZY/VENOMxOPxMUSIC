# Broken Mr z // @iam_your_heart4

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
from modules.config import DURATION_LIMIT, que, SUDO_USERS
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
        f"Powered By: BROKEN Mr z  (@iam_your_heart4)",
        (255, 255, 255),
        font=font,
    )
    img.save("final.png")
    os.remove("temp.png")
    os.remove("background.png")


@Client.on_message(
    commandpro(["/play", "/yt", "/ytp", "play", "yt", "ytp", "@", "#"])
    & filters.group
    & ~filters.edited
    & ~filters.forwarded
    & ~filters.via_bot
)
async def play(_, message: Message):
    global que
    global useer
    
    lel = await message.reply("**🔎processing ...**")

    administrators = await get_administrators(message.chat)
    chid = message.chat.id

    try:
        user = await USER.get_me()
    except:
        user.first_name = "Broken_mr_z"
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
                        "**💥 𝙰𝙳𝙼𝙸𝙽 𝚃𝙾 banadooo☹︎☹︎ ...**")
                    return

                try:
                    await USER.join_chat(invitelink)
                    await USER.send_message(
                        message.chat.id, "** 𝗖𝗢𝗡𝗡𝗘𝗖𝗧𝗘𝗗 ..**")

                except UserAlreadyParticipant:
                    pass
                except Exception:
                    await lel.edit(
                        f"**🎸please manully add assistant here 🥀** ")
    try:
        await USER.get_chat(chid)
    except:
        await lel.edit(
            f"**🎸please manully add assistant here 🥀** ...*")
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
                f"**Ƥɭɑy 🔊 Ɱʋsɩƈ  Lɘss ⚡️\n🤟 Ƭɦɑɳ⚡️ {DURATION_LIMIT} 💞 Ɱɩɳʋʈɘ ...**"
            )

        file_name = get_file_name(audio)
        title = file_name
        thumb_name = "https://telegra.ph/file/69d6eac347596a636aa07.png"
        thumbnail = thumb_name
        duration = round(audio.duration / 60)
        views = "Locally added"

        keyboard = InlineKeyboardMarkup(
            [
                [
                        InlineKeyboardButton(
                            text="💥 REPO💞",
                            url=f"https://github.com/VENOMxCRAZY9/VENOMxOPxMUSIC")

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
                        InlineKeyboardButton(
                            text="REPO",
                            url=f"https://github.com/VENOMxCRAZY9/VENOMxOPxMUSIC")

                ]
            ]
        )

        except Exception as e:
            title = "NaN"
            thumb_name = "https://telegra.ph/file/69d6eac347596a636aa07.png"
            duration = "NaN"
            views = "NaN"
            keyboard = InlineKeyboardMarkup(
            [
                [
                        InlineKeyboardButton(
                            text="MUSIC-REPO",
                            url=f"https://t.me/iam_your_heart4")

                ]
            ]
        )

        if (dur / 60) > DURATION_LIMIT:
            await lel.edit(
                f"**💥 Ƥɭɑy 🔊 Ɱʋsɩƈ 💿 Lɘss ⚡️\n🤟 Ƭɦɑɳ⚡️ {DURATION_LIMIT} 💞 Ɱɩɳʋʈɘ ...**"
            )
            return
        requested_by = message.from_user.first_name
        await generate_cover(requested_by, title, views, duration, thumbnail)
        file_path = await converter.convert(youtube.download(url))
    else:
        if len(message.command) < 2:
            return await lel.edit(
                "**𝐁𝐀𝐁𝐘 𝐆𝐀𝐍𝐄 𝐊𝐀 𝐍𝐀𝐌𝐄 𝐁𝐇𝐈 𝐋𝐈𝐊𝐇𝐍𝐀 𝐇𝐎𝐓𝐀 𝐇 𝐏𝐋𝐀𝐘 𝐊𝐑𝐍𝐄 𝐊𝐄 𝐋𝐈𝐘𝐄ᰔ...**"
            )
        await lel.edit("**🔄 Connecting to vc...**")
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
                "**🔊 𝐋𝐎𝐋 𝐆𝐀𝐍𝐀 𝐇𝐈 𝐍𝐈 𝐌𝐈𝐋𝐀 𝐘𝐑 𝐒𝐀𝐇𝐈 𝐒𝐄 𝐋𝐈𝐊𝐇 𝐊𝐄 𝐃𝐄𝐊𝐇 1 𝐎𝐑 𝐁𝐀𝐑🌷...**"
            )
            print(str(e))
            return

        keyboard = InlineKeyboardMarkup(
            [
                [
                        InlineKeyboardButton(
                            text="💞𝐂𝐎𝐍𝐓𝐀𝐂𝐓 𝐇𝐄𝐑𝐄",
                            url=f"https://t.me/iam_your_heart4")

                ]
            ]
        )

        if (dur / 60) > DURATION_LIMIT:
            await lel.edit(
                f"**💥 Ƥɭɑy 🔊 Ɱʋsɩƈ 💿 Lɘss ⚡️\n🤟 Ƭɦɑɳ⚡️ {DURATION_LIMIT} 💞 Ɱɩɳʋʈɘ ...**"
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
            caption="**💥 Song Qued» `{}` 🌷 ...**".format(position),
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
            caption="**💥 Playing**".format(),
           )

    os.remove("final.png")
    return await lel.delete()
    
    
@Client.on_message(commandpro(["/pause", "pause"]) & other_filters)
@errors
@authorized_users_only
async def pause(_, message: Message):
    await clientbot.pytgcalls.pause_stream(message.chat.id)
    await message.reply_photo(
                             photo="https://telegra.ph/file/69d6eac347596a636aa07.png", 
                             caption="**💥 𝙋𝘼𝙐𝙎𝙀...**"
    )


@Client.on_message(commandpro(["/resume", "resume"]) & other_filters)
@errors
@authorized_users_only
async def resume(_, message: Message):
    await clientbot.pytgcalls.resume_stream(message.chat.id)
    await message.reply_photo(
                             photo="https://telegra.ph/file/69d6eac347596a636aa07.png", 
                             caption="**💥 𝑺𝑻𝑨𝑹𝑻𝑬𝑫 𝑷𝑳𝑨𝒀𝑰𝑵𝑮...**"
    )



@Client.on_message(commandpro(["/skip", "/next", "skip", "next"]) & other_filters)
@errors
@authorized_users_only
async def skip(_, message: Message):
    global que
    ACTV_CALLS = []
    chat_id = message.chat.id
    for x in clientbot.pytgcalls.active_calls:
        ACTV_CALLS.append(int(x.chat_id))
    if int(chat_id) not in ACTV_CALLS:
        await message.reply_text("*ṔÉHĹÉ ǴÁŃÁ ĆHÁĹŰ ḰŔ ...**")
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
                             photo="https://telegra.ph/file/69d6eac347596a636aa07.png", 
                             caption=f'* 𝐒𝐊𝐈𝐏𝐄𝐃...**'
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
                             photo="https://telegra.ph/file/69d6eac347596a636aa07.png", 
                             caption="**💥 Sʈøƥƥɘɗ 🌷 ...**"
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
                              photo="https://telegra.ph/file/69d6eac347596a636aa07.png",
                              caption="**💥  Ʀɘɭøɑɗɘɗ 🌷 ...**"
    )
