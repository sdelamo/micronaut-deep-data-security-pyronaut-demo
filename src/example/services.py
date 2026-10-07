"""Builds the model rendered by the home page."""

from decimal import ROUND_HALF_UP, Decimal

from jakarta.inject import Singleton
from micronaut.security.authentication import Authentication

from .dto import SalaryAggregates, SalarySummaryDto
from .repository import EmployeeRepository

CENTS = Decimal("0.01")

@Singleton
class EmployeeService:
    def __init__(self, employee_repository: EmployeeRepository):
        self.employee_repository = employee_repository

    def employee_model(self, authentication: Authentication | None) -> dict:
        """The view model: empty for an anonymous visitor, the employee records
        and the salary summary for a signed-in user."""
        model: dict = {}
        if authentication is not None:
            model["employees"] = self.employee_repository.findAll()
            model["salarySummary"] = salary_summary(self.employee_repository.getSalaryAggregates())
        return model

def salary_summary(aggregates: SalaryAggregates) -> SalarySummaryDto:
    """Average salary to two decimal places, rounding half up, as the Java
    version does with ``BigDecimal.divide(..., 2, RoundingMode.HALF_UP)``."""
    count = aggregates.count
    employee_count = 0 if count is None else int(count)
    average_salary = None
    if aggregates.sum is not None and employee_count > 0:
        average_salary = (Decimal(aggregates.sum) / employee_count).quantize(CENTS, rounding=ROUND_HALF_UP)
    return SalarySummaryDto(
        minSalary=aggregates.min,
        maxSalary=aggregates.max,
        averageSalary=average_salary,
        employeeCount=employee_count,
    )
