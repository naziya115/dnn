from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

# Create your states here.
class MainState(StatesGroup):
    link = State()
    grammar_check = State()
    get_audio_state = State()