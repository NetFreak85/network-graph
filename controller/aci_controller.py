# coding=utf-8

#########################################################################
#  Class that will receive the Cisco ACI Token and will fetch all the   #
#  Nodes and Edge information detected in the fabric                    #
# #######################################################################

##################
# Import Section #
##################

from typing import Any, Dict, Type, List, Tuple, Optional, Union, cast
from parsers.aci_parser import ACITroubleshooterParser
from aci_api_client.getCookie import getCookie
from aci_api_client.Url import UrlClass
from aci_api_client.UserClass import UserClass
from controller.aci_tenant_controller import ACITenantController # NEW IMPORT
import concurrent.futures

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

#########################################################################################################
# ACIController Class that will fetch all information from the Cisco ACI Controllers                    #
# and return the lists of Nodes and Edges Detected in the Fabric                                        #
#########################################################################################################

class ACIController(metaclass=_PrivateCookie):

    def __init__(self) -> None:
        self.parser: ACITroubleshooterParser = ACITroubleshooterParser()
        self.tenant_controller: ACITenantController = ACITenantController() # NEW INITIALIZATION

    ##################
    # Public Methods #
    ##################

    # Function that return a list of nodes from a Cisco ACI Fabric Json var
    def getNodesList(self, main_cookie: getCookie, Urls: UrlClass, User: UserClass) -> Tuple[List[Tuple[str, Dict[str, Any]]], List[Tuple[str, str, Dict[str, Any]]]]:

        # Fetching all the Nodes detected in the Cisco ACI Fabric
        fabricInfo = main_cookie.get_request(Urls.getFabricNumNodesIDs().replace('https://%s',"https://" + User.base_url))

        # List generated from the Cisco ACI Fabric Json Variable
        nodeList: List[Tuple[str, Dict[str, Any]]] = []
        # List generated to return the connections between nods in the Fabric
        edgeList: List[Tuple[str, str, Dict[str, Any]]] = []

        # List that will store all devices connected to our Fabrics
        epgNodeList: List[str] = []
        epgEdgeList: List[Tuple[str, str, Dict[str, Any]]] = []

        # =========================================================================
        # NEW FEATURE: Fetch Global Fabric Configuration (Tenants, EPGs, etc.)
        # =========================================================================

        # Get the global config node and add it to the list
        fabric_config_node = self.tenant_controller.getFabricTenantConfig(main_cookie, Urls, User)
        nodeList.append(fabric_config_node)

        # =========================================================================
        # END OF NEW FEATURE
        # =========================================================================

        # We check if there is information collected from the Fabric
        if int(fabricInfo['totalCount']) > 0:

            # Create a ThreadPoolExecutor to run tasks concurrently
            with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
                # Submit tasks for each node
                future_results = executor.map(lambda node: self._process_node(node, main_cookie, Urls, User), fabricInfo['imdata'])

                # Process results as they become available
                for node_result, edge_result, epgNodeList_result, epgEdgeList_result in future_results:
                    if node_result:
                        nodeList.append(node_result)
                    edgeList.extend(edge_result)
                    epgNodeList.extend(epgNodeList_result)
                    epgEdgeList.extend(epgEdgeList_result)

        # Correcting the bug: Convert epgNodeList to a list of tuples before extending nodeList
        epgNodeList_formatted: List[Tuple[str, Dict[str, Any]]] = [(node, {}) for node in epgNodeList]
        nodeList.extend(epgNodeList_formatted)

        # Extending List edgeList with the connection between Fabric Switch Node and Endpoint Device
        edgeList.extend(epgEdgeList)

        # Returning list
        return nodeList, edgeList

    ####################
    # Privates Methods #
    ####################

    # Function that contains the logic for a single node, now passed to the executor
    def _process_node(self, node: Dict[str, Any], main_cookie: getCookie, Urls: UrlClass, User: UserClass) -> Tuple[Optional[Tuple[str, Dict[str, Any]]], List[Tuple[str, str, Dict[str, Any]]], List[str], List[Tuple[str, str, Dict[str, Any]]]]:

        # List generated from the Cisco ACI Fabric Json Variable
        node_result = None

        # List generated to return the connections between nodes in the Fabric
        edge_result: List[Tuple[str, str, Dict[str, Any]]] = []

        # List that will store all devices connected to our Fabrics
        epgNodeList: List[str] = []
        epgEdgeList: List[Tuple[str, str, Dict[str, Any]]] = []

        # Auxilear Tuples for Resources feching depending on device role
        switch_role = {'leaf', 'spine'}

        # Attributes saved in the variable for simplicity
        attributes = node['fabricNode']['attributes']

        # Node Name in the Graph
        # Ensure nodeName is explicitly a str immediately
        nodeName: str = str(attributes['name'])

        # Eliminating unnecesary attributes
        attributes_node = attributes.copy()
        attributes_node.pop('name', None)
        attributes_node.pop('dn', None)
        attributes_node.pop('lastStateModTs', None)
        attributes_node.pop('lcOwn', None)
        attributes_node.pop('modTs', None)
        attributes_node.pop('monPolDn', None)
        attributes_node.pop('nodeType', None)
        attributes_node.pop('uid', None)
        attributes_node.pop('delayedHeartbeat', None)

        # If the node role is 'leaf' or 'spine' we fecth the following info from then:
        #   - PSU Info
        #   - Linecards
        #   - System Controllers (Only Spine Switches)
        #   - Fabric Modules (Only Spine Switches)
        #   - Supervisors
        #   - Filesystem
        if attributes_node.get('role') in switch_role:

            # Using a nested thread pool for interface-related fetches
            with concurrent.futures.ThreadPoolExecutor(max_workers=5) as sub_executor:

                # All I/O-bound requests for a single node are now inside this function
                # and will be executed in parallel by the thread pool.

                #######################
                #     Power Supply    #
                #######################
                SwitchPsuInfo = main_cookie.get_request(Urls.getApicPowerSupply().replace('https://%s',"https://" + User.base_url).replace('node-%s', 'node-' + attributes_node.get('id')))
                if int(SwitchPsuInfo.get('totalCount')) > 0:
                    attributes_node['psus'] = self.parser.getSwitchPsuInfo(SwitchPsuInfo)
                else:
                    attributes_node['psus'] = []

                #######################
                #     Supervisor      #
                #######################
                SwitchSupInfo = main_cookie.get_request(Urls.getChassisSuppervisor().replace('https://%s',"https://" + User.base_url).replace('node-%s', 'node-' + attributes_node.get('id')))
                if int(SwitchSupInfo.get('totalCount')) > 0:
                    attributes_node['supervisors'] = self.parser.getSwitchSupInfo(SwitchSupInfo)
                else:
                    attributes_node['supervisors'] = []

                ####################
                #    Linecards     #
                ####################
                SwitchLinecardInfo = main_cookie.get_request(Urls.getChassisLinecardInfo().replace('https://%s',"https://" + User.base_url).replace('node-%s', 'node-' + attributes_node.get('id')))
                if int(SwitchLinecardInfo.get('totalCount')) > 0:
                    attributes_node['linecard'] = self.parser.getSwitchLinecardInfo(SwitchLinecardInfo)
                else:
                    attributes_node['linecard'] = []

                ##########################
                #     Interface info     #
                ##########################
                SwitchInterfaceInfo = main_cookie.get_request(Urls.getChassisInterfaceBriefStatus().replace('https://%s',"https://" + User.base_url).replace('node-%s', 'node-' + attributes_node.get('id')))
                if int(SwitchInterfaceInfo.get('totalCount')) > 0:
                    attributes_node['interfaces'], fabricAuxInterfaceVar, DownlinkAuxInterfaceVar = self.parser.getSwitchIntInfo(SwitchInterfaceInfo)

                    # Handling Downlink Endpoints
                    for downlink in DownlinkAuxInterfaceVar:
                        portStatus = main_cookie.get_request(Urls.getChassisInterfaceOperationalStatus().replace('https://%s',"https://" + User.base_url).replace('node-%s', 'node-' + attributes_node.get('id')).replace('eth%s/%s', downlink.get('id').lower() ))
                        # Check if the port is 'up' and has a 'descr' attribute
                        if int(portStatus.get('totalCount')) > 0:
                            portOperAttributes = portStatus['imdata'][0]['ethpmPhysIf']['attributes']
                            if portOperAttributes.get('operSt') == "up" and downlink.get('descr'):
                                # Retrieve optional description
                                deviceDesc_opt = downlink.get('descr')
                                # Ensure deviceDesc_raw is a string by casting anything retrieved and stripping it
                                deviceDesc_raw: str = str(deviceDesc_opt).strip() if deviceDesc_opt is not None else ""

                                # Clean up any remaining extra characters from the device description
                                final_deviceDesc: str = deviceDesc_raw.split('-')[0]

                                # Only proceed if the resulting deviceDesc is not empty
                                if final_deviceDesc:
                                    # Defining Downlink Attribute
                                    auxDeviceDictAttribute = {
                                        'downlink'      : True,
                                        'leaf'          : attributes_node.get('id'),
                                        'leaf_int'      : downlink.get('id').lower(),
                                        'allowedVlans'  : portOperAttributes.get('portStatus', 'N/A'),
                                        'operVlans'     : portOperAttributes.get('operVlans', 'N/A'),
                                        'backplaneMac'  : portOperAttributes.get('backplaneMac', 'N/A'),
                                        'lastLinkStChg' : portOperAttributes.get('lastLinkStChg', 'N/A'),
                                        'operMode'      : portOperAttributes.get('operMode', 'N/A'),
                                        'operSpeed'     : portOperAttributes.get('operSpeed', 'N/A'),
                                        'operSt'        : portOperAttributes.get('operSt', 'N/A')
                                    }

                                    # Fix for controller/aci_controller.py:225: error: Argument 1 to "append" of "list" has incompatible type
                                    # Since nodeName is now explicitly str, we only need to assure the derived name is str.
                                    # We use the variable with the guaranteed type 'final_deviceDesc'

                                    # Using cast to explicitly confirm the type for MyPy (Fix for previous error at line 225)
                                    new_epg_edge = cast(
                                        Tuple[str, str, Dict[str, Any]],
                                        (nodeName, final_deviceDesc, auxDeviceDictAttribute)
                                    )

                                    if new_epg_edge not in epgEdgeList:
                                        epgEdgeList.append(new_epg_edge)

                    # New lists for storing interface data
                    sfpList: List[Dict[str, Any]] = []
                    optIntList: List[Dict[str, Union[str, Dict[str, Any]]]] = []

                    # Map LLDP neighbor fetching for fabric interfaces
                    neighbor_futures = [sub_executor.submit(self._get_lldp_neighbor_info, main_cookie, Urls, User, attributes_node.get('id'), fabricInt) for fabricInt in fabricAuxInterfaceVar]
                    for future in concurrent.futures.as_completed(neighbor_futures):
                        try:
                            neighbor_name, source_int_oper, dest_int_oper, source_int_counter, dest_int_counter = future.result()
                            if neighbor_name is not None:
                                # **START OF FIX FOR LINE 232**
                                # Extract sysName and ensure it is a string (defaulting to empty string if missing)
                                # The explicit casting here resolves the mypy error.
                                sys_name: str = str(neighbor_name.get('sysName', ''))

                                new_edge = cast(
                                    Tuple[str, str, Dict[str, Any]],
                                    (
                                        nodeName,
                                        sys_name,
                                        {
                                            'source_interface_speed'             : neighbor_name.get('source_int_speed'),
                                            'source_interface_id'                : neighbor_name.get('destInt'),
                                            'source_interface_mtu'               : neighbor_name.get('source_int_mtu'),
                                            'source_interface_adminSt'           : neighbor_name.get('source_int_adminSt'),
                                            'source_interface_mode'              : neighbor_name.get('source_int_mode'),
                                            'source_interface_operSt'            : source_int_oper.get('operSt') if source_int_oper else None,
                                            'source_interface_operAllowedVlans'  : source_int_oper.get('allowedVlans') if source_int_oper else None,
                                            'source_interface_operLastErrors'    : source_int_oper.get('lastErrors') if source_int_oper else None,
                                            'source_interface_operLastLinkStChg' : source_int_oper.get('lastLinkStChg') if source_int_oper else None,
                                            'source_interface_operOperDuplex'    : source_int_oper.get('operDuplex') if source_int_oper else None,
                                            'source_interface_operOperMode'      : source_int_oper.get('operMode') if source_int_oper else None,
                                            'source_interface_operSpeed'         : source_int_oper.get('operSpeed') if source_int_oper else None,
                                            'source_broadcastPkts'               : source_int_counter.get('broadcastPkts') if source_int_counter else None,
                                            'source_cRCAlignErrors'              : source_int_counter.get('cRCAlignErrors') if source_int_counter else None,
                                            'source_collisions'                  : source_int_counter.get('collisions') if source_int_counter else None,
                                            'source_dropEvents'                  : source_int_counter.get('dropEvents') if source_int_counter else None,
                                            'source_fragments'                   : source_int_counter.get('fragments') if source_int_counter else None,
                                            'source_jabbers'                     : source_int_counter.get('jabbers') if source_int_counter else None,
                                            'source_multicastPkts'               : source_int_counter.get('multicastPkts') if source_int_counter else None,
                                            'source_oversizePkts'                : source_int_counter.get('oversizePkts') if source_int_counter else None,
                                            'source_pkts'                          : source_int_counter.get('pkts') if source_int_counter else None,
                                            'source_pkts65to127Octets'           : source_int_counter.get('pkts65to127Octets') if source_int_counter else None,
                                            'source_pkts128to255Octets'          : source_int_counter.get('pkts128to255Octets') if source_int_counter else None,
                                            'source_pkts256to511Octets'          : source_int_counter.get('pkts256to511Octets') if source_int_counter else None,
                                            'source_pkts512to1023Octets'         : source_int_counter.get('pkts512to1023Octets') if source_int_counter else None,
                                            'source_pkts1024to1518Octets'        : source_int_counter.get('pkts1024to1518Octets') if source_int_counter else None,
                                            'source_octets'                      : source_int_counter.get('octets') if source_int_counter else None,
                                            'source_pkts64Octets'                : source_int_counter.get('pkts64Octets') if source_int_counter else None,
                                            'source_rXNoErrors'                  : source_int_counter.get('rXNoErrors') if source_int_counter else None,
                                            'source_rxGiantPkts'                 : source_int_counter.get('rxGiantPkts') if source_int_counter else None,
                                            'source_rxOversizePkts'              : source_int_counter.get('rxOversizePkts') if source_int_counter else None,
                                            'source_tXNoErrors'                  : source_int_counter.get('tXNoErrors') if source_int_counter else None,
                                            'source_txGiantPkts'                 : source_int_counter.get('txGiantPkts') if source_int_counter else None,
                                            'source_txOversizePkts'              : source_int_counter.get('txOversizePkts') if source_int_counter else None,
                                            'source_undersizePkts'               : source_int_counter.get('undersizePkts') if source_int_counter else None,
                                            'dest_interface_id'                  : neighbor_name.get('source_int_id'),
                                            'dest_interface_speed'               : dest_int_oper.get('operSpeed') if dest_int_oper else None,
                                            'dest_interface_mtu'                 : neighbor_name.get('dest_int_mtu'),
                                            'dest_interface_admingSt'            : neighbor_name.get('dest_int_adminSt'),
                                            'dest_interface_mode'                : neighbor_name.get('dest_int_mode'),
                                            'dest_interface_operSt'              : dest_int_oper.get('operSt') if dest_int_oper else None,
                                            'dest_interface_operAllowedVlans'    : dest_int_oper.get('allowedVlans') if dest_int_oper else None,
                                            'dest_interface_operLastErrors'      : dest_int_oper.get('lastErrors') if dest_int_oper else None,
                                            'dest_interface_operLastLinkStChg'   : dest_int_oper.get('lastLinkStChg') if dest_int_oper else None,
                                            'dest_interface_operOperDuplex'      : dest_int_oper.get('operDuplex') if dest_int_oper else None,
                                            'dest_interface_operOperMode'        : dest_int_oper.get('operMode') if dest_int_oper else None,
                                            'dest_interface_operSpeed'           : dest_int_oper.get('operSpeed') if dest_int_oper else None,
                                            'dest_broadcastPkts'                 : dest_int_counter.get('broadcastPkts') if dest_int_counter else None,
                                            'dest_cRCAlignErrors'                : dest_int_counter.get('cRCAlignErrors') if dest_int_counter else None,
                                            'dest_collisions'                    : dest_int_counter.get('collisions') if dest_int_counter else None,
                                            'dest_dropEvents'                    : dest_int_counter.get('dropEvents') if dest_int_counter else None,
                                            'dest_fragments'                     : dest_int_counter.get('fragments') if dest_int_counter else None,
                                            'dest_jabbers'                       : dest_int_counter.get('jabbers') if dest_int_counter else None,
                                            'dest_multicastPkts'                 : dest_int_counter.get('multicastPkts') if dest_int_counter else None,
                                            'dest_oversizePkts'                  : dest_int_counter.get('oversizePkts') if dest_int_counter else None,
                                            'dest_pkts'                          : dest_int_counter.get('pkts') if dest_int_counter else None,
                                            'dest_pkts65to127Octets'             : dest_int_counter.get('pkts65to127Octets') if dest_int_counter else None,
                                            'dest_pkts128to255Octets'            : dest_int_counter.get('pkts128to255Octets') if dest_int_counter else None,
                                            'dest_pkts256to511Octets'            : dest_int_counter.get('pkts256to511Octets') if dest_int_counter else None,
                                            'dest_pkts512to1023Octets'           : dest_int_counter.get('pkts512to1023Octets') if dest_int_counter else None,
                                            'dest_pkts1024to1518Octets'          : dest_int_counter.get('pkts1024to1518Octets') if dest_int_counter else None,
                                            'dest_octets'                        : dest_int_counter.get('octets') if dest_int_counter else None,
                                            'dest_pkts64Octets'                  : dest_int_counter.get('pkts64Octets') if dest_int_counter else None,
                                            'dest_rXNoErrors'                    : dest_int_counter.get('rXNoErrors') if dest_int_counter else None,
                                            'dest_rxGiantPkts'                   : dest_int_counter.get('rxGiantPkts') if dest_int_counter else None,
                                            'dest_rxOversizePkts'                : dest_int_counter.get('rxOversizePkts') if dest_int_counter else None,
                                            'dest_tXNoErrors'                    : dest_int_counter.get('tXNoErrors') if dest_int_counter else None,
                                            'dest_txGiantPkts'                   : dest_int_counter.get('txGiantPkts') if dest_int_counter else None,
                                            'dest_txOversizePkts'                : dest_int_counter.get('txOversizePkts') if dest_int_counter else None,
                                            'dest_undersizePkts'                 : dest_int_counter.get('undersizePkts') if dest_int_counter else None
                                        }
                                    )
                                )
                                edge_result.append(new_edge)
                                # **END OF FIX FOR LINE 232**
                        except Exception as e:
                            print(f"Error processing LLDP neighbor for node {nodeName}: {e}")

                    # 2 different threads for each feature, one detect the operational status
                    # The other one check the SFP Status
                    oper_futures = [sub_executor.submit(self._get_operational_info, main_cookie, Urls, User, attributes_node.get('id'), i) for i in (DownlinkAuxInterfaceVar + fabricAuxInterfaceVar)]
                    sfp_futures = [sub_executor.submit(self._get_sfp_info, main_cookie, Urls, User, attributes_node.get('id'), i) for i in (DownlinkAuxInterfaceVar + fabricAuxInterfaceVar)]

                    for oper_future in concurrent.futures.as_completed(oper_futures):
                        try:
                            int_info = oper_future.result()
                            if int_info:
                                optIntList.append(int_info)
                        except Exception as e:
                            print(f"Error processing operational info for node {nodeName}: {e}")

                    for sfp_future in concurrent.futures.as_completed(sfp_futures):
                        try:
                            sfp_info = sfp_future.result()
                            # Only append if a valid SFP object is returned
                            if sfp_info:
                                # Ensure sfp_info is a list before extending
                                if isinstance(sfp_info, list):
                                    sfpList.extend(sfp_info)
                                else:
                                    sfpList.append(sfp_info)
                        except Exception as e:
                            print(f"Error processing SFP info for node {nodeName}: {e}")

                    # Store the collected SFP data in the attributes_node dictionary
                    if sfpList:
                        sfpList.sort(key=lambda x: x['int_id'])
                        attributes_node['sfp'] = sfpList
                    else:
                        attributes_node['sfp'] = []

                    if optIntList:
                        optIntList.sort(key=lambda x: str(x['intID']))
                        attributes_node['opt_interfaces'] = optIntList
                else:
                    attributes_node['interfaces'] = []
                    attributes_node['opt_interfaces'] = []
                    attributes_node['sfp'] = []

            ###################
            #     Faults      #
            ###################
            SwitchFaultsInfo = main_cookie.get_request(Urls.getChassisNodeFault().replace('https://%s',"https://" + User.base_url).replace('node-%s', 'node-' + attributes_node.get('id')))
            if int(SwitchFaultsInfo.get('totalCount')) > 0:
                attributes_node['faults'] = self.parser.getSwitchFaultsInfo(SwitchFaultsInfo)
            else:
                attributes_node['faults'] = []

            ######################
            #    File System     #
            ######################
            SwitchFileSystemInfo = main_cookie.get_request(Urls.getFileSystemInfo().replace('https://%s',"https://" + User.base_url).replace('node-%s', 'node-' + attributes_node.get('id')))
            if int(SwitchFileSystemInfo.get('totalCount')) > 0:
                attributes_node['filesystem'] = self.parser.getSwitchFileSystemInfo(SwitchFileSystemInfo)
            else:
                attributes_node['faults'] = []

            ###############################
            #    Spine Hardware Modules   #
            ###############################

            if attributes_node.get('role') == "spine":

                #######################
                #    Fabric Modules   #
                #######################
                SpineSwitchFabricModuleInfo = main_cookie.get_request(Urls.getChassisFabricModule().replace('https://%s',"https://" + User.base_url).replace('node-%s', 'node-' + attributes_node.get('id')))
                if int(SpineSwitchFabricModuleInfo['totalCount']) > 0:
                    attributes_node['fabric_modules'] = self.parser.getSwitchFabricModuleInfo(SpineSwitchFabricModuleInfo)
                else:
                    attributes_node['fabric_modules'] = []

                ##################################
                #    System Controller Modules   #
                ##################################
                SpineSwitchSystemControllerInfo = main_cookie.get_request(Urls.getChassisSystemController().replace('https://%s',"https://" + User.base_url).replace('node-%s', 'node-' + attributes_node.get('id')))
                if int(SpineSwitchSystemControllerInfo['totalCount']) > 0:
                    attributes_node['system_controller'] = self.parser.getSwitchFabricSystemControllerInfo(SpineSwitchSystemControllerInfo)
                else:
                    attributes_node['system_controller'] = []

        # If the device role is apic, we will retrieve the following information
        #   - Power Supply
        #   - DIMMs
        #   - FANs
        #   - Filesystem
        #   - Physical Interfaces
        #   - Aggregate Interfaces
        else:
            #######################
            #   APIC NTP Server   #
            #######################
            ApicNtpInfo = main_cookie.get_request(Urls.getApicNtp().replace('https://%s',"https://" + User.base_url).replace('node-%s', 'node-' + attributes_node.get('id')))
            if int(ApicNtpInfo.get('totalCount')) > 0:
                attributes_node['apic_ntp'] = self.parser.getApicNtpInfo(ApicNtpInfo)
            else:
                attributes_node['apic_ntp'] = []

            ################################
            #    Apic BBDD Health State    #
            ################################
            ApicBbddHealthState = main_cookie.get_request(Urls.getApicClusterByNode().replace('https://%s',"https://" + User.base_url).replace('node-%s', 'node-' + attributes_node.get('id')))
            if int(ApicBbddHealthState.get('totalCount')) > 0:
                attributes_node['apic_bbdd_sync'] = self.parser.getApicDatabaseStatusInfo(ApicBbddHealthState)
            else:
                attributes_node['apic_bbdd_sync'] = []

            ##########################
            #   APICs Power Supply   #
            ##########################
            ApicPowerSupplyInfo = main_cookie.get_request(Urls.getApicPowerSupply().replace('https://%s',"https://" + User.base_url).replace('node-%s', 'node-' + attributes_node.get('id')))
            if int(ApicPowerSupplyInfo.get('totalCount')) > 0:
                attributes_node['apic_power_supplies'] = self.parser.getApicPowerSupplyInfo(ApicPowerSupplyInfo)
            else:
                attributes_node['apic_power_supplies'] = []

            ###################
            #    APIC FANs    #
            ###################
            ApicFansInfo = main_cookie.get_request(Urls.getApicFan().replace('https://%s',"https://" + User.base_url).replace('node-%s', 'node-' + attributes_node.get('id')))
            if int(ApicFansInfo.get('totalCount')) > 0:
                attributes_node['apic_fans'] = self.parser.getApicFansInfo(ApicFansInfo)
            else:
                attributes_node['apic_fans'] = []

            ########################
            #     APIC Sensors     #
            ########################
            ApicSensorInfo = main_cookie.get_request(Urls.getApicSensors().replace('https://%s',"https://" + User.base_url).replace('node-%s', 'node-' + attributes_node.get('id')))
            if int(ApicSensorInfo.get('totalCount')) > 0:
                attributes_node['apic_sensor'] = self.parser.getApicSensorInfo(ApicSensorInfo)
            else:
                attributes_node['apic_sensor'] = []

            #####################
            #     APIC DIMM     #
            #####################
            ApicDimmInfo = main_cookie.get_request(Urls.getApicMemorySlots().replace('https://%s',"https://" + User.base_url).replace('node-%s', 'node-' + attributes_node.get('id')))
            if int(ApicDimmInfo.get('totalCount')) > 0:
                attributes_node['apic_dimm'] = self.parser.getApicDimmInfo(ApicDimmInfo)

            ###########################
            #     APIC FileSystem     #
            ###########################
            ApicFsInfo = main_cookie.get_request(Urls.getApicFileSystem().replace('https://%s',"https://" + User.base_url).replace('node-%s', 'node-' + attributes_node.get('id')))
            if int(ApicFsInfo.get('totalCount')) > 0:
                attributes_node['apic_filesystem'] = self.parser.getApicFileSystemInfo(ApicFsInfo)
            else:
                attributes_node['apic_filesystem'] = []

            ###################################
            #     APIC Physical Interface     #
            ###################################
            ApicPhyIntInfo = main_cookie.get_request(Urls.getApicPhyInterfaces().replace('https://%s',"https://" + User.base_url).replace('node-%s', 'node-' + attributes_node.get('id')))
            if int(ApicPhyIntInfo.get('totalCount')) > 0:
                attributes_node['apic_phyint'] = self.parser.getApicPhyIntInfo(ApicPhyIntInfo)
            else:
                attributes_node['apic_phyint'] = []

            ####################################
            #     APIC Aggregate Interface     #
            ####################################
            ApicAggIntInfo = main_cookie.get_request(Urls.getApicAggregatedInterfaces().replace('https://%s',"https://" + User.base_url).replace('node-%s', 'node-' + attributes_node.get('id')))
            if int(ApicAggIntInfo.get('totalCount')) > 0:
                attributes_node['apic_aggint'] = self.parser.getApicAggyIntInfo(ApicAggIntInfo)
            else:
                attributes_node['apic_aggint'] = []

        node_result = (nodeName, attributes_node)

        return node_result, edge_result, epgNodeList, epgEdgeList

    # Helper function for concurrent LLDP neighbor fetching
    def _get_lldp_neighbor_info(self, main_cookie: getCookie, Urls: UrlClass, User: UserClass, node_id: str, fabricInt: Dict[str, Any]) -> Tuple[Optional[Dict[str, Any]], Optional[Dict[str, Any]], Optional[Dict[str, Any]], Optional[Dict[str, Any]], Optional[Dict[str, Any]]]:
        # Ensure fabric_int_id is a string before concatenation
        fabric_int_id_opt = fabricInt.get('id')
        if fabric_int_id_opt is None:
            return None, None, None, None, None

        fabric_int_id: str = str(fabric_int_id_opt)

        neighbor_name = self.parser.getSwitchLldpNeightborIntInfo(
            main_cookie.get_request(Urls.getProtocolLldpNeighbors().replace('https://%s',"https://" + User.base_url).replace('node-%s', 'node-' + node_id).replace('if-[%s]', 'if-[' + fabric_int_id + "]"))
        )
        if neighbor_name is not None:

            # Helper to safely get and lower the interface ID, providing a default to avoid 'None' errors
            def safe_lower(key: str) -> str:
                return str(neighbor_name.get(key, "")).lower()

            dest_int_id: str = safe_lower('destInt')

            neighbor_interface_status = self.parser.getSwitchSingleIntInfo(
                main_cookie.get_request(Urls.getChassisInterfaceStatus().replace('https://%s',"https://" + User.base_url).replace('node-%s', 'node-' + neighbor_name.get('neighbor_id')).replace('eth%s/%s', dest_int_id))
            )

            source_oper_inter_json = main_cookie.get_request(Urls.getChassisInterfaceOperationalStatus().replace('https://%s',"https://" + User.base_url).replace('node-%s', 'node-' + node_id).replace('eth%s/%s', fabric_int_id.lower()))
            destination_oper_inter_json = main_cookie.get_request(Urls.getChassisInterfaceOperationalStatus().replace('https://%s',"https://" + User.base_url).replace('node-%s', 'node-' + neighbor_name.get('neighbor_id')).replace('eth%s/%s', dest_int_id))
            source_operational_counter_int_json = main_cookie.get_request(Urls.getChassisInterfaceOperationalCounterStatus().replace('https://%s',"https://" + User.base_url).replace('node-%s', 'node-' + node_id).replace('%s', fabric_int_id.lower()))
            dest_operational_counter_int_json = main_cookie.get_request(Urls.getChassisInterfaceOperationalCounterStatus().replace('https://%s',"https://" + User.base_url).replace('node-%s', 'node-' + neighbor_name.get('neighbor_id')).replace('%s', dest_int_id))

            source_oper_inter = self.parser.getSwitchSingleOperationalIntInfo(source_oper_inter_json)
            destination_oper_inter = self.parser.getSwitchSingleOperationalIntInfo(destination_oper_inter_json)
            source_oper_int_counter = self.parser.getSwitchSingleOperationalCounterIntInfo(source_operational_counter_int_json)
            dest_oper_int_counter = self.parser.getSwitchSingleOperationalCounterIntInfo(dest_operational_counter_int_json)

            neighbor_name['source_int_speed'] = str(fabricInt.get('speed', ''))
            neighbor_name['source_int_mtu'] = str(fabricInt.get('mtu', ''))
            neighbor_name['source_int_adminSt'] = str(fabricInt.get('adminSt', ''))
            neighbor_name['source_int_mode'] = str(fabricInt.get('mode', ''))
            neighbor_name['source_int_id'] = fabric_int_id

            if neighbor_interface_status:
                neighbor_name['dest_int_mtu'] = neighbor_interface_status.get('mtu')
                neighbor_name['dest_int_adminSt'] = neighbor_interface_status.get('adminSt')
                neighbor_name['dest_int_mode'] = neighbor_interface_status.get('mode')

            return neighbor_name, source_oper_inter, destination_oper_inter, source_oper_int_counter, dest_oper_int_counter
        return None, None, None, None, None

    # New Helper function for concurrent operational status fetching
    def _get_operational_info(self, main_cookie: getCookie, Urls: UrlClass, User: UserClass, node_id: str, interface_info: Dict[str, Any]) -> Optional[Dict[str, Union[str, Dict[str, Any]]]]:
        int_id_opt = interface_info.get('id')
        if int_id_opt is None:
             return None

        int_id: str = str(int_id_opt)

        if int_id != "":
            port_status = main_cookie.get_request(Urls.getChassisInterfaceOperationalStatus().replace('https://%s',"https://" + User.base_url).replace('node-%s', 'node-' + node_id).replace('eth%s/%s', int_id.lower()))
            return {'nodeID': node_id, 'intID': int_id.lower(), 'operSt': self.parser.getSwitchSingleOperationalIntInfo(port_status)}
        return None

    # New Helper function for concurrent SFP info fetching
    def _get_sfp_info(self, main_cookie: getCookie, Urls: UrlClass, User: UserClass, node_id: str, interface_info: Dict[str, Any]) -> Optional[Union[Dict[str, Any], List[Dict[str, Any]]]]:
        int_id_opt = interface_info.get('id')
        if int_id_opt is None:
            return None

        int_id: str = str(int_id_opt)

        if int_id != "":
            sfp_port_info_json = main_cookie.get_request(Urls.getChassisInterfaceSfp().replace('https://%s',"https://" + User.base_url).replace('node-%s', 'node-' + node_id).replace('eth%s/%s', int_id.lower()))
            sfp_port_tuple = self.parser.getSwitchSfpInfo(sfp_port_info_json, int_id.lower())
            if sfp_port_tuple:
                return sfp_port_tuple
        return None
