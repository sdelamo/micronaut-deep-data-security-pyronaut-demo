"""Shared pytest fixtures.

Oracle Database Free is started once per session with Testcontainers, driven
from Python against the Java Testcontainers API, exactly as the ``Oracle``
helper of the Java version does. The ``hr`` schema is created by a startup
script copied into the container, and each test context loads the sample
employees with the ``Sql`` phase of the pytest Micronaut fixture.
"""

from contextlib import contextmanager

import java
import pytest
from micronaut.security.authentication import Authentication
from org.testcontainers.oracle import OracleContainer
from org.testcontainers.utility import DockerImageName, MountableFile
from pyronaut.test import MicronautTest, Sql, micronaut_test_fixture

IMAGE_NAME = "gvenzl/oracle-free:23.26.1-faststart"
# The faststart image already has a database, so startup scripts are the
# reliable hook for schema creation.
INIT_SCRIPT = "/container-entrypoint-startdb.d/01-hr-schema.sql"
EMPLOYEES_TEST_DATA = "classpath:employees-test-data.sql"

# Internal to Micronaut Security, so it has no generated stub; loaded by its Java name.
ServerRequestContextSecurityContextSupplier = java.type(
    "io.micronaut.security.context.ServerRequestContextSecurityContextSupplier"
)


@pytest.fixture(scope="session")
def oracle():
    """Oracle Database Free with the ``hr.employees`` table, started once.

    Yields the datasource properties the application needs to reach it.
    """
    # tests-config/ is on the test classpath. Resolving the script there, rather
    # than relative to __file__, works wherever Pyronaut stages the test sources.
    container = OracleContainer(DockerImageName.parse(IMAGE_NAME)).withCopyFileToContainer(
        MountableFile.forClasspathResource("oracle-init.sql"), INIT_SCRIPT
    )
    container.start()
    try:
        yield {
            "datasources.default.url": str(container.getJdbcUrl()),
            "datasources.default.username": str(container.getUsername()),
            "datasources.default.password": str(container.getPassword()),
        }
    finally:
        container.stop()


@pytest.fixture
def application_context(request, oracle):
    """An application context wired to the Oracle container, with the sample
    employees loaded. The HTTP server is not started: these tests call the
    repository and the service directly."""
    fixture = micronaut_test_fixture(
        request,
        MicronautTest(
            environments=["test"],
            start_application=False,
            properties=oracle,
            sql=Sql(EMPLOYEES_TEST_DATA),
        ),
    )
    yield fixture
    fixture.stop()


@pytest.fixture
def server_context(request, oracle):
    """A running application, HTTP server included, for page tests."""
    fixture = micronaut_test_fixture(
        request,
        MicronautTest(
            environments=["test"],
            properties={**oracle, "micronaut.server.port": "-1"},
            sql=Sql(EMPLOYEES_TEST_DATA),
        ),
    )
    yield fixture
    fixture.stop()


@contextmanager
def run_as(username: str):
    """Run the block under an authentication for ``username``.

    The Java tests put ``@RunAs(name = "...")`` on the test class so that the
    repository's ``@RunAs("ORACLE_DATA_ROLE_COMPENSATION_ANALYST")`` has a
    current authentication to add the data role to; without one Micronaut
    Security refuses the call. A pytest function is not an intercepted bean,
    so the same authentication is propagated here by hand, with the propagated
    context the ``@RunAs`` interceptor itself uses.
    """
    propagated = ServerRequestContextSecurityContextSupplier.withAuthentication(Authentication.build(username))
    scope = propagated.propagate()
    try:
        yield
    finally:
        scope.close()
