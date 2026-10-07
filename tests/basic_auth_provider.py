"""A test-only authentication provider.

The application signs users in with Microsoft Entra ID, which is configured in
the ``dev`` environment only. Under ``test`` nothing authenticates, so this bean
lets a page test sign in with HTTP Basic credentials and exercise the signed-in
branch of the home page: Micronaut Security's basic-auth fetcher is enabled by
default and hands the credentials to the provider.

A Python class implementing the Java ``HttpRequestAuthenticationProvider``
interface. It lives in ``tests/``, so it is processed into the test classes
only and never ships with the application.
"""

from jakarta.inject import Singleton
from micronaut.context.annotation import Requires
from micronaut.http import HttpRequest
from micronaut.security.authentication import (
    AuthenticationFailureReason,
    AuthenticationRequest,
    AuthenticationResponse,
)
from micronaut.security.authentication.provider import HttpRequestAuthenticationProvider

PASSWORD = "secret"
USERS = {"emma@supremo.onmicrosoft.com": PASSWORD}


@Singleton
@Requires(env=["test"])
class BasicAuthProvider(HttpRequestAuthenticationProvider):
    def authenticate(
        self, requestContext: HttpRequest, authRequest: AuthenticationRequest
    ) -> AuthenticationResponse:
        identity = str(authRequest.getIdentity())
        if USERS.get(identity) == str(authRequest.getSecret()):
            # Entra ID puts the user's email in the `preferred_username` claim,
            # which the home page shows in the navigation bar.
            return AuthenticationResponse.success(identity, [], {"preferred_username": identity})
        return AuthenticationResponse.failure(AuthenticationFailureReason.CREDENTIALS_DO_NOT_MATCH)
