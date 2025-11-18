"""Prompt manager with autocomplete and in-memory history using prompt_toolkit."""

from prompt_toolkit import PromptSession
from prompt_toolkit.completion import WordCompleter
from prompt_toolkit.formatted_text import HTML
from prompt_toolkit.history import InMemoryHistory

from .styles import get_prompt_style


class PromptManager:
    def __init__(self, commands: list[str]):
        self.history = InMemoryHistory()

        self.completer = WordCompleter(commands, ignore_case=True, sentence=True)

        self.style = get_prompt_style()

        self.session = PromptSession(
            history=self.history,
            completer=self.completer,
            style=self.style,
            complete_while_typing=True,
        )

    def get_input(self, prompt_text: str = "Enter command: ") -> str:
        try:
            formatted_prompt = HTML(f"<cyan>{prompt_text}</cyan>")
            return self.session.prompt(formatted_prompt)
        except (KeyboardInterrupt, EOFError):
            raise
