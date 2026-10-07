"""Micronaut Data JDBC repository for ``hr.employees``.

``getSalaryAggregates`` is the privilege-escalation example of the demo: the
query runs with the ``COMPENSATION_ANALYST`` data role enabled, whoever the
signed-in user is. ``@RunAs`` adds the ``ORACLE_DATA_ROLE_COMPENSATION_ANALYST``
role to the current authentication for the duration of the call, and the
Micronaut Security OJDBC extension turns every role carrying the
``ORACLE_DATA_ROLE_`` prefix into an Oracle ``DATA ROLE`` in the End User
Security Context it hands to Oracle JDBC.
"""

from typing import Protocol

from java.lang import Long
from micronaut.data.annotation import Query
from micronaut.data.jdbc.annotation import JdbcRepository
from micronaut.data.model.query.builder.sql import Dialect
from micronaut.data.repository import CrudRepository
from micronaut.security.annotation import RunAs

from .domain import EmployeeEntity
from .dto import SalaryAggregates


@JdbcRepository(dialect=Dialect.ORACLE)
class EmployeeRepository(CrudRepository[EmployeeEntity, Long], Protocol):

    @RunAs("ORACLE_DATA_ROLE_COMPENSATION_ANALYST")
    @Query("SELECT MIN(salary) AS min, MAX(salary) AS max, SUM(salary) AS sum, COUNT(*) AS count FROM hr.employees")
    def getSalaryAggregates(self) -> SalaryAggregates: ...
