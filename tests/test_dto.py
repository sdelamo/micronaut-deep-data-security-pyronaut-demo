"""The DTOs are introspected and round-trip through JSON.

The checks run against the Java classes ``pyronaut process`` generates for the
dataclasses, which is what Micronaut Data and Micronaut Serialization see.
"""

import java
import pytest
from java.math import BigDecimal
from java.util import Objects
from micronaut.core.beans import BeanIntrospection
from micronaut.json import JsonMapper
from pyronaut.test import MicronautTest, micronaut_test_fixture

EmployeeDto = java.type("example.EmployeeDto")
SalaryAggregates = java.type("example.SalaryAggregates")
SalarySummaryDto = java.type("example.SalarySummaryDto")


@pytest.fixture
def json_mapper(request):
    fixture = micronaut_test_fixture(
        request,
        MicronautTest(
            environments=["test"],
            start_application=False,
            properties={"datasources.default.enabled": "false"},
        ),
    )
    yield fixture.get_bean(JsonMapper)
    fixture.stop()


def property_names(java_class) -> set[str]:
    introspection = BeanIntrospection.getIntrospection(java_class)
    return {str(p.getName()) for p in introspection.getBeanProperties()}


def test_employee_dto_is_introspected():
    assert property_names(EmployeeDto) == {"id", "name", "salary", "phone"}


def test_employee_dto_can_be_serialized_and_deserialized(json_mapper):
    dto = EmployeeDto(42, "Sherlock Holmes", BigDecimal("12345.67"), "+1-555-0100")

    json = json_mapper.writeValueAsString(dto)
    decoded = json_mapper.readValue(json, EmployeeDto)

    assert str(json) == '{"id":42,"name":"Sherlock Holmes","salary":12345.67,"phone":"+1-555-0100"}'
    assert Objects.equals(dto, decoded)


def test_salary_aggregates_is_introspected():
    assert property_names(SalaryAggregates) == {"min", "max", "sum", "count"}


def test_salary_aggregates_can_be_serialized_and_deserialized(json_mapper):
    aggregates = SalaryAggregates(BigDecimal("1000.50"), BigDecimal("9000.75"), BigDecimal("25000.25"), 7)

    json = json_mapper.writeValueAsString(aggregates)
    decoded = json_mapper.readValue(json, SalaryAggregates)

    assert str(json) == '{"min":1000.50,"max":9000.75,"sum":25000.25,"count":7}'
    assert Objects.equals(aggregates, decoded)


def test_salary_summary_dto_is_introspected():
    assert property_names(SalarySummaryDto) == {"minSalary", "maxSalary", "averageSalary", "employeeCount"}


def test_salary_summary_dto_can_be_serialized_and_deserialized(json_mapper):
    summary = SalarySummaryDto(BigDecimal("1000.50"), BigDecimal("9000.75"), BigDecimal("3571.46"), 7)

    json = json_mapper.writeValueAsString(summary)
    decoded = json_mapper.readValue(json, SalarySummaryDto)

    assert str(json) == '{"minSalary":1000.50,"maxSalary":9000.75,"averageSalary":3571.46,"employeeCount":7}'
    assert Objects.equals(summary, decoded)
