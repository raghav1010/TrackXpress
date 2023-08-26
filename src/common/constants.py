from enum import Enum

PROD_CONTAINER = "prod"
STAGE_CONTAINER = "stage"
LOCAL_CONTAINER = "localhost"

LOCAL_NAKED_URL = "http://0.0.0.0:5050/"
PROD_NAKED_URL = ""
STAGE_NAKED_URL = ""


DEFAULT_POSTGRES_URL = "127.0.0.1"
DEFAULT_POSTGRES_DBNAME = "track_xpress_db"
DEFAULT_POSTGRES_DBUSER = "track_xpress_user"
DEFAULT_POSTGRES_DBPASS = "track_xpress_password"

DEFAULT_POSTGRES_PORT = 5432
DEFAULT_DOCKER_FLAG = "false"


class ContainerEnvProjectMapper(Enum):
    LOCAL = (LOCAL_CONTAINER, "local")
    STAGE = (STAGE_CONTAINER, "dummy_stage_project_id")
    PROD = (PROD_CONTAINER, "dummy_prod_project_id")

    @classmethod
    def get_project_by_container(cls, container=None):
        project_id = ''
        if not container:
            return project_id
        for c in cls:
            if c.value[0] == container:
                project_id = c.value[1]
                return project_id
        return project_id
