
from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from plugins.pm_filter import filter_query

@Client.on_message(filters.command("start") & filters.private)
async def start_handler(client: Client, message: Message):
    if len(message.command) > 1:
        payload = message.command[1]
        if payload.startswith("getfile-"):
            keyword = payload.replace("getfile-", "").replace("-", " ")
            message.text = keyword  # Send fake message to autofilter
            return await filter_query(client, message)

    await message.reply(
        "Hello! I am your AutoFilter Bot.\n\n"
        "Use /link <file name> to get a sharable link.",
        quote=True
    )

@Client.on_message(filters.command(["link", "links"]) & filters.private)
async def get_file_link(client: Client, message: Message):
    if len(message.command) < 2:
        return await message.reply(
            "Please provide a keyword to generate a link.\n\nExample:\n`/link game of thrones`",
            quote=True
        )

    query_text = " ".join(message.command[1:]).strip()
    keyword = "-".join(message.command[1:]).lower()
    bot_username = (await client.get_me()).username
    link = f"https://t.me/{bot_username}?start=getfile-{keyword}"

    await message.reply(
        f"**Here is your link for:** `{query_text}`\n{link}",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("ðŸ”— Share Link", url=link)]
        ]),
        disable_web_page_preview=False,
        quote=True,
        parse_mode="markdown"
    )
