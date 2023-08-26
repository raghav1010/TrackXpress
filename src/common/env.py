import os
import logging

from src.common.constants import ContainerEnvProjectMapper, PROD_CONTAINER, STAGE_CONTAINER, LOCAL_NAKED_URL, \
    DEFAULT_POSTGRES_URL, DEFAULT_POSTGRES_DBNAME, DEFAULT_POSTGRES_DBUSER, DEFAULT_POSTGRES_DBPASS, \
    DEFAULT_POSTGRES_PORT, DEFAULT_DOCKER_FLAG


def get_env_variable_value(variable):
    value = os.environ.get(variable)
    if value:
        return value
    return ''


def get_project_id():
    container = os.environ.get("CONTAINER_ENV")
    project_id = ContainerEnvProjectMapper.get_project_by_container(container)
    return project_id


def is_production():
    project_id = get_project_id()
    return project_id == ContainerEnvProjectMapper.get_project_by_container(PROD_CONTAINER)


def is_staging():
    project_id = get_project_id()
    return project_id == ContainerEnvProjectMapper.get_project_by_container(STAGE_CONTAINER)


if is_staging():
    logging.info("running stage server")


elif is_production():
    logging.info("running prod server")

else:
    """ =====================================================
                               LOCAL:DEV Environment
        ========================================================="""

    NAKED_URL = LOCAL_NAKED_URL
    POSTGRES_URL = os.environ.get("POSTGRES_URL", DEFAULT_POSTGRES_URL)
    POSTGRES_DBNAME = os.environ.get("POSTGRES_DB", DEFAULT_POSTGRES_DBNAME)
    POSTGRES_DBUSER = os.environ.get("POSTGRES_USER", DEFAULT_POSTGRES_DBUSER)
    POSTGRES_DBPASS = os.environ.get("POSTGRES_PASSWORD", DEFAULT_POSTGRES_DBPASS)

    POSTGRES_PORT = os.environ.get("POSTGRES_PORT", DEFAULT_POSTGRES_PORT)
    DOCKER_FLAG = os.environ.get("DOCKER_FLAG", DEFAULT_DOCKER_FLAG)

    if DOCKER_FLAG.lower() != "true":
        logging.info("running dev server in local.")
        POSTGRES_INSTANCE_URI = f"postgresql://{POSTGRES_DBUSER}:{POSTGRES_DBPASS}@{POSTGRES_URL}:" \
                                f"{POSTGRES_PORT}/{POSTGRES_DBNAME}"
    else:
        logging.info("running dev server in docker container.")
        POSTGRES_INSTANCE_URI = f"postgresql://{POSTGRES_DBUSER}:{POSTGRES_DBPASS}@{POSTGRES_URL}:" \
                                f"{POSTGRES_PORT}/{POSTGRES_DBNAME}"
