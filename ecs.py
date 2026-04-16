from __future__ import annotations
from typing import Type, TypeVar, Generic
from components.base import Component

T = TypeVar("T", bound=Component)

class ECS:
    """Einfacher Entity-Component-System Manager."""
    
    def __init__(self):
        self.entities: list[Entity] = []
        self.next_id = 0

    def create_entity(self) -> Entity:
        """Erstellt eine neue Entity und gibt sie zurück."""
        entity = Entity(self.next_id)
        self.entities.append(entity)
        self.next_id += 1
        return entity

    def add_component(self, entity: Entity, component: Component) -> None:
        """Fügt einer Entity eine Komponente hinzu."""
        entity.add_component(component)

    def get_component(self, entity: Entity, component_type: Type[T]) -> T | None:
        """Gibt eine Komponente einer Entity zurück (oder None)."""
        return entity.get_component(component_type)

    def get_entities_with(self, component_type: Type[T]) -> list[tuple[Entity, T]]:
        """Gibt alle Entities zurück, die eine bestimmte Komponente besitzen."""
        result = []
        for entity in self.entities:
            comp = entity.get_component(component_type)
            if comp is not None:
                result.append((entity, comp))
        return result


class Entity:
    """Eine einzelne Entity (Spieler, Monster, Item, ...)."""
    
    def __init__(self, eid: int):
        self.id = eid
        self.components: dict[type, Component] = {}

    def add_component(self, component: Component) -> None:
        self.components[type(component)] = component

    def get_component(self, component_type: Type[T]) -> T | None:
        return self.components.get(component_type)

    def has_component(self, component_type: Type) -> bool:
        return component_type in self.components