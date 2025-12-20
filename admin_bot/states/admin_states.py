from aiogram.fsm.state import State, StatesGroup

class GenerateLinkStates(StatesGroup):
    waiting_for_resource = State()
    waiting_for_post_no = State()
    waiting_for_description = State()
    waiting_for_extra_message = State()

class RegeneratePostStates(StatesGroup):
    waiting_for_post_no = State()

class GenerateBatchStates(StatesGroup):
    waiting_for_post_no = State()
    waiting_for_description = State()
    waiting_for_extra_message = State()
    waiting_for_resources = State()

class BroadcastStates(StatesGroup):
    waiting_for_message = State()
    waiting_for_duration = State()

class AddForceSubStates(StatesGroup):
    waiting_for_channel_link = State()
    waiting_for_placeholder = State()

class BanUserStates(StatesGroup):
    waiting_for_user_id = State()

class UnbanUserStates(StatesGroup):
    waiting_for_user_id = State()

class SetMediaAccessStates(StatesGroup):
    waiting_for_count = State()

class SetPaidAccessStates(StatesGroup):
    waiting_for_user_id = State()
    waiting_for_count = State()

class SetPasswordStates(StatesGroup):
    waiting_for_password = State()

class SetDeletionTimeStates(StatesGroup):
    waiting_for_time = State()

class SetTokenLimitStates(StatesGroup):
    waiting_for_limit = State()

class SetHowToVerifyStates(StatesGroup):
    waiting_for_link = State()
