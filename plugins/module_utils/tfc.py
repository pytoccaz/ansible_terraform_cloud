# -*- coding: utf-8 -*-

# Copyright: (c) 2024 Olivier Bernard
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type


try:
    from requests import get, post, patch
    from requests.auth import AuthBase
    from requests.exceptions import HTTPError, RequestException, JSONDecodeError
    HAS_REQUESTS = True
except ImportError:
    HAS_REQUESTS = False

API_URL = "{url}/api/{version}"
URL = "https://app.terraform.io"
VERSION = "v2"


class TfcError(Exception):
    pass


if HAS_REQUESTS:
    class TfcTokenAuth(AuthBase):
        """Attaches HTTP TFC Token Authentication to the given Request object."""

        def __init__(self, token):
            # setup any auth-related data here
            self.token = token

        def __call__(self, r):
            # modify and return the request
            if self.token is not None:
                r.headers['Authorization'] = "Bearer {0}".format(self.token)

            return r


class TfcClient:

    def __init__(self, token: str, url: str = None) -> None:
        if not HAS_REQUESTS:
            raise TfcError('All Tfc modules require python requests library')

        if url is None:
            url = URL

        if not url.lower().startswith(('http:', 'https:')):
            raise TfcError(
                "url '%s' should either start with 'http' or 'https'." % url)

        self.api_url = API_URL.format(url=url, version=VERSION)
        self.token = token
        self.headers = {"Content-Type": "application/vnd.api+json"}

    def do_request(self, func, path: str, params=None, json=None, verify=True, timeout=10):

        if path.startswith(('http:', 'https:')):
            api_url = path
        elif path is not None:
            api_url = self.api_url + path
        else:
            api_url = self.api_url

        auth = TfcTokenAuth(self.token)

        try:
            response = func(api_url, params=params, headers=self.headers,
                            json=json, verify=verify, auth=auth, timeout=timeout)
            response.raise_for_status()
        except HTTPError as e:
            raise TfcError(
                'Status code error from request POST %s: %s' % (api_url, str(e)))
        except RequestException as e:
            raise TfcError('Error trying request POST %s: %s' %
                           (api_url, str(e)))

        try:
            return response.json()
        except JSONDecodeError as e:
            raise TfcError(
                'API returned invalid JSON when trying to POST %s: %s' % (api_url, str(e)))

    def patch(self, path, json=None, verify=True, timeout=10):
        return self.do_request(patch, path, json=json, verify=verify, timeout=timeout)

    def create(self, path, json=None, verify=True, timeout=10):
        return self.do_request(post, path, json=json, verify=verify, timeout=timeout)

    def read(self, path, params=None, verify=True, timeout=10):
        return self.do_request(get, path, params=params, verify=verify, timeout=timeout)
