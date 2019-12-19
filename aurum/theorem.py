from .singleton import SingletonDecorator


@SingletonDecorator
class Theorem:
    """
    Singleton class responsible act as a single source of truth regarding the experiment change's state
    Eg. inform that the source-code has changed
    """

    def __init__(self):
        self.requirements_changed = False
        self.code_changed = False
        self.dataset_changed = False
        self.parameters_changed = False

    def has_any_change(self):
        return self.requirements_changed is not False or self.code_changed is not False or \
               self.dataset_changed is not False or self.parameters_changed is not False

    def requirements_did_change(self, requirements_metadata_location_hash: str) -> None:
        self.requirements_changed = requirements_metadata_location_hash

    def code_did_change(self, code_metadata_location_hash: str) -> None:
        self.code_changed = code_metadata_location_hash

    def dataset_did_change(self, dataset_metadata_location_hash: str) -> None:
        self.dataset_changed = dataset_metadata_location_hash

    def parameters_did_change(self, parameters_metadata_location_hash: str) -> None:
        self.parameters_changed = parameters_metadata_location_hash
