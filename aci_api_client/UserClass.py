######################################################
# Class declaration for the user/password management #
######################################################

##################
# Import Section #
##################

import os
from typing import Any, Dict, Type

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

############################
# Public Class declaration #
############################

class UserClass(metaclass=_PrivateCookie):

    def __init__(self):
        self.__user = os.getenv('USER')
        self.__pwd = os.getenv('UserPwd')
        self.__base_url = os.getenv('FabricGtmUrl')
        self.__Fabric_Version = os.getenv('AciVer')
        self.__Path = os.getenv('FabricGraphPath')
        self.__Email_Sender = os.getenv('Email_Sender')
        self.__Email_Token = os.getenv('Email_Token')
        self.__Email_Receiver = os.getenv('Email_Receiver')
        self.__SMTP_SERVER = os.getenv('SMTP_SERVER')
        self.__SMTP_PORT = os.getenv('SMTP_PORT')

    ###########################
    # Get Methods Definitions #
    ###########################

    # Return Access user
    @property
    def user(self):
        return self.__user

    # Return Access Password
    @property
    def pwd(self):
        return self.__pwd

    # Return Access URL
    @property
    def base_url(self):
        return self.__base_url

    # Return Fabric Version
    @property
    def Fabric_Version(self):
        return self.__Fabric_Version

    # Return Script Path
    @property
    def Path(self):
          return self.__Path

    # Return Email Sender
    @property
    def Email_Sender(self):
        return self.__Email_Sender

    # Return Sender Authentication Token
    @property
    def Email_Token(self):
        return self.__Email_Token

    # Return Email Receiver
    @property
    def Email_Receiver(self):
        return self.__Email_Receiver

    # Return SMTP Server
    @property
    def SMTP_SERVER(self):
        return self.__SMTP_SERVER

    # Return Smtp Service Port
    @property
    def SMTP_PORT(self):
        return self.__SMTP_PORT
