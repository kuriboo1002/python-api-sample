from employee.domain.item import Item

from employee.domain.events import ItemCreatedEvent

class ItemFactory:
    @staticmethod
    def create(name: str, description: str):
        item = Item(name, description)
        event = ItemCreatedEvent(item)
        return item, event
