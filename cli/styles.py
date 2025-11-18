from prompt_toolkit.styles import Style


def get_prompt_style() -> Style:
    return Style.from_dict(
        {
            "": "#00ffff",  # Cyan text
            "completion-menu": "bg:#0000aa #ffffff",
            "completion-menu.completion": "bg:#0000aa #cccccc",
            "completion-menu.completion.current": "bg:#00aaaa #000000 bold",
        }
    )


def get_dark_prompt_style() -> Style:
    return Style.from_dict(
        {
            "": "#00ff00 bold",  # Green text
            "completion-menu": "bg:#1a1a1a #ffffff",
            "completion-menu.completion": "bg:#1a1a1a #aaaaaa",
            "completion-menu.completion.current": "bg:#00aa00 #000000 bold",
        }
    )
