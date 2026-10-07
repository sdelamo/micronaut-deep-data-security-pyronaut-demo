"""Micronaut Data entity mapped to the ``hr.employees`` table of the Oracle
Deep Data Security sample schema.

The dataclass is compiled by ``pyronaut process`` into a Java class with the
Micronaut Data metadata. ``decimal.Decimal`` becomes ``java.math.BigDecimal``
and ``Long`` is the JVM ``java.lang.Long``, which keeps the column types of the
Java version of this demo.
"""

from dataclasses import dataclass
from decimal import Decimal
from typing import Annotated

from java.lang import Long
from micronaut.data.annotation import Id, MappedEntity, MappedProperty
from micronaut.serde.annotation import Serdeable


@Serdeable
@MappedEntity(value="employees", schema="hr")
@dataclass
class EmployeeEntity:
    employeeId: Annotated[Long | None, Id, MappedProperty("employee_id")] = None
    firstName: Annotated[str | None, MappedProperty("first_name")] = None
    lastName: Annotated[str | None, MappedProperty("last_name")] = None
    email: str | None = None
    manager: str | None = None
    ssn: str | None = None
    salary: Decimal | None = None
    phone: str | None = None
