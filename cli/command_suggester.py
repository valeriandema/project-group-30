"""Command suggester for analyzing user input and suggesting closest command"""

import difflib
from typing import List, Tuple


class CommandSuggester:
    """Analyze user input and suggest closest matching command"""

    # Available commands
    AVAILABLE_COMMANDS = [
        "add",
        "show",
        "all",
        "change",
        "rename",
        "delete",
        "delete-phone",
        "note-add",
        "na",
        "note-del",
        "nd",
        "note-list",
        "nl",
        "note-edit",
        "ne",
        "search-contacts",
        "birthdays",
        "help",
        "close",
        "tag",
        "exit",
        "quit",
    ]

    @staticmethod
    def suggest_command(
        user_input: str, available_commands: List[str] = None
    ) -> List[Tuple[str, float]]:
        """
        Suggest closest matching command based on user input

        Args:
            user_input: User's input command
            available_commands: List of available commands (defaults to AVAILABLE_COMMANDS)

        Returns:
            List of tuples (command, similarity_score) sorted by similarity
        """
        if available_commands is None:
            available_commands = CommandSuggester.AVAILABLE_COMMANDS

        if not user_input:
            return []

        user_input_lower = user_input.lower().strip()

        # Calculate similarity scores
        suggestions = []
        for cmd in available_commands:
            # Use SequenceMatcher for similarity
            similarity = difflib.SequenceMatcher(
                None, user_input_lower, cmd.lower()
            ).ratio()
            suggestions.append((cmd, similarity))

        # Sort by similarity (highest first) and filter out very low matches
        suggestions.sort(key=lambda x: x[1], reverse=True)
        suggestions = [
            s for s in suggestions if s[1] > 0.3
        ]  # Only suggest if >30% similar

        return suggestions[:3]  # Return top 3 suggestions

    @staticmethod
    def get_suggestion_message(user_input: str) -> str:
        """
        Get formatted suggestion message for invalid command

        Args:
            user_input: User's input command

        Returns:
            Formatted suggestion message
        """
        suggestions = CommandSuggester.suggest_command(user_input)

        if not suggestions:
            return (
                f"Unknown command: '{user_input}'. Type 'help' for available commands."
            )

        best_match = suggestions[0]
        if best_match[1] > 0.6:  # High similarity
            return f"Unknown command: '{user_input}'. Did you mean '{best_match[0]}'?"
        else:
            # Multiple suggestions
            cmd_list = ", ".join([cmd for cmd, _ in suggestions])
            return f"Unknown command: '{user_input}'. Did you mean one of: {cmd_list}?"
