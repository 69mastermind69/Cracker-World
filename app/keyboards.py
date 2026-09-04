from telegram import InlineKeyboardButton, InlineKeyboardMarkup

from .tools import TOOLS


def tools_keyboard():
    keyboard = []
    row = []

    for tool_id, tool_data in TOOLS.items():
        tool_name = tool_data[0]

        row.append(
            InlineKeyboardButton(
                text=tool_name,
                callback_data=f"tool:{tool_id}"
            )
        )

        if len(row) == 2:
            keyboard.append(row)
            row = []

    if row:
        keyboard.append(row)

    return InlineKeyboardMarkup(keyboard)
