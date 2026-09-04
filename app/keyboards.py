from telegram import InlineKeyboardButton, InlineKeyboardMarkup


def tools_keyboard():
    keyboard = []

    row = []

    for tool_id, tool_data in TOOLS.items():
        name = tool_data[0]

        row.append(
            InlineKeyboardButton(
                name,
                callback_data=f"tool:{tool_id}"
            )
        )

        if len(row) == 2:
            keyboard.append(row)
            row = []

    if row:
        keyboard.append(row)

    return InlineKeyboardMarkup(keyboard)
