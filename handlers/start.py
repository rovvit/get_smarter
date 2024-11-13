from aiogram import Router, F
from aiogram.filters import CommandStart, Command
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder
from aiogram.types import Message, KeyboardButton, CallbackQuery
from sheet_parsers.cities_parser import get_city_question, get_city_by_id

HELP_COMMANDS = """
Список команд бота:
/start - начало работы с ботом
/help - вывести текущее сообщение
/test - test
"""

start_router = Router()


@start_router.message(CommandStart())
async def cmd_start(message: Message):
    builder = ReplyKeyboardBuilder()
    builder.row(
        KeyboardButton(text='Хочу вопрос с выбором')
    )
    builder.row(
        KeyboardButton(text='Вторая кнопка')
    )
    await message.answer("Бот для чгкшной бинготы", reply_markup=builder.as_markup(resize_keyboard=True))


@start_router.message(F.text.lower() == 'хочу вопрос с выбором')
async def multi_choice_question(message: Message):
    builder = ReplyKeyboardBuilder()
    builder.row(
        KeyboardButton(text='Города')
    )
    await message.reply("Выберете тему", reply_markup=builder.as_markup(resize_keyboard=True))


@start_router.message(Command("help"))
async def cmd_start(message: Message):
    await message.answer(HELP_COMMANDS)


@start_router.message(Command("test"))
async def cmd_start(message: Message):
    await message.answer('test')


# question = {
#     "id": 1,
#     "city": "Москва",
#     "answers": ["Россия", "Франция", "Германия", "Мексика"],
#     "correct": "Россия"
# }
@start_router.message(F.text.lower() == 'города')
async def cities_multi_choice(message: Message):
    question = get_city_question()  # [ id, city, country, comment, answers ]

    builder = InlineKeyboardBuilder()
    for item in question["choices"]:
        builder.button(text=item,
                       callback_data='city_' + str(question['id']) + '_' + item)
    builder.adjust(4, 1)
    await message.answer(f"В какой стране находится {question['question']}?",
                         reply_markup=builder.as_markup(resize_keyboard=True))


@start_router.callback_query(F.data.startswith('city'))
async def check_multi_choice(query: CallbackQuery):
    await query.answer()
    await query.message.delete_reply_markup()
    answer = query.data.split('_')
    correct_ans = get_city_by_id(int(answer[1]))
    if answer[2] == correct_ans[1]:
        await query.message.answer(f'Правильно! Город известен {correct_ans[2]}')
    else:
        await query.message.answer(f'Неправильно! Правильный ответ был {correct_ans[1]}, потому что {correct_ans[2]}')
