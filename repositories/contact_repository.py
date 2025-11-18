from collections import defaultdict

from models.contact import Record
from models.note import Note

from search.search_service import SearchService
from cli.presenter import Presenter


class ContactRepository:
    def __init__(self):
        self.contacts = {}
        self.search_service = SearchService()
        self.notes = []

    def add_contact(self, record: Record):
        """Add a new contact or update existing one"""
        self.contacts[record.name.value] = record

    def find_contact(self, name: str) -> Record:
        """Find a contact by name"""
        return self.contacts.get(name)

    def delete_contact(self, name: str):
        """Delete a contact by name"""
        if name in self.contacts:
            del self.contacts[name]
            return True
        return False

    def get_all_contacts(self):
        """Get all contacts"""
        return list(self.contacts.values())

    def has_contact(self, name: str) -> bool:
        """Check if contact exists"""
        return name in self.contacts

    def search_contacts(self, query: str):
        return self.search_service.exact_search(self.contacts, query)

    def search_closest_contacts(self, query: str):
        return self.search_service.fuzzy_search(self.contacts, query)

    # --- Notes ---
    def add_note(self, note):
        self.notes.append(note)
        return self.format_notes(note, Presenter.success(" Note added:"))

    def del_note(self, note):
        if note not in self.notes:
            return "Note not found."

        deleted_text = note.text

        self.notes.remove(note)

        return self.format_notes(note, Presenter.success(" Note deleted:"))

    def find_note(self, query):
        query = query.lower().strip()

        for note in self.notes:
            if query in note.text.lower() or any(
                query in tag.lower() for tag in note.tags
            ):
                return note

        return None

    def search_notes(self, query=""):
        header = f"Notes matching filter: {query}" if query else " All notes"

        if not query:
            res = self.notes
        else:
            query = query.lower().strip()
            res = [
                note
                for note in self.notes
                if query in note.text.lower()
                or any(query in tag.lower() for tag in note.tags)
            ]

        return (res, self.format_notes(res, header))

    def format_notes(self, notes, header=""):
        if notes is None or (isinstance(notes, list) and not notes):
            return " No notes to show."

        if isinstance(notes, Note):
            notes = [notes]

        lines = []

        if header:
            lines.append(header)

        if len(notes) == 1:
            lines.append(str(notes[0]))
        else:
            for i, note in enumerate(notes, start=1):
                lines.append(f"{i}. {str(note)}")

        return "\n".join(lines)

    def edit_note(self, note, new_text=None, new_tags=None):
        if note not in self.notes:
            return "Note not found."

        if new_text is not None and len(new_text) > 0:
            note.text = new_text

        if new_tags is not None and len(new_tags) > 0:
            note.tags = new_tags

        return self.format_notes(note, Presenter.success(" Note updated:"))

    def notes_by_tags(self, notes=None):
        if not notes:
            notes = self.notes

        tag_map = defaultdict(list)
        no_tag_notes = []

        for note in notes:
            if note.tags:
                for tag in note.tags:
                    tag_map[tag].append(note)
            else:
                no_tag_notes.append(note)

        output_lines = []

        for tag in sorted(tag_map.keys()):
            output_lines.append(f"Tag: {tag}")
            for note in tag_map[tag]:
                output_lines.append(f"  {note}")
            output_lines.append("")  # пустая строка между тегами

        if no_tag_notes:
            output_lines.append("No tags:")
            for note in no_tag_notes:
                output_lines.append(f"  {note}")

        if output_lines:
            return "\n".join(output_lines)

        return "No notes to show."
