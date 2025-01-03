import logging
from telegram import Update
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
import chess
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
# Включаем логирование
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Инициализируем шахматную доску
board = chess.Board()

# Команда /start


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    keyboard = [
        [InlineKeyboardButton("Открыть шахматы", web_app=WebAppInfo(url="https://moglavos.github.io/chess_cur/"))]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text('Нажми на кнопку ниже, чтобы открыть шахматное приложение:', reply_markup=reply_markup)

# Команда /play
async def play(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    global board
    board = chess.Board()
    await update.message.reply_text('Игра началась! Ваш ход. Отправьте свой ход в формате e2e4.')

# Обработка сообщений с ходами
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    global board
    move = update.message.text.strip()
    
    try:
        # Пытаемся сделать ход
        chess_move = chess.Move.from_uci(move)
        if chess_move in board.legal_moves:
            board.push(chess_move)
            await update.message.reply_text(f'Ход принят: {move}\n\n{board}')
            if board.is_checkmate():
                await update.message.reply_text('Шах и мат! Игра окончена.')
                board = chess.Board()  # сбрасываем доску после игры
        else:
            await update.message.reply_text('Неправильный ход. Попробуйте еще раз.')
    except Exception as e:
        await update.message.reply_text('Ошибка! Убедитесь, что ваш ход в формате e2e4.')

# Команда /help
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text('Используйте команду /play, чтобы начать игру. Ваши ходы отправляйте в формате e2e4.')

# Основная функция
def main() -> None:
    # Вставьте свой токен ниже
    application = ApplicationBuilder().token("7515796949:AAGyuhj6uNsIWXcjzd3_GYwbEkykIgX4YxI").build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("play", play))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # Запуск бота
    application.run_polling()

if __name__ == '__main__':
    main()