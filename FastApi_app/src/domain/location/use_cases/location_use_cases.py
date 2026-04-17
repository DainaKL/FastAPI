from src.domain.location.use_cases.get_locations import GetLocationsUseCase
from src.domain.location.use_cases.get_published_locations import GetPublishedLocationsUseCase
from src.domain.location.use_cases.get_location import GetLocationUseCase
from src.domain.location.use_cases.get_location_by_name import GetLocationByNameUseCase
from src.domain.location.use_cases.create_location import CreateLocationUseCase
from src.domain.location.use_cases.update_location import UpdateLocationUseCase
from src.domain.location.use_cases.delete_location import DeleteLocationUseCase


class LocationUseCases:
    def __init__(self):
        self.get_all = GetLocationsUseCase().execute
        self.get_published = GetPublishedLocationsUseCase().execute
        self.get_by_id = GetLocationUseCase().execute
        self.get_by_name = GetLocationByNameUseCase().execute
        self.create = CreateLocationUseCase().execute
        self.update = UpdateLocationUseCase().execute
        self.delete = DeleteLocationUseCase().execute
