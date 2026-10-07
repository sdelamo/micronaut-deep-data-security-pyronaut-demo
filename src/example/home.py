"""The home page.

A classless route module mounted at ``/``. The page is open to anonymous
visitors (``IS_ANONYMOUS``): the template shows a sign-in prompt until the
visitor has authenticated with Microsoft Entra ID, after which the Oracle HR
employee data is loaded under that user's identity.

The request is executed on the blocking executor because the datasource calls
block the thread.
"""

from typing import Annotated

from jakarta.inject import Inject
from micronaut.http.annotation import Get
from micronaut.scheduling import TaskExecutors
from micronaut.scheduling.annotation import ExecuteOn
from micronaut.security.annotation import Secured
from micronaut.security.authentication import Authentication
from micronaut.security.rules import SecurityRule
from micronaut.views import View

from .services import EmployeeService

employee_service: Annotated[EmployeeService, Inject]


@Get("/")
@View("home")
@Secured(SecurityRule.IS_ANONYMOUS)
@ExecuteOn(TaskExecutors.BLOCKING)
def index(authentication: Authentication | None) -> dict:
    return employee_service.employee_model(authentication)
