import factory
import factory.fuzzy

from crb_inventory.database_schema import Category, CustomField, Tag


class CategoryFactory(factory.Factory):
    class Meta:
        model = Category

    name = factory.Sequence(lambda n: f"Categoria Teste {n}")
    description = factory.Faker("text")


class TagFactory(factory.Factory):
    class Meta:
        model = Tag

    name = factory.Sequence(lambda n: f"tag-test-{n}")
    description = factory.Faker("text")


class CustomFieldFactory(factory.Factory):
    class Meta:
        model = CustomField

    name = factory.Sequence(lambda n: f"field_test_{n}")
    description = factory.Faker("text")
