# Copyright © 2019 Province of British Columbia
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""This manages all of the authentication and authorization service."""
from http import HTTPStatus
from typing import List

from flask import current_app
from flask_jwt_oidc import JwtManager
from requests import Session, exceptions
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry


SYSTEM_ROLE = 'system'
STAFF_ROLE = 'staff'
COLIN_ROLE = 'colin'
PPR_ROLE = 'ppr'
STAFF_ROLE = 'staff'
BASIC_USER = 'basic'
PRO_DATA_USER = 'pro_data'
PUBLIC_USER = 'public_user'
USER_ORGS_PATH = 'users/orgs'


#  def authorized(identifier: str, jwt: JwtManager, action: List[str]) -> bool:
def authorized(identifier: str, jwt: JwtManager) -> bool:  # pylint: disable=too-many-return-statements
    """Verify the user is authorized to submit the request by inspecting the web token.

    The gateway has already verified the JWT with the OIDC service.
    """
    if not jwt:
        return False

    # Could call the auth api here to check the token roles (/api/v1/orgs/{account_id}/authorizations),
    # but JWTManager.validate_roles does the same thing.

    # All users including staff must have the PPR role.
    if not jwt.validate_roles([PPR_ROLE]):
        return False

    # Account ID (idenfifier) is required if not staff.
    if identifier and identifier.strip() != '':
        return True

    if jwt.validate_roles([STAFF_ROLE]):
        return True

#        template_url = current_app.config.get('AUTH_SVC_URL')
#        auth_url = template_url.format(**vars())

#        token = jwt.get_token_auth_header()
#        headers = {'Authorization': 'Bearer ' + token}
#        try:
#            http = Session()
#            retries = Retry(total=5,
#                            backoff_factor=0.1,
#                            status_forcelist=[500, 502, 503, 504])
#            http.mount('http://', HTTPAdapter(max_retries=retries))
#            rv = http.get(url=auth_url, headers=headers)

#           if rv.status_code != HTTPStatus.OK \
#                    or not rv.json().get('roles'):
#                return False

#            if all(elem.lower() in rv.json().get('roles') for elem in action):
#                return True

#        except (exceptions.ConnectionError,  # pylint: disable=broad-except
#                exceptions.Timeout,
#                ValueError,
#                Exception) as err:
#            current_app.logger.error(f'template_url {template_url}, svc:{auth_url}')
#            current_app.logger.error(f'Authorization connection failure for {identifier}, using svc:{auth_url}', err)
#            return False

    return False


def authorized_token(  # pylint: disable=too-many-return-statements
        identifier: str, jwt: JwtManager, action: List[str]) -> bool:
    """Assert that the user is authorized to submit API requests for a particular action."""
    if not action or not identifier or not jwt:
        return False

    # All users including staff must have the PPR role.
    if not jwt.validate_roles([PPR_ROLE]):
        return False

    if jwt.has_one_of_roles([BASIC_USER, PRO_DATA_USER]):

        template_url = current_app.config.get('AUTH_SVC_URL')
        auth_url = template_url.format(**vars())

        token = jwt.get_token_auth_header()
        headers = {'Authorization': 'Bearer ' + token}
        try:
            http = Session()
            retries = Retry(total=5,
                            backoff_factor=0.1,
                            status_forcelist=[500, 502, 503, 504])
            http.mount('http://', HTTPAdapter(max_retries=retries))
            rv = http.get(url=auth_url, headers=headers)

            if rv.status_code != HTTPStatus.OK \
                    or not rv.json().get('roles'):
                return False

            if all(elem.lower() in rv.json().get('roles') for elem in action):
                return True

        except (exceptions.ConnectionError,  # pylint: disable=broad-except
                exceptions.Timeout,
                ValueError,
                Exception) as err:
            current_app.logger.error(f'template_url {template_url}, svc:{auth_url}')
            current_app.logger.error(f'Authorization connection failure for {identifier}, using svc:{auth_url}', err)
            return False

    return False


def user_orgs(token: str) -> dict:
    """Auth API call to get user organizations for the user identified by the token."""
    response = None
    if not token:
        return response

    service_url = current_app.config.get('AUTH_SVC_URL')
    api_url = service_url + '/' if service_url[-1] != '/' else service_url
    api_url += USER_ORGS_PATH

    try:
        headers = {
            'Authorization': 'Bearer ' + token,
            'Content-Type': 'application/json'
        }
        # current_app.logger.debug('Auth get user orgs url=' + url)
        http = Session()
        retries = Retry(total=3,
                        backoff_factor=0.1,
                        status_forcelist=[500, 502, 503, 504])
        http.mount('http://', HTTPAdapter(max_retries=retries))
        ret_val = http.get(url=api_url, headers=headers)
        current_app.logger.debug('Auth get user orgs response status: ' + str(ret_val.status_code))
        # current_app.logger.debug('Auth get user orgs response data:')
        response = ret_val.json()
        # current_app.logger.debug(response)
    except (exceptions.ConnectionError,  # pylint: disable=broad-except
            exceptions.Timeout,
            ValueError,
            Exception) as err:
        current_app.logger.error(f'Authorization connection failure using svc:{api_url}', err)

    return response


def is_staff(jwt: JwtManager) -> bool:  # pylint: disable=too-many-return-statements
    """Return True if the user has the BC Registries staff role."""
    if not jwt:
        return False

    if jwt.validate_roles([STAFF_ROLE]):
        return True

    return False
