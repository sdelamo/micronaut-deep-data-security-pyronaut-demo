"""``EmployeeService`` builds the home page model."""

from decimal import Decimal

from micronaut.security.authentication import Authentication

from conftest import run_as

EMPLOYEE_SERVICE = "example.EmployeeService"
USERNAME = "emma@supremo.onmicrosoft.com"


def test_employee_model(application_context):
    service = application_context.get_bean(EMPLOYEE_SERVICE)
    with run_as(USERNAME):
        model = service.employee_model(Authentication.build(USERNAME))

    assert len(list(model["employees"])) == 5
    summary = model["salarySummary"]
    assert summary.minSalary == Decimal("6900")
    assert summary.maxSalary == Decimal("13000")
    assert str(summary.averageSalary) == "9826.00"
    assert summary.employeeCount == 5


def test_employee_model_is_empty_for_anonymous(application_context):
    service = application_context.get_bean(EMPLOYEE_SERVICE)
    assert service.employee_model(None) == {}
