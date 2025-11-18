# search/search_service.py
import difflib


class SearchService:

    def exact_search(self, contacts, query):
        query = query.lower()
        results = []

        for record in contacts.values():
            fields = self.collect_fields(record)
            combined = " ".join(fields)
            if query in combined:
                results.append(record)

        return results

    def fuzzy_search(self, contacts, query, limit=5):
        query = query.lower()
        scored = []

        for record in contacts.values():
            fields = self.collect_fields(record)

            best_score = 0
            for field in fields:
                score = difflib.SequenceMatcher(None, query, field).ratio()
                if score > best_score:
                    best_score = score

            scored.append((best_score, record))

        scored.sort(key=lambda x: x[0], reverse=True)
        return [record for score, record in scored if score >= 0.3][:limit]

    def collect_fields(self, record):
        fields = []

        if getattr(record, "name", None):
            fields.append(record.name.value.lower())

        for phone in getattr(record, "phones", []):
            fields.append(phone.value.lower())

        for email in getattr(record, "emails", []):
            fields.append(email.value.lower())

        address = getattr(record, "address", None)
        if address:
            fields.append(address.value.lower())

        birthday = getattr(record, "birthday", None)
        if birthday:
            fields.append(str(birthday).lower())

        return fields
