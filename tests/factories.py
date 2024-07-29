import factory
import factory.fuzzy

from crb_inventory.database_schema import Category, Item, Tag
from crb_inventory.services.uuid import generate_uuid_v7


class CategoryFactory(factory.Factory):
    class Meta:
        model = Category

    id = factory.LazyFunction(generate_uuid_v7)
    name = factory.Sequence(lambda n: f"Categoria Teste {n}")
    description = factory.Faker("text")


class TagFactory(factory.Factory):
    class Meta:
        model = Tag

    id = factory.LazyFunction(generate_uuid_v7)
    name = factory.Sequence(lambda n: f"tag-test-{n}")
    description = factory.Faker("text")


class ItemFactory(factory.Factory):
    class Meta:
        model = Item

    id = factory.LazyFunction(generate_uuid_v7)
    name = factory.Sequence(lambda n: f"item_{n}")
    description = factory.Faker("text")
    category_id = None
    minimum_threshold = factory.fuzzy.FuzzyInteger(1, 20)
    stock_quantity = factory.fuzzy.FuzzyInteger(21, 100)
