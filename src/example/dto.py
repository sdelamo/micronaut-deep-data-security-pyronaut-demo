"""Data transfer objects.

``@Serdeable`` generates the JSON serializer and deserializer for each
dataclass at build time, and ``pyronaut process`` generates the bean
introspection Micronaut Data needs to map a query result onto
``SalaryAggregates``. ``decimal.Decimal`` fields are ``java.math.BigDecimal``
on the JVM side, ``Long`` is ``java.lang.Long``.
"""

from dataclasses import dataclass
from decimal import Decimal

from java.lang import Long
from micronaut.serde.annotation import Serdeable


@Serdeable
@dataclass
class EmployeeDto:
    id: Long
    name: str
    salary: Decimal
    phone: str


@Serdeable
@dataclass
class SalaryAggregates:
    """The row produced by ``EmployeeRepository.getSalaryAggregates``."""

    min: Decimal | None
    max: Decimal | None
    sum: Decimal | None
    count: Long | None


@Serdeable
@dataclass
class SalarySummaryDto:
    minSalary: Decimal | None
    maxSalary: Decimal | None
    averageSalary: Decimal | None
    employeeCount: int
