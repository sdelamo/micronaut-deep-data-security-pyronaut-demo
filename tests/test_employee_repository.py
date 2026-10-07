"""``EmployeeRepository`` against a real Oracle Database."""

from decimal import Decimal

import pytest

from conftest import run_as

# Pyronaut names the generated Java class after the package and the class, so the
# repository declared in example/repository.py is the bean "example.EmployeeRepository".
EMPLOYEE_REPOSITORY = "example.EmployeeRepository"


def test_find_all(application_context):
    repository = application_context.get_bean(EMPLOYEE_REPOSITORY)
    with run_as("sergio"):
        assert len(list(repository.findAll())) == 5


def test_get_salary_aggregates(application_context):
    """The projection comes back as the ``SalaryAggregates`` dataclass, with
    ``BigDecimal`` columns converted to ``decimal.Decimal``."""
    repository = application_context.get_bean(EMPLOYEE_REPOSITORY)
    with run_as("sergio"):
        aggregates = repository.getSalaryAggregates()

    assert aggregates.min == Decimal("6900")
    assert aggregates.max == Decimal("13000")
    assert aggregates.sum == Decimal("49130")
    assert aggregates.count == 5


def test_get_salary_aggregates_requires_an_authentication(application_context):
    """``@RunAs`` with roles only cannot build an authentication from nothing.

    A Java exception crosses into Python as a foreign exception, hence
    ``BaseException``.
    """
    repository = application_context.get_bean(EMPLOYEE_REPOSITORY)
    with pytest.raises(BaseException, match="@RunAs name cannot be blank"):
        repository.getSalaryAggregates()
