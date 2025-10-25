# bot.py
import os
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

TOKEN = os.getenv("BOT_TOKEN")
if not TOKEN:
    raise ValueError("BOT_TOKEN environment variable is not set")


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("Пришлите вложение — верну его file_id.")


async def handle_attachments(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> None:
    msg = update.effective_message
    if not msg:
        return

    file_ids = []

    # Фото приходят массивом разных размеров — берём самый большой
    if msg.photo:
        largest = max(msg.photo, key=lambda p: (p.file_size or 0))
        file_ids.append(("photo", largest.file_id))
        # Если нужно ВСЕ размеры, раскомментируйте:
        # for p in msg.photo:
        #     file_ids.append(("photo", p.file_id))

    if msg.document:
        file_ids.append(("document", msg.document.file_id))
    if msg.audio:
        file_ids.append(("audio", msg.audio.file_id))
    if msg.voice:
        file_ids.append(("voice", msg.voice.file_id))
    if msg.video:
        file_ids.append(("video", msg.video.file_id))
    if msg.video_note:
        file_ids.append(("video_note", msg.video_note.file_id))
    if msg.animation:
        file_ids.append(("animation", msg.animation.file_id))  # GIF
    if msg.sticker:
        file_ids.append(("sticker", msg.sticker.file_id))

    if not file_ids:
        # Нет вложений — ничего не отвечаем, чтобы не спамить
        return

    lines = [f"{kind}: <code>{fid}</code>" for kind, fid in file_ids]
    await msg.reply_text("file_id:\n" + "\n".join(lines), parse_mode="HTML")


def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    # Обрабатываем любые сообщения и сами фильтруем вложения в хэндлере
    app.add_handler(MessageHandler(filters.ALL, handle_attachments))
    app.run_polling()


if __name__ == "__main__":
    main()
