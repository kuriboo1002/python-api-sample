class ItemDomainService:
    @staticmethod
    def is_duplicate_name(name: str, items: list) -> bool:
        return any(item.name.value == name for item in items)
