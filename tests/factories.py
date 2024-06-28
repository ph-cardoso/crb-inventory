import factory
import factory.fuzzy

from crb_inventory.database_schema import Category


class CategoryFactory(factory.Factory):
    class Meta:
        model = Category

    name = factory.Sequence(lambda n: f"Categoria Teste {n}")
    description = factory.Faker("text")
