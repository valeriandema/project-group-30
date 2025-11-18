import sys

from cli.command_suggester import CommandSuggester
from cli.presenter import Presenter
from cli.prompt_manager import PromptManager
from handlers.command_handler import CommandHandler
from repositories.contact_repository import ContactRepository
from storage.factory import StorageFactory
from utils.utils import parse_user_input_data


def main():
    # Initialize repositories and handlers
    storage_type = sys.argv[1] if len(sys.argv) > 1 else "pkl"

    try:
        storage = StorageFactory.create_storage(storage_type)
    except ValueError as e:
        print(f"Error: {e}")
        sys.exit(1)

    repository = storage.load()
    if not isinstance(repository, ContactRepository):
        repository = ContactRepository()

    command_handler = CommandHandler(repository)
    command_suggester = CommandSuggester()
    prompt_manager = PromptManager(commands=CommandSuggester.AVAILABLE_COMMANDS)

    # Display welcome message
    Presenter.print_welcome()

    # Main loop
    try:
        while True:
            try:
                # Get user input with autocomplete and history
                user_input = prompt_manager.get_input("Enter command: ")
                if user_input:
                    command, *args = parse_user_input_data(user_input)
                    if command in ["close", "exit", "quit"]:
                        print("Good bye User!")
                        break
                    if command_handler[command]:
                        print(command_handler[command](*args))
                    else:
                        print(command_suggester.get_suggestion_message(command))
                else:
                    print('Please enter a command or use "help"')

            except KeyboardInterrupt:
                # Handle Ctrl+C gracefully
                print("\n" + Presenter.info("Goodbye!"))
                break
            except EOFError:
                # Handle Ctrl+D gracefully
                print("\n" + Presenter.info("Goodbye!"))
                break
            except Exception as e:
                # Handle unexpected errors
                print(Presenter.error(f"Unexpected error: {str(e)}"))
    finally:
        storage.save(repository)


if __name__ == "__main__":
    main()
