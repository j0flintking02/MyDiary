def search_entry(entries, entry_id):
    for entry in entries:
        if entry['entry_id'] == entry_id:
            return entry

