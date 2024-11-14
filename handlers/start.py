from aiogram import Router, F
from aiogram.filters import CommandStart, Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
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


class GameState(StatesGroup):
    choosing_game_title = State()
    game_started = State()
    root_qst_asked = State()
    # game_started = State()


@start_router.message(
    StateFilter(None),
    CommandStart()
)
async def cmd_start(message: Message, state: FSMContext):
    builder = ReplyKeyboardBuilder()
    builder.row(
        KeyboardButton(text='Хочу вопрос с выбором')
    )
    builder.row(
        KeyboardButton(text='Хочу вопрос с свободным вводом')
    )
    await message.answer("Бот для чгкшной бинготы", reply_markup=builder.as_markup(resize_keyboard=True))
    await state.set_state(GameState.choosing_game_title)


@start_router.message(
    GameState.choosing_game_title,
    F.text.lower == 'хочу вопрос с выбором'
)
async def multi_choice_question(message: Message, state: FSMContext):
    builder = ReplyKeyboardBuilder()
    builder.row(
        KeyboardButton(text='Города')
    )
    await message.reply("Выберете тему", reply_markup=builder.as_markup(resize_keyboard=True))
    await state.set_state(GameState.game_started)


@start_router.message(Command("help"))
async def cmd_help(message: Message):
    await message.answer(HELP_COMMANDS)


@start_router.message(Command("stop"))
async def cmd_stop(message: Message, state: FSMContext):
    await message.answer('Игра отменена')
    await state.set_state(GameState.choosing_game_title)


@start_router.message(Command("test"))
async def cmd_test(message: Message):
    await message.answer('test')


# question = {
#     "id": 1,
#     "city": "Москва",
#     "answers": ["Россия", "Франция", "Германия", "Мексика"],
#     "correct": "Россия"
# }
@start_router.message(
    GameState.game_started,
    F.text.lower() == 'города'
)
async def cities_multi_choice(message: Message, state: FSMContext):
    question = get_city_question()  # [ id, city, country, comment, answers ]

    builder = InlineKeyboardBuilder()
    for item in question["choices"]:
        builder.button(text=item,
                       callback_data='city_' + str(question['id']) + '_' + item)
    builder.adjust(4, 1)
    await message.answer(f"В какой стране находится {question['question']}?",
                         reply_markup=builder.as_markup(resize_keyboard=True))
    # await state.set_state(GameState.game_started)


@start_router.callback_query(
    GameState.game_started,
    F.data.startswith('city')
)
async def check_multi_choice(query: CallbackQuery):
    await query.answer()
    await query.message.delete_reply_markup()
    answer = query.data.split('_')
    correct_ans = get_city_by_id(int(answer[1]))
    if answer[2] == correct_ans[1]:
        await query.message.answer(f'Правильно! Город известен {correct_ans[2]}')
    else:
        await query.message.answer(f'Неправильно! Правильный ответ был {correct_ans[1]}, потому что {correct_ans[2]}')


@start_router.message(
    GameState.choosing_game_title,
    F.text.lower() == 'хочу вопрос с свободным вводом')
async def free_game(message: Message, state: FSMContext):
    builder = ReplyKeyboardBuilder()
    builder.row(
        KeyboardButton(text='Корни')
    )
    await message.answer("Выберете тему", reply_markup=builder.as_markup(resize_keyboard=True))
    await state.set_state(GameState.game_started)

# @start_router.message(
#     GameState.game_started,
#     F.text.lower() == 'корни'
# )
# async def root_question(message: Message, state: FSMContext):
#     qst = {
#         "id": 1,
#         "question": "хуй",
#         "ethymology": "Русский",
#         "comment": "test",
#         "answer": "писька"
#     }
#     await state.update_data(qst=qst)
#     await message.answer(f"Что означает корень {qst['question']}?")
#     await state.set_state(GameState.root_qst_asked)
#
# @start_router.message(
#     GameState.root_qst_asked
# )
# async def check_root_answer(message: Message, state: FSMContext, data: dict[str, dict]):
#     qst = data["qst"]
#     if message.text.lower == qst["answer"]:
#         await message.answer('Правильно!')
#     else:
#         await message.answer('Неправильно!')
#     await state.set_state(GameState.game_started)