import factory
import factory.fuzzy

from crb_inventory.database_schema import Category, CustomField, Tag
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


class CustomFieldFactory(factory.Factory):
    class Meta:
        model = CustomField

    id = factory.LazyFunction(generate_uuid_v7)
    name = factory.Sequence(lambda n: f"field_test_{n}")
    description = factory.Faker("text")
