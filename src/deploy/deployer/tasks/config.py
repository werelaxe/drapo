import yaml
from dataclasses import dataclass
from marshmallow import Schema, fields, post_load


class InvalidTaskConfigError(Exception):
    pass


@dataclass
class ServiceConfig:
    ports: list


@dataclass
class TaskConfig:
    services: list
    run_independently: bool


class ServiceConfigSchema(Schema):
    ports = fields.List(fields.Integer())

    @post_load
    def make_service_config(self, data):
        return ServiceConfig(**data)


class TaskConfigSchema(Schema):
    services = fields.Dict(fields.Nested(ServiceConfigSchema))
    run_independently = fields.Boolean()

    @post_load
    def make_task_config(self, data):
        print(data)
        return TaskConfig(**data)


task_config_schema = TaskConfigSchema()


def parse_task_config(raw_data: str) -> TaskConfigSchema:
    try:
        config = yaml.safe_load(raw_data)
        result = task_config_schema.load(config)
        if result.errors:
            raise InvalidTaskConfigError(f"Invalid config: invalid field(s), {result.errors}")
        return result.data
    except yaml.YAMLError as e:
        raise InvalidTaskConfigError(f"Invalid config: is not a valid yaml file, {e}")
