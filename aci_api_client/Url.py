############################################
# Class declaration for the URL management #
############################################

##################
# Import Section #
##################

from __future__ import annotations
import yaml
from .UserClass import UserClass
from typing import Any, Dict, Type, cast

###########################
# Private Singleton Class #
###########################

class _PrivateCookie(type):

    _instances: Dict[Type[Any], Any] = {}

    def __call__(cls, *args: Any, **kwargs: Any) -> Any:

        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]

# Class declaration
class UrlClass(metaclass=_PrivateCookie):

    def __init__(self) -> None:
        self.__URLs: Dict[str, Any] = {}
        self.__UserClass: UserClass = UserClass()
        self.__Read_Yaml_File()

    ######################
    # ACI Components URL #
    ######################

    # Returning ACI Spine Component URL
    def getAciComponentSpine(self) -> str:
        return cast(str, self.__URLs['COMPONENTS']['SPINE'])

    # Returning ACI Leaf Component URL
    def getAciComponentLeaf(self) -> str:
        return cast(str, self.__URLs['COMPONENTS']['LEAF'])

    # Returning ACI Controller Component URL
    def getAciComponentController(self) -> str:
        return cast(str, self.__URLs['COMPONENTS']['CONTROLLER'])

    # Returning ACI APIC URL
    def getComponentApic(self) -> str:
        return cast(str, self.__URLs['COMPONENTS']['APIC'])

    ####################
    # APIC Get Methods #
    ####################

    # Returning APIC Clusster Seen by Node URL
    def getApicClusterByNode(self) -> str:
        return cast(str, self.__URLs['URLs']['APIC']['APIC_CLUSTER_AS_SEEN_BY_NODE'])

    # Returning APIC Physical Interfaces URL
    def getApicPhyInterfaces(self) -> str:
        return cast(str, self.__URLs['URLs']['APIC']['APIC_PHYSICAL_INTERFACES'])

    # Returning APIC Aggregated Interfaces URL
    def getApicAggregatedInterfaces(self) -> str:
        return cast(str, self.__URLs['URLs']['APIC']['APIC_AGGREGATED_INTERFACES'])

    # Returning APIC Power Supply URL
    def getApicPowerSupply(self) -> str:
        return cast(str, self.__URLs['URLs']['APIC']['APIC_POWER_SUPPLY'])

    # Returning APIC Power Supply Consume URL
    def getApicPowerSupplyConsume(self) -> str:
        return cast(str, self.__URLs['URLs']['APIC']['APIC_POWER_SUPPLY_CONSUME'])

    # Returning APIC NTP URL
    def getApicNtp(self) -> str:
        return cast(str, self.__URLs['URLs']['APIC']['APIC_NTP'])

    # Returning APIC FAN URL
    def getApicFan(self) -> str:
        return cast(str, self.__URLs['URLs']['APIC']['APIC_FAN'])

    # Returning APIC Sensors
    def getApicSensors(self) -> str:
        return cast(str, self.__URLs['URLs']['APIC']['APIC_SENSORS'])

    # Returning APIC Memory Slots
    def getApicMemorySlots(self) -> str:
        return cast(str, self.__URLs['URLs']['APIC']['APIC_MEMORY_SLOTS'])

    # Returning APIC File System
    def getApicFileSystem(self) -> str:
        return cast(str, self.__URLs['URLs']['APIC']['APIC_FILE_SYSTEM'])

    # Returning APIC Container
    def getApicContainer(self) -> str:
        return cast(str, self.__URLs['URLs']['APIC']['APIC_CONTAINER'])

    # Returning APIC Processes
    def getApicProcesses(self) -> str:
        return cast(str, self.__URLs['URLs']['APIC']['APIC_PROCESSES'])

    # Returning APIC Faults
    def getApicFault(self) -> str:
        return cast(str, self.__URLs['URLs']['CHASSIS']['CHASSIS_INFO']['APIC_FAULTS'])

    # Returning APIC RAMs
    def getApicRam(self) -> str:
        return cast(str, self.__URLs['URLs']['APIC']['APIC_RAM'])

    # Returning APIC CPU
    def getApicCPU(self) -> str:
        return cast(str, self.__URLs['URLs']['APIC']['APIC_CPU'])

    # Returning Fabric Health Status
    def getApicFabricHealth(self) -> str:
        return cast(str, self.__URLs['URLs']['APIC']['APIC_FABRIC_HEALTH'])

    # Returning Fabric License Status
    def getApicLicense(self) -> str:
        return cast(str, self.__URLs['URLs']['APIC']['APIC_LICENSE'])

    ###########################
    # FABRIC INFO Get Methods #
    ###########################

    # Returning Fabric Num Controllers URL
    def getFabricNumControllers(self) -> str:
        return cast(str, self.__URLs['URLs']['FABRIC_INFO']['NUM_CONTROLLERS'])

    # Returning Fabric Num Nodes IDs URLs
    def getFabricNumNodesIDs(self) -> str:
        return cast(str, self.__URLs['URLs']['FABRIC_INFO']['NUM_NODES_PLUS_IDS'])

    # Returning Fabric Name URL
    def getFabricName(self) -> str:
        return cast(str, self.__URLs['URLs']['FABRIC_INFO']['FABRIC_NAME'])

    # Returning Fabric Name Second Option URL
    def getFabricNameSecondOption(self) -> str:
        return cast(str, self.__URLs['URLs']['FABRIC_INFO']['FABRIC_NAME_SECOND_OPTION'])

    ##########################
    # Token INFO Get Methods #
    ##########################

    # Returning Token v4 URL
    def getTokenV4(self) -> str:
        return cast(str, self.__URLs['URLs']['TOKEN_INFO']['TOKEN_4'])

    # Returning Token v5 URL
    def getTokenV5(self) -> str:
        return cast(str, self.__URLs['URLs']['TOKEN_INFO']['TOKEN_5'])

    # Returning Token Token Refresh URL
    def getTokenRefresh(self) -> str:
        return cast(str, self.__URLs['URLs']['TOKEN_INFO']['TOKEN_REFRESH'])

    # Returning Token Logout URL
    def getTokenLogout(self) -> str:
        return cast(str, self.__URLs['URLs']['TOKEN_INFO']['TOKEN_LOGOUT'])

    ############################
    # Chassis INFO Get Methods #
    ############################

    # Returning Chassis Info URL
    def getChassisInfo(self) -> str:
        return cast(str, self.__URLs['URLs']['CHASSIS']['CHASSIS_INFO']['CHASSIS'])

    # Returning Chassis Node Info URL
    def getChassisNodeInfo(self) -> str:
        return cast(str, self.__URLs['URLs']['CHASSIS']['CHASSIS_INFO']['NODE_INFO'])

    # Returning Chassis Node Disk Info URL
    def getChassisNodeDisk(self) -> str:
        return cast(str, self.__URLs['URLs']['CHASSIS']['CHASSIS_INFO']['NODE_DISK_INFO'])

    # Returning Chassis Node Faults  URL
    def getChassisNodeFault(self) -> str:
        return cast(str, self.__URLs['URLs']['CHASSIS']['CHASSIS_INFO']['NODE_FAULTS'])

    # Returning Chassis Power Supply URL
    def getChassisPowerSupply(self) -> str:
        return cast(str, self.__URLs['URLs']['CHASSIS']['POWER_SUPPLY_INFO']['POWER_SUPPLY'])

    # Returning Chassis Power Supply Consume (watts) URL
    def getChassisPowerSupplyProvided(self) -> str:
        return cast(str, self.__URLs['URLs']['CHASSIS']['POWER_SUPPLY_INFO']['POWER_SUPPLY_PROVIDED'])

    # Returning Chassis Supervisor URL
    def getChassisSuppervisor(self) -> str:
        return cast(str, self.__URLs['URLs']['CHASSIS']['SUPERVISOR_INFO']['SUPERVISOR'])

    # Returning Chassis Fabric Module URL
    def getChassisFabricModule(self) -> str:
        return cast(str, self.__URLs['URLs']['CHASSIS']['FABRIC_MODULE_INFO']['FABRIC_MODULE'])

    # Returning Chassis System Controller URL
    def getChassisSystemController(self) -> str:
        return cast(str, self.__URLs['URLs']['CHASSIS']['SYSTEM_CONTROLLER_INFO']['SYSTEM_CONTROLLER'])

    # Returning Chassis Linecard Info URL
    def getChassisLinecardInfo(self) -> str:
        return cast(str, self.__URLs['URLs']['CHASSIS']['LINECARD_INFO']['LINECARDS'])

    # Returning Chassis Linecard Interface Status URL
    def getChassisInterfaceStatus(self) -> str:
        return cast(str, self.__URLs['URLs']['CHASSIS']['LINECARD_INFO']['INTERFACE_STATUS'])

    # Returning Chassis Linecard Interface Operational Status URL
    def getChassisInterfaceOperationalStatus(self) -> str:
        return cast(str, self.__URLs['URLs']['CHASSIS']['LINECARD_INFO']['OPERATIONAL_INTERFACE_STATUS'])

    # Returning Chassis Linecard Interface Operational Counters URL
    def getChassisInterfaceOperationalCounterStatus(self) -> str:
        return cast(str, self.__URLs['URLs']['CHASSIS']['LINECARD_INFO']['OPERATIONAL_INTERFACE_COUNTERS'])

    # Returning Chassis Interface Status from the Leaf
    def getChassisInterfaceBriefStatus(self) -> str:
        return cast(str, self.__URLs['URLs']['CHASSIS']['LINECARD_INFO']['INTERFACE_LEAF_INFO'])

    # Returning Chassis Linecard SFP Details URL
    def getChassisInterfaceSfp(self) -> str:
        return cast(str, self.__URLs['URLs']['CHASSIS']['LINECARD_INFO']['INTERFACE_SFP_DETAILS'])

    # Returning Chassis Linecard Interface EPG Deployed URL
    def getChassisInterfaceEpg(self) -> str:
        return cast(str, self.__URLs['URLs']['CHASSIS']['LINECARD_INFO']['INTERFACE_EPG'])

    # Returning Chassis Interface Loopbacks URL
    def getChassisLoppbackInterfaces(self) -> str:
        return cast(str, self.__URLs['URLs']['CHASSIS']['LINECARD_INFO']['INTERFACE_LOOPBACKS'])

    # Returning Chassis Interface Loopbacks Details URL
    def getChassisLoppbackInterfacesDetails(self) -> str:
        return cast(str, self.__URLs['URLs']['CHASSIS']['LINECARD_INFO']['LOOPBACK_DETAILS'])

    ##########################
    # File System Get Method #
    ##########################

    # Returning File System URL
    def getFileSystemInfo(self) -> str:
        return cast(str, self.__URLs['URLs']['FILE_SYSTEM']['FILE_SYSTEM'])

    #############################
    # Protocols IPv4 Get Method #
    #############################

    # Returning Protocol IPv4 VRF URL
    def getProtocolIPv4Vrf(self) -> str:
        return cast(str, self.__URLs['URLs']['PROTOCOLS']['IPV4_VRF']['IPv4_VRF'])

    # Returning Protocol IPv4 ARP per VRF URL
    def getProtocolIPv4ArpVrf(self) -> str:
        return cast(str, self.__URLs['URLs']['PROTOCOLS']['IPV4_VRF']['IPv4_VRF_ARP'])

    # Returning Protocol IPv4 VRF Routes URL
    def getProtocolIPv4VrfRoutes(self) -> str:
        return cast(str, self.__URLs['URLs']['PROTOCOLS']['IPV4_VRF']['IPv4_VRF_Routes'])

    # Returning Protocol IPv4 VRF Routes Next Hop URL
    def getProtocolIPv4VrfRoutesNextHop(self) -> str:
        return cast(str, self.__URLs['URLs']['PROTOCOLS']['IPV4_VRF']['IPv4_VRF_Routes_NextHop'])

    ############################
    # Protocol CDP Get Methods #
    ############################

    # Returning Protocol CDP Interface Enable URL
    def getProtocolCdpInterfaces(self) -> str:
        return cast(str, self.__URLs['URLs']['PROTOCOLS']['CDP']['CDP_INTERFACE'])

    # Returning Protocol CDP Neighbors Detected URL
    def getProtocolCdpNeighbors(self) -> str:
        return cast(str, self.__URLs['URLs']['PROTOCOLS']['CDP']['CDP_NEIGHBOR'])

    #############################
    # Protocol LLDP Get Methods #
    #############################

    # Returning Protocol LLDP Interface URL
    def getProtocolLldpInterfaces(self) -> str:
        return cast(str, self.__URLs['URLs']['PROTOCOLS']['LLDP']['LLDP_INTERFACE'])

    # Returning Protocol LLDP Neighbors URL
    def getProtocolLldpNeighbors(self) -> str:
        return cast(str, self.__URLs['URLs']['PROTOCOLS']['LLDP']['LLDP_NEIGHBOR'])

    #############################
    # Protocol ISIS Get Methods #
    #############################

    # Returning Protocol ISIS URL
    def getProtocolIsisInfo(self) -> str:
        return cast(str, self.__URLs['URLs']['PROTOCOLS']['ISIS']['ISIS_PROTOCOL'])

    # Returning Protocol ISIS URL
    def getProtocolIsisdTE(self) -> str:
        return cast(str, self.__URLs['URLs']['PROTOCOLS']['ISIS']['ISIS_DTE'])

    # Returning Protocol ISIS DTE Tunnel Information URL
    def getProtocolIsisInterfaces(self) -> str:
        return cast(str, self.__URLs['URLs']['PROTOCOLS']['ISIS']['ISIS_INTERFACES'])

    # Returning Protocol ISIS Neighbors URL
    def getProtocolIsisNeighbors(self) -> str:
        return cast(str, self.__URLs['URLs']['PROTOCOLS']['ISIS']['ISIS_NEIGHBORS'])

    # Returning Protocol ISIS Routes URL
    def getProtocolIsisRoutes(self) -> str:
        return cast(str, self.__URLs['URLs']['PROTOCOLS']['ISIS']['ISIS_ROUTES'])

    #############################
    # Protocol COOP Get Methods #
    #############################

    # Returning Protocol COOP Domain and Adj URL
    def getProtocolCoopDomainAndAdj(self) -> str:
        return cast(str, self.__URLs['URLs']['PROTOCOLS']['COOP']['COOP_DOMAIN_AND_ADJ'])

    # Returning Protocol COOP Domain SPINE URL
    def getProtocolCoopDomainSpine(self) -> str:
        return cast(str, self.__URLs['URLs']['PROTOCOLS']['COOP']['COOP_DOMAIN_SPINE_SWITCH'])

    # Returning Protocol COOP VPC Database URL
    def getProtocolCoopVpcDatabase(self) -> str:
        return cast(str, self.__URLs['URLs']['PROTOCOLS']['COOP']['VPC_DATABASE'])

    # Returning Protocol COOP Node References URL
    def getProtocolCoopNodeReference(self) -> str:
        return cast(str, self.__URLs['URLs']['PROTOCOLS']['COOP']['COOP_VPC_NODE_REF'])

    # Returning Protocol COOP Endpoints Detected URL
    def getProtocolCoopEndpoints(self) -> str:
        return cast(str, self.__URLs['URLs']['PROTOCOLS']['COOP']['COOP_ENDPOINTS'])

    ##############################
    # Protocol RIBv4 Get Methods #
    ##############################

    # Returning Protocol RIBv4 Domains
    def getProtocolRibv4Domains(self) -> str:
        return cast(str, self.__URLs['URLs']['PROTOCOLS']['RIBv4']['RIBv4_DOMAINS'])

    # Returning Protocol RIBv4 Domain Routes
    def getProtocolRibv4DomainRoutes(self) -> str:
        return cast(str, self.__URLs['URLs']['PROTOCOLS']['RIBv4']['RIBv4_ROUTE'])

    # Returning Protocol RIBv4 Route Details
    def getProtocolRibv4DomainRouteDetails(self) -> str:
        return cast(str, self.__URLs['URLs']['PROTOCOLS']['RIBv4']['RIBv4_ROUTE_DETAILS'])

    ######################
    # Tenant Get Methods #
    ######################

    # Returning Tenants deployed URL
    def getTenantsDeployed(self) -> str:
        return cast(str, self.__URLs['URLs']['TENANT']['TENANT_INFO'])

    # Returning Tenant Application Profiles Detected
    def getTenantAP(self) -> str:
        return cast(str, self.__URLs['URLs']['TENANT']['TENANT_AP'])

    # New Method: Returning Full Tenant Subtree URL
    def getTenantFullSubtree(self) -> str:
        return cast(str, self.__URLs['URLs']['TENANT']['TENANT_FULL_SUBTREE'])

    ##################################
    # Private Method that will build #
    ##################################

    # Function that read the Cisco ACI URL for RESCONF querys in YAML file
    def __Read_Yaml_File(self) -> None:
        with open( self.__UserClass.Path + '/aci_api_client/url.yaml' ) as file:
            try:
                self.__URLs = yaml.safe_load(file)
            except yaml.YAMLError as exc:
                exit(print("Error reading from URL.YAML file"))
