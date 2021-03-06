
from . import target_ids
from . import event_ids
from .component import Identifiable, Component
from ..config import ConfigType, Config
from ..script.read_config import read_user_configuration
from ..script.script_logger import create_bus_logger


# noinspection PyUnusedLocal
def config_loader_factory(bus, config, id_manager):
    ConfigLoader(bus, config.init_options['config-file'])


class ConfigLoader(Identifiable, Component, ConfigType):
    def __init__(self, bus, config_file=None):
        Component.__init__(self, bus)
        Identifiable.__init__(self, target_ids.CONFIGURATION_LOADER)

        self.__config_file = config_file

        if config_file is not None:
            self.__config = read_user_configuration(config_file, create_bus_logger(bus))
            assert isinstance(self.__config, Config)
        else:
            self.__config = Config()

        self._listen(event_ids.CONFIG__REQUEST_LOAD, target_ids.CONFIGURATION_LOADER, self._load_config_file)

    def get_workgroup_for_display(self, monitors):
        return self.__config.get_workgroup_for_display(monitors)

    @property
    def uses_layout(self):
        return self.__config.uses_layout

    @property
    def applications(self):
        return self.__config.applications

    @property
    def hotkeys(self):
        return self.__config.hotkeys

    @property
    def commands(self):
        return self.__config.commands

    @property
    def chrome(self):
        return self.__config.chrome

    # noinspection PyUnusedLocal
    def _load_config_file(self, event_id, target_id, event_obj):
        new_config_file = self.__config_file
        if 'config-file' in event_obj:
            new_config_file = event_obj['config-file']

        new_config = read_user_configuration(new_config_file, create_bus_logger(self._bus))
        self.__config_file = new_config_file
        self.__config = new_config

        self._fire(event_ids.CONFIG__UPDATE, target_ids.BROADCAST, {})
