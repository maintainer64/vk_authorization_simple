from pydantic import ValidationError
from typing import Sequence
import logging

logger = logging.getLogger(__name__)


class ResponseValidationError(Exception):
    code = "response_resource_validation_error"
    message = "Ответ с сервера не может быть обработан валидатором"


def validate_dict(response: dict, base_model):
    """Валидация dict.

    :param response:
    :param base_model:
    :return:
    """
    try:
        return base_model(**response)
    except TypeError as err:
        logger.error("TypeError объекта response", extra={"error": err})
        raise ResponseValidationError()
    except ValidationError as err:
        logger.error("ValidationError объекта response", extra={"error": err})
        raise ResponseValidationError()


def validate_list(response: Sequence[dict], base_model) -> list:
    """Валидация list.

    :param response:
    :param base_model:
    :return:
    """
    return [validate_dict(item, base_model) for item in response]
