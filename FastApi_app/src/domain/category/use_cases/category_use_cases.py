from src.domain.category.use_cases.get_categories import GetCategoriesUseCase
from src.domain.category.use_cases.get_category import GetCategoryUseCase
from src.domain.category.use_cases.get_category_by_slug import GetCategoryBySlugUseCase
from src.domain.category.use_cases.create_category import CreateCategoryUseCase
from src.domain.category.use_cases.update_category import UpdateCategoryUseCase
from src.domain.category.use_cases.delete_category import DeleteCategoryUseCase


class CategoryUseCases:
    def __init__(self):
        self.get_all = GetCategoriesUseCase().execute
        self.get_by_id = GetCategoryUseCase().execute
        self.get_by_slug = GetCategoryBySlugUseCase().execute
        self.create = CreateCategoryUseCase().execute
        self.update = UpdateCategoryUseCase().execute
        self.delete = DeleteCategoryUseCase().execute
