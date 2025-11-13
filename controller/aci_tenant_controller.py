# coding=utf-8

#########################################################################
#  Class that will fetch all global configuration information like      #
#  Tenants, Application Profiles, EPGs, L3Outs, etc. from the fabric. #
#########################################################################

##################
# Import Section #
##################

from typing import Any, Dict, List, Tuple
from parsers.aci_parser import ACITroubleshooterParser
from aci_api_client.getCookie import getCookie
from aci_api_client.Url import UrlClass
from aci_api_client.UserClass import UserClass

###########################
# Private Singleton Class #
###########################

class _PrivateCookie(type):

    _instances: Dict[Any, Any] = {}

    def __call__(cls, *args: Any, **kwargs: Any) -> Any:

        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]

#########################################################################################################
# ACITenantController Class that fetches and processes global configuration data.                       #
#########################################################################################################

class ACITenantController(metaclass=_PrivateCookie):

    def __init__(self) -> None:
        self.parser: ACITroubleshooterParser = ACITroubleshooterParser()

    ##################
    # Public Methods #
    ##################

    # Function that fetches and returns the full tenant subtree data.
    def getFabricTenantConfig(self, main_cookie: getCookie, Urls: UrlClass, User: UserClass) -> Tuple[str, Dict[str, Any]]:

        # Define a single 'root' node name for all fabric-wide configuration data
        fabric_config_node_name = "Fabric_Config_Root"
        fabric_config_attributes: Dict[str, Any] = {'role': 'fabric_config_root'}

        # Fetching Full Tenant Subtree
        try:
            apic_url = Urls.getTenantFullSubtree().replace('https://%s', "https://" + User.base_url)
            AciTenantFullSubtree = main_cookie.get_request(apic_url)
            tenant_data = self.parser.getTenantFullSubtreeInfo(AciTenantFullSubtree)

            if tenant_data:
                # Store the raw, nested tenant configuration subtree
                fabric_config_attributes['tenants'] = tenant_data

        except Exception as e:
            # Handle API/Network errors gracefully
            fabric_config_attributes['error'] = f"Failed to fetch tenant configuration: {e}"
            fabric_config_attributes['tenants'] = []

        # Return the config data as a single node tuple for the NetworkX graph
        return (fabric_config_node_name, fabric_config_attributes)
