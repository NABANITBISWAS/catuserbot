# Created by @kirito6969

import io
import logging
import os
from re import sub

from PIL import Image, ImageDraw

from . import catub
from ..core.managers import edit_or_reply, edit_delete

plugin_category = "extra"
logger = logging.getLogger(__name__)


@catub.cat_cmd(
    pattern="tgs ?(.*)",
    command=("tgs", plugin_category),
    info={
        "header": "Destory a sticker",
        "usage": "{tr}tgs <reply to a animated sticker>",
    },
)
async def tgscmd(message):
    """Tgs Killer"""
    reply = await message.get_reply_message()
    if not reply:
        await edit_delete(message, "`Reply to an animated sticker`", 3)
        return
    if not reply.file:
        await edit_delete(message, "`Reply to an animated sticker`", 3)
        return
    if not reply.file.name.endswith(".tgs"):
        await edit_delete(message, "`Reply to an animated sticker`", 3)
        return
        await reply.download_media("tgs.tgs")
        await edit_or_reply(event, "`Fixing this sticker...`")
        os.system("lottie_convert.py tgs.tgs json.json")
        json = open("json.json", "r")
        jsn = json.read()
        json.close()
        jsn = (
            jsn.replace("[1]", "[20]")
            .replace("[2]", "[30]")
            .replace("[3]", "[40]")
            .replace("[4]", "[50]")
            .replace("[5]", "[60]")
        )

        open("json.json", "w").write(jsn)
        os.system("lottie_convert.py json.json tgs.tgs")
        await reply.reply(file="tgs.tgs")
        os.remove("json.json")
        os.remove("tgs.tgs")
        await message.delete()


@catub.cat_cmd(
    pattern="doti ?(.*)",
    command=("doti", plugin_category),
    info={
        "header": "Image to Colorful dots",
        "description": "The bigger, the slower and bugger! Recommended not more than 1000",
        "usage": [
            "{tr}doti <reply to image> [deafult is 100]",
            "{tr}doti <count> <reply to image>",
        ],
    },
)
async def dotifycmd(message):
    """Image to RGB dots"""
    mode = False
    reply, pix = await parse(message)
    if reply:
        await dotify(message, reply, pix, mode)


@catub.cat_cmd(
    pattern="doty ?(.*)",
    command=("doty", plugin_category),
    info={
        "header": "Image to BW dots",
        "description": "The bigger, the slower and bugger! Recommended not more than 1000",
        "usage": [
            "{tr}doty <reply to image> [deafult is 100]",
            "{tr}doty <count> <reply to image>",
        ],
    },
)
async def dotificmd(message):
    """Image to BW dots """
    mode = True
    reply, pix = await parse(message)
    if reply:
        await dotify(message, reply, pix, mode)


async def parse(message):
    reply = await message.get_reply_message()
    if not reply:
        await edit_delete(message, "<b>Reply to an Image!</b>", 3, parse_mode="html")
        return None, None
    args = message.pattern_match.group(1).split(" ", 1)
    pix = 100
    if args:
        args = args[0]
        if args.isdigit():
            pix = int(args) if int(args) > 0 else 100
    return reply, pix


async def dotify(message, reply, pix, mode):
    await edit_or_reply(message, "<b>Putting dots...</b>", parse_mode="html")
    count = 24
    im_ = Image.open(io.BytesIO(await reply.download_media(bytes)))
    if im_.mode == "RGBA":
        temp = Image.new("RGB", im_.size, "#000")
        temp.paste(im_, (0, 0), im_)
        im_ = temp

    im = im_.convert("L")
    im_ = im if mode else im_
    [_.thumbnail((pix, pix)) for _ in [im, im_]]
    w, h = im.size
    img = Image.new(im_.mode, (w * count + (count // 2), h * count + (count // 2)), 0)
    ImageDraw.Draw(img)

    def cirsle(im, x, y, r, fill):
        x += r // 2
        y += r // 2
        draw = ImageDraw.Draw(im)
        draw.ellipse((x - r, y - r, x + r, y + r), fill)
        return im

    _x = _y = count // 2
    for x in range(w):
        for y in range(h):
            r = im.getpixel((x, y))
            fill = im_.getpixel((x, y))
            cirsle(img, _x, _y, r // count, fill)
            _y += count
        _x += count
        _y = count // 2

    out = io.BytesIO()
    out.name = "out.png"
    img.save(out)
    out.seek(0)
    await reply.reply(file=out)
    await message.delete()
