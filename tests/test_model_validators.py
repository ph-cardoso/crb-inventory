import pytest

from crb_inventory.models.validators import (
    validate_custom_field_name_value,
    validate_positive_value,
    validate_tag_name_value,
)


def test_validate_positive_value_should_return_value_when_value_is_positive():
    value = 10
    assert validate_positive_value(value) == value


def test_validate_positive_value_should_return_value_when_value_is_zero():
    value = 0
    assert validate_positive_value(value) == value


def test_validate_positive_value_should_raise_value_error_when_value_is_negative():
    value = -10
    with pytest.raises(ValueError, match="value should be greater than or equal to 0"):
        validate_positive_value(value)


def test_validate_custom_field_name_value_should_return_value_when_value_is_valid():
    value = "valid_name"
    assert validate_custom_field_name_value(value) == value


def test_validate_custom_field_name_value_should_raise_value_error_when_max_length_exceeded():
    value = "a" * 31
    with pytest.raises(
        ValueError, match="value should have a max length of 30 characters"
    ):
        validate_custom_field_name_value(value)


def test_validate_custom_field_name_value_should_raise_value_error_when_invalid_format():
    value = "invalid-name"
    with pytest.raises(
        ValueError,
        match="value should be in the format of lowercase alphanumeric characters separated by underscores",
    ):
        validate_custom_field_name_value(value)


def test_validate_tag_name_value_should_return_value_when_value_is_valid():
    value = "valid-tag"
    assert validate_tag_name_value(value) == value


def test_validate_tag_name_value_should_raise_value_error_when_max_length_exceeded():
    value = "a" * 51
    with pytest.raises(
        ValueError, match="value should have a max length of 50 characters"
    ):
        validate_tag_name_value(value)


def test_validate_tag_name_value_should_raise_value_error_when_invalid_format():
    value = "invalid_tag"
    with pytest.raises(
        ValueError,
        match="value should be in the format of lowercase alphanumeric characters separated by hyphens",
    ):
        validate_tag_name_value(value)
