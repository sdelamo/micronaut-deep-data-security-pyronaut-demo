"""The home page, rendered by Thymeleaf from the model the route returns."""

import base64

from pyronaut import requests

from basic_auth_provider import PASSWORD

BROWSER_ACCEPT = {"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"}
USERNAME = "emma@supremo.onmicrosoft.com"


def basic_auth(username: str, password: str) -> dict:
    token = base64.b64encode(f"{username}:{password}".encode()).decode()
    return {"Authorization": f"Basic {token}"}


def test_home_page_prompts_anonymous_visitor_to_sign_in(server_context):
    client = requests.with_context(server_context)
    response = client.get("/", headers=BROWSER_ACCEPT)
    assert response.status_code == 200, response.text
    assert "Anonymous" in response.text
    assert "Sign in with Microsoft Entra ID" in response.text
    assert 'href="/oauth/login/entraid"' in response.text


def test_home_page_shows_employees_and_salary_summary_to_signed_in_user(server_context):
    """The signed-in branch renders the Python model: a list of entities from
    the repository and the ``SalarySummaryDto`` dataclass."""
    client = requests.with_context(server_context)
    response = client.get("/", headers={**BROWSER_ACCEPT, **basic_auth(USERNAME, PASSWORD)})
    assert response.status_code == 200, response.text
    page = response.text
    assert f"Signed in as <span class=\"fw-semibold\">{USERNAME}</span>" in page
    assert 'href="/logout"' in page
    # Salary summary cards
    assert "9826.00" in page
    assert "13000" in page
    assert "6900" in page
    # One row per employee
    for first_name in ("Victoria", "Marvin", "Chris", "Emma", "Taylor"):
        assert first_name in page, first_name
    assert "219-09-9999" in page


def test_home_page_rejects_wrong_credentials(server_context):
    client = requests.with_context(server_context)
    response = client.get("/", headers={**BROWSER_ACCEPT, **basic_auth(USERNAME, "wrong")})
    # The page is open to anonymous visitors, so bad credentials fall back to
    # the anonymous rendering rather than a 401.
    assert response.status_code == 200, response.text
    assert "Anonymous" in response.text
