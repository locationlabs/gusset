"""
Test validation.
"""
from unittest import TestCase
from nose.tools import raises
from gusset.validation import assert_valid_arguments


def no_args():
    pass


def one_arg(foo):
    pass


def optional_arg(foo, bar="bar"):
    pass


class TestValidation(TestCase):

    def test_valid_arguments(self):
        assert_valid_arguments(no_args)
        assert_valid_arguments(one_arg, "foo")
        assert_valid_arguments(one_arg, foo="foo")
        assert_valid_arguments(optional_arg, "foo", "bar")
        assert_valid_arguments(optional_arg, "foo", None)
        assert_valid_arguments(optional_arg, "foo", bar="bar")
        assert_valid_arguments(optional_arg, "foo", bar=None)

    @raises
    def test_missing_argument(self):
        assert_valid_arguments(one_arg)
        assert_valid_arguments(optional_arg)
        assert_valid_arguments(optional_arg, bar="bar")

    @raises
    def test_unexpected_argument(self):
        assert_valid_arguments(no_args, "foo")
        assert_valid_arguments(one_arg, "foo", "bar")
        assert_valid_arguments(one_arg, bar="bar")
        assert_valid_arguments(optional_arg, baz="baz")
