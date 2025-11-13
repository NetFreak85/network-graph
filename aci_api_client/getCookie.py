# coding=utf-8

#################################################################################
#  Class that will provide all the information related to the Cisco ACI Cookie  #
#################################################################################

##################
# Import Section #
##################

import requests
import urllib3
import requests
import json
from datetime import datetime
from datetime import timedelta
from typing import Any, Dict, Type, Union, cast

# Disabling the Restconf warnings 
urllib3.disable_warnings()

###########################
# Private Singleton Class #
###########################

class _PrivateCookie(type):

    _instances: Dict[Type[Any], Any] = {}

    def __call__(cls, *args, **kwargs):

        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]

class getCookie(metaclass=_PrivateCookie):

    def __init__( self, username, password, base_url, token_url):
        self.__username = username
        self.__password = password
        self.__base_url = base_url
        self.__token_url = token_url
        self.__cookie = None
        self.__last_login = None
        self.__refresh_timeout = None
        self.__getToken()

    ###############
    # Get Methods #
    ###############

    # Return the URL/IP Address of the APIC management address
    def getBaseUrl(self):
        return self.__base_url

    # Return the Cookie
    def getCookie(self):

        # We check if the token need to be refreshed
        if self.__aaaRefresh():
            self.__cookie = self.__getToken()

        # returning cookie
        return self.__cookie

    # Method to request tokens to the Cisco APICs
    def __getToken(self):
        try:
            # URL that help with the token generation
            url = self.__token_url % self.__base_url

            # Payload
            payload = {
                "aaaUser":
                {
                    "attributes":
                    {
                        "name": self.__username,
                        "pwd": self.__password
                    }
                }
            }

            # Post Method to retrieve the token from APICs
            session = self._handle_request(url, request_type="post", data=payload)

            # If Username or password are incorrect the script stop with exit code 1
            if session.status_code != 200:
                print ("ERROR: Username/Password incorrect")
                exit(1)

            # We save the cookie value, current date for the last login and the refresh timer
            self.__cookie = session.cookies
            self.__last_login = datetime.now()
            self.__refresh_timeout = int(session.json()["imdata"][0]["aaaLogin"]["attributes"]["refreshTimeoutSeconds"])

            # We return the cookie
            return self.__cookie

        # Exception in case of problems with timeout or connection error
        except requests.exceptions.Timeout:
            return 1
        except requests.exceptions.ConnectionError:
            raise Exception("Connection error can't logging to APIC %s with user %s" % (self.__base_url, self.__username))

    # Restconf Request to ACI APIC
    def _handle_request(self, url: str, params: Union[Dict[Any, Any], None] = None, request_type: str = "get", data: Union[Dict[Any, Any], None] = None) -> object:
        try:
            resp = requests.request(
                    method=request_type,
                    url=url,
                    cookies=cast(requests.cookies.RequestsCookieJar, self.__cookie),
                    params=params,
                    verify=False,
                    json=data,
                    timeout=30,
                    )

        # Exception in case of invalid base url
        except requests.exceptions.RequestException as error:
            print("Error occurred communicating with {self.base_uri}:\n{error}")

        # Returning restconf object
        return resp

    # Method that refresh the token from the Cisco APICs
    def __aaaRefresh(self):

        # Private method to check if the login token needs refreshed. Returns True if login needs refresh.
        if not self.__last_login:
            return True

        # if time diff b/w now and last login greater than refresh_timeout then refresh login
        if datetime.now() - self.__last_login >= timedelta(seconds=self.__refresh_timeout) * 0.9:
            return True

        return False

    # Method that logout the token session in the Cisco APIC
    def aaaLogout(self):
        try:

            # URL for the Token session logout
            Logout = "https://%s/api/aaaLogout.json" % self.__base_url

            # Logout Token session body
            LogoutBody = '<aaaUser name="%s" />' % self.__username

            # Logout Token session 
            requests.post(Logout, data=LogoutBody,verify=False, timeout=8)

        except requests.exceptions.Timeout:
            return 1
        except requests.exceptions.ConnectionError:
            raise Exception("Error with logout in APIC %s" % (self.__base_url))

    # Method that will help the sub class to retrieve the information from APICs in JSON format
    def get_request(self, url):

        # We check if the token need to be refreshed
        if self.__aaaRefresh():
            self.__cookie = self.__getToken()

        # Making the Get method in the Request Library for Resconf Cisco ACI Query
        responds = requests.get(url, cookies=self.getCookie(), verify=False)
        json_obj = json.loads(responds.content)

        # Return Json object obtained by Cisco ACI
        return json_obj
