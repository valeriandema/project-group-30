from cli.presenter import Presenter
from models.contact import Record
from models.note import Note
from handlers.decorators import input_error
from handlers.birthday_service import BirthdayService


class CommandHandler:
    def __init__(self, repository):
        self.repository = repository
        self.birthday_service = BirthdayService(repository)
        self.commands = {
            "add": self.add_contact,
            "show": self.show_contact,
            "all": self.show_all_contacts,
            "change": self.change,
            "rename": self.edit_name,
            "delete": self.delete_contact,
            "delete-phone": self.delete_phone,
            "note-add": self.note_add,
            "na": self.note_add,
            "note-del": self.note_del,
            "nd": self.note_del,
            "note-list": self.note_list,
            "nl": self.note_list,
            "ne": self.note_edit,
            "note-edit": self.note_edit,
            "tag": self.tag,
            "search-contacts": self.search_contacts,
            "birthdays": self.show_birthdays,
            "help": self._handle_help,
        }

    def __getitem__(self, key):
        return self.commands.get(key)

    @input_error
    def add_contact(self):
        print(
            Presenter.info(
                "Let's create a new contact. Name is required. Other fields are optional"
            )
        )
        print(Presenter.info("Press Enter to skip any optional field."))

        while True:
            name = input(Presenter.highlight("Name (required): ")).strip()
            if not name:
                print(Presenter.error("Name is required. Please enter a name."))
                continue
            break

        contact = self.repository.find_contact(name)

        if contact is None:
            contact = Record(name)
            self.repository.add_contact(contact)
        else:
            return Presenter.warning(
                "Contact already exist, please use update to modify"
            )

        while True:
            phone = input(
                Presenter.info("Phone (optional): ")
                + Presenter.format_hint("[380XXXXXXXXX]")
                + ": "
            ).strip()
            if not phone:
                break
            try:
                contact.add_phone(phone)
                break
            except Exception as e:
                print(
                    Presenter.error(
                        f"Error: {e}. Please try again or press Enter to skip."
                    )
                )
                continue

        while True:
            email = input(Presenter.info("Email (optional): ")).strip()
            if not email:
                break
            try:
                contact.add_email(email)
                break
            except Exception as e:
                print(
                    Presenter.error(
                        f"Error: {e}. Please try again or press Enter to skip."
                    )
                )
                continue

        address = input(Presenter.info("Address (optional): ")).strip() or None
        if address:
            contact.set_address(address)

        while True:
            birthday = input(
                Presenter.info("Birthday (optional): ")
                + Presenter.format_hint("[dd.mm.yyyy]")
                + ": "
            ).strip()
            if not birthday:
                break
            try:
                contact.set_birthday(birthday)
                break
            except Exception as e:
                print(
                    Presenter.error(
                        f"Error: {e}. Please try again or press Enter to skip."
                    )
                )
                continue

        return Presenter.success("Contact added.")

    @input_error
    def show_contact(self):
        """Show a specific contact"""
        while True:
            name = input("Enter the name to show contact: ").strip()
            # Allow Enter to cancel
            if not name:
                return None
            break

        contact = self.repository.find_contact(name)
        if contact is None:
            raise KeyError(f"Contact {name} not found.")
        Presenter.print_contacts_table([contact])
        return ""

    @input_error
    def show_all_contacts(self):
        """Show all contacts"""
        contacts = self.repository.get_all_contacts()
        if not contacts:
            return Presenter.warning("No contacts stored.")
        Presenter.print_contacts_table(contacts)
        return ""

    @input_error
    def change(self) -> str:
        """Change a contact field - displays interactive menu"""
        while True:
            self._display_change_menu()
            choice = input("Enter your choice: ").strip()

            # Allow Enter to cancel
            if not choice:
                return "Return to main menu"

            if choice == "6":
                return "Return to main menu"

            if choice not in ["1", "2", "3", "4", "5"]:
                print(
                    Presenter.error(
                        "Invalid choice. Please enter a number from 1 to 6."
                    )
                )
                continue

            # Get contact name
            while True:
                name = input("Enter the EXISTING contact name to edit: ").strip()
                # Allow Enter to cancel
                if not name:
                    return "Return to main menu"
                break

            contact = self.repository.find_contact(name)
            if contact is None:
                raise KeyError(f"Contact {name} not found.")

            # Handle the selected option
            result = None
            if choice == "1":
                result = self._change_name(contact, name)
            elif choice == "2":
                result = self._change_phone(contact, name)
            elif choice == "3":
                result = self._change_email(contact, name)
            elif choice == "4":
                result = self._change_address(contact, name)
            elif choice == "5":
                result = self._change_birthday(contact, name)

            # Check if user cancelled (returned None)
            if result is None:
                return "Return to main menu"
            return result

    def _display_change_menu(self):
        """Display the change menu options"""
        print(Presenter.info("\nChoose what you want to edit:\n"))
        print("1. Name")
        print("2. Phone")
        print("3. Email")
        print("4. Address")
        print("5. Birthday")
        print("6. Return\n")

    @input_error
    def _change_name(self, contact: Record, current_name: str) -> str:
        """Handle name editing"""
        print(Presenter.info(f"\nCurrent contact name: {current_name}"))
        while True:
            new_name = input("Enter the NEW name for this contact: ").strip()
            # Allow Enter to cancel
            if not new_name:
                return None
            break

        if self.repository.find_contact(new_name):
            raise ValueError(f"Contact {new_name} already exists.")

        self.repository.delete_contact(current_name)
        contact.name.value = new_name
        self.repository.add_contact(contact)

        return Presenter.success(
            f"Contact name changed from {current_name} to {new_name}."
        )

    @input_error
    def _change_phone(self, contact: Record, name: str) -> str:
        """Handle phone editing"""
        if not contact.phones:
            print(Presenter.info("This contact has no phone numbers."))
            add_new = (
                input("Would you like to add a new phone? (y/n): ").strip().lower()
            )
            # Allow Enter to cancel
            if not add_new:
                return None
            if add_new == "y":
                while True:
                    new_phone = input(
                        "Enter new phone "
                        + Presenter.format_hint("[380XXXXXXXXX]")
                        + ": "
                    ).strip()
                    # Allow Enter to cancel
                    if not new_phone:
                        return None
                    try:
                        contact.add_phone(new_phone)
                        return Presenter.success(
                            f"Phone {new_phone} added to contact {name}."
                        )
                    except Exception as e:
                        print(Presenter.error(f"Error: {e}. Please try again."))
                        continue
            else:
                return Presenter.info("No changes made.")

        # Display existing phones
        print(Presenter.info("\nExisting phone numbers:"))
        for idx, phone in enumerate(contact.phones, 1):
            print(f"  {idx}. {phone.value}")

        # Get old phone selection
        while True:
            try:
                selection = input(
                    "\nEnter the number of the phone to edit (or enter the phone number directly): "
                ).strip()
                # Allow Enter to cancel
                if not selection:
                    return None
                # Try to parse as index
                try:
                    idx = int(selection)
                    if 1 <= idx <= len(contact.phones):
                        old_phone = contact.phones[idx - 1].value
                        break
                    else:
                        print(
                            Presenter.error(
                                f"Invalid selection. Please enter a number between 1 and {len(contact.phones)}."
                            )
                        )
                        continue
                except ValueError:
                    # Not a number, treat as phone value
                    old_phone = selection
                    if contact.find_phone(old_phone):
                        break
                    else:
                        print(
                            Presenter.error(
                                f"Phone {old_phone} not found. Please try again."
                            )
                        )
                        continue
            except Exception as e:
                print(Presenter.error(f"Error: {e}. Please try again."))
                continue

        # Get new phone
        while True:
            new_phone = input(
                "Enter new phone " + Presenter.format_hint("[380XXXXXXXXX]") + ": "
            ).strip()
            # Allow Enter to cancel
            if not new_phone:
                return None
            try:
                contact.edit_phone(old_phone, new_phone)
                return Presenter.success(
                    f"Phone number for {name} changed from {old_phone} to {new_phone}."
                )
            except Exception as e:
                print(Presenter.error(f"Error: {e}. Please try again."))
                continue

    @input_error
    def _change_email(self, contact: Record, name: str) -> str:
        """Handle email editing"""
        if not contact.emails:
            print(Presenter.info("This contact has no email addresses."))
            add_new = (
                input("Would you like to add a new email? (y/n): ").strip().lower()
            )
            # Allow Enter to cancel
            if not add_new:
                return None
            if add_new == "y":
                while True:
                    new_email = input("Enter new email: ").strip()
                    # Allow Enter to cancel
                    if not new_email:
                        return None
                    try:
                        contact.add_email(new_email)
                        return Presenter.success(
                            f"Email {new_email} added to contact {name}."
                        )
                    except Exception as e:
                        print(Presenter.error(f"Error: {e}. Please try again."))
                        continue
            else:
                return Presenter.info("No changes made.")

        # Display existing emails
        print(Presenter.info("\nExisting email addresses:"))
        for idx, email in enumerate(contact.emails, 1):
            print(f"  {idx}. {email.value}")

        # Get old email selection
        while True:
            try:
                selection = input(
                    "\nEnter the number of the email to edit (or enter the email address directly): "
                ).strip()
                # Allow Enter to cancel
                if not selection:
                    return None
                # Try to parse as index
                try:
                    idx = int(selection)
                    if 1 <= idx <= len(contact.emails):
                        old_email = contact.emails[idx - 1].value
                        break
                    else:
                        print(
                            Presenter.error(
                                f"Invalid selection. Please enter a number between 1 and {len(contact.emails)}."
                            )
                        )
                        continue
                except ValueError:
                    # Not a number, treat as email value
                    old_email = selection
                    if contact.find_email(old_email):
                        break
                    else:
                        print(
                            Presenter.error(
                                f"Email {old_email} not found. Please try again."
                            )
                        )
                        continue
            except Exception as e:
                print(Presenter.error(f"Error: {e}. Please try again."))
                continue

        # Get new email
        while True:
            new_email = input("Enter new email: ").strip()
            # Allow Enter to cancel
            if not new_email:
                return None
            try:
                contact.edit_email(old_email, new_email)
                return Presenter.success(
                    f"Email for {name} changed from {old_email} to {new_email}."
                )
            except Exception as e:
                print(Presenter.error(f"Error: {e}. Please try again."))
                continue

    @input_error
    def _change_address(self, contact: Record, name: str) -> str:
        """Handle address editing"""
        if contact.address:
            print(Presenter.info(f"Current address: {contact.address.value}"))

        new_address = input("Enter new address: ").strip()
        # Allow Enter to cancel
        if not new_address:
            return None
        contact.set_address(new_address)
        return Presenter.success(f"Address for {name} updated to: {new_address}.")

    @input_error
    def _change_birthday(self, contact: Record, name: str) -> str:
        """Handle birthday editing"""
        if contact.birthday:
            print(Presenter.info(f"Current birthday: {contact.birthday}"))

        while True:
            birthday = input(
                "Enter new birthday " + Presenter.format_hint("[dd.mm.yyyy]") + ": "
            ).strip()
            # Allow Enter to cancel
            if not birthday:
                return None

            try:
                contact.set_birthday(birthday)
                return Presenter.success(f"Birthday for {name} updated to: {birthday}.")
            except Exception as e:
                print(Presenter.error(f"Error: {e}. Please try again."))
                continue

    @input_error
    def edit_name(self) -> str:
        """Rename a contact"""
        print(Presenter.info("Let's update contact name. Please enter contact name"))
        while True:
            name = input(Presenter.info("Name (required): ")).strip()
            if not name:
                print(Presenter.error("Name is required. Please enter a name."))
                continue
            break

        contact = self.repository.find_contact(name)

        if not contact:
            raise KeyError(f"Contact {name} not found.")

        while True:
            new_name = input(Presenter.info("New name (required): ")).strip()
            if not new_name:
                print(Presenter.error("New name is required. Please enter a name."))
                continue
            break

        if self.repository.find_contact(new_name):
            raise ValueError(f"Contact {new_name} already exists.")

        self.repository.delete_contact(name)
        contact.name.value = new_name
        self.repository.add_contact(contact)

        return Presenter.success(f"Contact name changed from {name} to {new_name}.")

    @input_error
    def delete_contact(self):
        """Delete a contact"""
        print(Presenter.info("Let's delete contact. Please enter contact name"))
        while True:
            name = input(Presenter.info("Name (required): ")).strip()
            if not name:
                print(Presenter.error("Name is required. Please enter a name."))
                continue
            break

        record = self.repository.find_contact(name)
        if record is None:
            raise KeyError(f"Contact {name} not found.")
        print(Presenter.warning("Do you really want to remove this contact?"))
        response = input("(y/n): ").strip()
        if response == "y":
            self.repository.delete_contact(name)
            return Presenter.success(f"Contact {name} deleted successfully.")
        else:
            return Presenter.info("Cancelled. Returning to main menu.")

    @input_error
    def delete_phone(self) -> str:
        """Delete a phone number from a contact"""
        print(
            Presenter.info(
                "Let's delete phone number from contact. Please enter contact name"
            )
        )
        while True:
            name = input(Presenter.info("Name (required): ")).strip()
            if not name:
                print(Presenter.error("Name is required. Please enter a name."))
                continue
            break
        record = self.repository.find_contact(name)
        if not record:
            raise KeyError(f"Contact {name} not found.")

        Presenter.print_contacts_table([record])

        if len(record.phones) == 0:
            return Presenter.error(
                "This contact doesn’t have a phone number. Nothing to delete."
            )

        while True:
            phone = input(Presenter.info("Phone to delete(required): ")).strip()
            if not phone:
                print(Presenter.error("Phone is required. Please enter a value."))
                continue
            break

        phone_obj = record.find_phone(phone)
        if not phone_obj:
            return Presenter.error(f"Phone {phone} not found for contact {name}.")

        record.remove_phone(phone)
        return Presenter.success(f"Phone {phone} removed from contact {name}.")

    @input_error
    def search_contacts(self) -> str:
        while True:
            query = input("Query string(required): ").strip()
            if not query:
                print("Query is required. Please enter a search value.\n")
                continue
            break
        exact_results = self.repository.search_contacts(query)

        if exact_results:
            print(Presenter.info(f"\nFound {len(exact_results)} contact(s):"))
            Presenter.print_contacts_table(exact_results)
            return ""

        closest = self.repository.search_closest_contacts(query)

        if closest:
            print(Presenter.warning(f"\nNo exact matches for '{query}'."))
            print(Presenter.info("Most similar contacts:"))
            Presenter.print_contacts_table(closest)
            return ""

        return Presenter.warning(f"No contacts found matching '{query}'.")

    @input_error
    def show_birthdays(self, days: str) -> str:
        """Show contacts with birthdays within specified number of days"""
        try:
            days_int = int(days)
        except ValueError:
            raise ValueError(
                f"Invalid number of days: {days}. Please provide a valid integer."
            )
        results = self.birthday_service.find_near(days_int)
        Presenter.print_birthdays_table(results, days_int)
        return ""

    @input_error
    def note_add(self, text=None, tags=None):
        while not text:
            text = input(Presenter.info("Enter note text: ")).strip()

        if tags is None:
            raw = input(
                Presenter.info(
                    "Enter tags separated by commas (or press Enter to continue): "
                )
            ).strip()
            if raw:
                tags = [t.strip() for t in raw.split(",") if t.strip()]
            else:
                tags = []
        else:
            if isinstance(tags, str):
                tags = [t.strip() for t in tags.split(",") if t.strip()]

        note = Note(text, tags)

        return self.repository.add_note(note)

    @input_error
    def note_del(self, query=None):
        while True:
            notes, msg = self.repository.search_notes(query)
            print(msg)

            query = input(
                Presenter.info("Enter a search string (or press Enter to continue): ")
            ).strip()
            if not query:
                break

        if not notes:
            return "No notes to delete. Deletion cancelled."

        while True:
            user_input = input(
                Presenter.info(
                    f"Enter the number of the note to delete 1-{len(notes)} (or press Enter to exit): "
                )
            ).strip()

            if not user_input:
                break

            try:
                index = int(user_input)
                if not 1 <= index <= len(notes):
                    print(Presenter.warning("Invalid number. Try again."))
                    continue
            except ValueError:
                print(Presenter.warning("Please enter a valid number."))
                continue

            note_to_delete = notes[index - 1]
            print(self.repository.del_note(note_to_delete))
            break

        return ""

    @input_error
    def note_list(self, query=None):
        while True:
            notes, msg = self.repository.search_notes(query)
            print(msg)

            query = input(
                Presenter.info("Enter a search string (or press Enter to exit): ")
            ).strip()
            if not query:
                break

        return ""

    @input_error
    def note_edit(self, query=None):
        while True:
            notes, msg = self.repository.search_notes(query)
            print(msg)

            query = input(
                Presenter.info("Enter a search string (or press Enter to continue): ")
            ).strip()
            if not query:
                break

        if not notes:
            return "No notes to edit. Edit cancelled."

        while True:
            user_input = input(
                Presenter.info(
                    f"Enter the number of the note to edit 1-{len(notes)} (or press Enter to exit): "
                )
            ).strip()

            if not user_input:
                return "Edit cancelled."

            try:
                index = int(user_input)
                if not 1 <= index <= len(notes):
                    print(Presenter.warning("Invalid number. Try again."))
                    continue
            except ValueError:
                print(Presenter.warning("Please enter a valid number."))
                continue

            note_to_edit = notes[index - 1]
            break

        print(self.repository.format_notes(note_to_edit, " Editing..."))
        new_text = input(
            Presenter.info("Enter a new note text (or press Enter to continue): ")
        ).strip()

        tags = input(
            Presenter.info(
                "Enter new tags separated by commas (or press Enter to continue): "
            )
        ).strip()
        if tags:
            tags = [t.strip() for t in tags.split(",") if t.strip()]

        return self.repository.edit_note(note_to_edit, new_text, tags)

    @input_error
    def tag(self):
        return self.repository.notes_by_tags()

    def _handle_help(self):
        """Display help information in a formatted table"""
        Presenter.print_help_table()
        return ""
