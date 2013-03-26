import os


class FGConst:
    DEFAULT_NIMBUS_VERSION = "2.9"
    DEFAULT_NIMBUS_DB = "sqlite3"
    DEFAULT_OPENSTACK_VERSION = "essex"

    DEFAULT_CONFIG_FILENAME = "futuregrid.cfg"
    DEFAULT_CONFIG_FILEPATH = os.getenv("HOME") + "/.futuregrid/"
