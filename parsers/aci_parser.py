# coding=utf-8

################################################################################################
#  Class that will parser all the information collected in the network_graph.py from Cisco ACI #
################################################################################################

##################
# Import Section #
##################

from typing import Any, Dict, Type, List

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

#########################################################################################################
# ACITroubleshooterParser Class that will parse all the json info received from network_graph.py Script #
# returning a list with the information parser                                                          #
#########################################################################################################

class ACITroubleshooterParser(metaclass=_PrivateCookie):

    #
    # Switch Section
    #

    # Method that return the SFP Info from Switch
    def getSwitchSfpInfo(self, sfpJson: Dict[str, Any], int_id: str) -> List[Dict[str, Any]]: # Added type hints for clarity

        # Auxilear List with the SFP info
        sfpList: List[Dict[str, Any]] = []

        # For each SFP detected in the JSON var, we add the info into a list
        for sfp in sfpJson['imdata']:

            # Auxilear Var Attribute 
            attributes = sfp['ethpmFcot']['attributes']

            # Copy Attribute info for Dict Manipulation
            sfp_attribute = attributes.copy()

            # Removing unnecesary info
            sfp_attribute.pop('dn', None)
            sfp_attribute.pop('modTs', None)
            sfp_attribute.pop('monPolDn', None)

            # Adding Interface ID to identify it in the print section
            sfp_attribute['int_id'] = int_id

            # If the switch has a SFP in the interface 'id'
            # the 'actualType' have to be different for 'unknown' (sfp, qsfp, etc.)
            if sfp_attribute.get('actualType') != 'unknown':

                # This ensures the printer has the keys to check later.
                sfp_attribute['temp'] = sfp_attribute.get('temp', 'N/A')
                sfp_attribute['volt'] = sfp_attribute.get('volt', 'N/A')
                sfp_attribute['txPwr'] = sfp_attribute.get('txPwr', 'N/A')
                sfp_attribute['rxPwr'] = sfp_attribute.get('rxPwr', 'N/A')
                sfp_attribute['bias'] = sfp_attribute.get('bias', 'N/A')

                # Adding sfp detail to the list
                sfpList.append(sfp_attribute)

        # Returning List with the SFP Info
        return sfpList

    # Method that return the PSU info from Switches
    def getSwitchPsuInfo(self, psuJson):

        # Auxilear List with the PSU info
        psuList = []

        # For each PSU detected in the JSON var, we add the info into a list
        for psu in psuJson['imdata']:

            # Auxilear Var Attribute 
            attributes = psu['eqptPsu']['attributes']

            # Copy Attribute info for Dict Manipulation
            psu_attribute = attributes.copy()

            # Removing unnecesary info
            psu_attribute.pop('almReg', None)
            psu_attribute.pop('childAction', None)
            psu_attribute.pop('cimcVersion', None)
            psu_attribute.pop('dn', None)
            psu_attribute.pop('mfgTm', None)
            psu_attribute.pop('modTs', None)
            psu_attribute.pop('monPolDn', None)

            # Adding PSU Attributes to the psuList
            psuList.append(psu_attribute)

        # Returning List with PSU Info
        return psuList

    # Method that return the Supervisor info from switches
    def getSwitchSupInfo(self, SupJson):

        # Auxilear List with the PSU info
        SupList = []

        # For each PSU detected in the JSON var, we add the info into a list
        for sup in SupJson['imdata']:

            # Auxilear Var Attribute 
            attributes = sup['eqptSupC']['attributes']

            # Copy Attributes info for Dict Manipulation
            sup_attribute = attributes.copy()

            # Removing unnecesary info
            sup_attribute.pop('childAction', None)
            sup_attribute.pop('cimcVersion', None)
            sup_attribute.pop('dn', None)
            sup_attribute.pop('mfgTm', None)
            sup_attribute.pop('modTs', None)
            sup_attribute.pop('monPolDn', None)

            # Adding Supervisor Attributes to the SupList
            SupList.append(sup_attribute)

        # Returning List with Supervisor Info
        return SupList

    # Method that return the Fabric Modules information from Spine Switches
    def getSwitchFabricModuleInfo(self, FmJson):

        # Auxilear List with the Fabric Module Info
        FmList = []

        # for each Fabric Module in the JSON var, we add the info into a List
        for fm in FmJson['imdata']:

            # Auxilear Var Attributes
            attributes = fm['eqptFC']['attributes']

            # Copy Attributes info for Dict Manipulation
            fm_attributes = attributes.copy()

            #Removing unnecesary info
            fm_attributes.pop('childAction', None)
            fm_attributes.pop('cimcVersion', None)
            fm_attributes.pop('dn', None)
            fm_attributes.pop('mfgTm', None)
            fm_attributes.pop('modTs', None)
            fm_attributes.pop('monPolDn', None)

            # Adding Fabric Module Info to the FmList
            FmList.append(fm_attributes)

        # Returning List with all Fabric Module Info
        return FmList

    # Method that return the Linecard information from Switches
    def getSwitchLinecardInfo(self, linecardJson):

        # Auxilear List with the Linecard Info
        linecardList = []

        # For each Linecard in the JSON var, we add the info into the list
        for lc in linecardJson['imdata']:

            # Auxilear Var Attributes
            attributes = lc['eqptLC']['attributes']

            # Copy Attributes info for Dict Manipulation
            lc_attributes = attributes.copy()

            # Removing unnecesary info
            lc_attributes.pop('childAction', None)
            lc_attributes.pop('cimcVersion', None)
            lc_attributes.pop('dn', None)
            lc_attributes.pop('mfgTm', None)
            lc_attributes.pop('modTs', None)
            lc_attributes.pop('monPolDn', None)

            # # Adding Linecard Info to the lcList
            linecardList.append(lc_attributes)

        # Returning List with all the Linecards Info
        return linecardList

    # Method that return the System Controller information from Spine Switches
    def getSwitchFabricSystemControllerInfo(self, scJson):

        # Auxilear List with the System Controller Info
        SmList = []

        # for each System Controller in the JSON var, we add the info into the List
        for sc in scJson['imdata']:

            # Auxilear Var Attributes
            attributes = sc['eqptSysC']['attributes']

            # Copy Attributes info for Dict Manipulation
            sc_attributes = attributes.copy()

            # Removing unnecesary info
            sc_attributes.pop('childAction', None)
            sc_attributes.pop('cimcVersion', None)
            sc_attributes.pop('dn', None)
            sc_attributes.pop('mfgTm', None)
            sc_attributes.pop('modTs', None)
            sc_attributes.pop('monPolDn', None)

            # Adding System Controllers Info to the SmList
            SmList.append(sc_attributes)

        # Returning List with all the System Controllers Info
        return SmList

    # Method that return the faults detected in the Switches
    def getSwitchFaultsInfo(self, faultsJson):

        # Auxilear List with the faults Info
        switchFaults = []

        # for each fault in the JSON var, we add the info into the List
        for fault in faultsJson['imdata']:

            # Auxilear Var Attributes
            attributes = fault['faultSummary']['attributes']

            # Adding Faults Info to the switchFaults list
            switchFaults.append(attributes)

        # Returning faults info detected in the switch
        return switchFaults

    # Method that return the Filesystem information from the Switches
    def getSwitchFileSystemInfo(self, FileSystemJson):

        # Auxilear List with the Filesystem info
        switchFileSystem = []

        # for each directory detected in the JSON var, we add the info into the List
        for directory in FileSystemJson.get('imdata'):

            # Auxilear Var Attributes
            attributes = directory['eqptcapacityFSPartition']['attributes']

            # Copy Attributes info for Dict Manipulation
            fs_attributes = attributes.copy()

            # Removing unnecesary info
            fs_attributes.pop('dn', None)
            fs_attributes.pop('modTs', None)
            fs_attributes.pop('monPolDn', None)
            fs_attributes.pop('childAction', None)

            # Making calculation for better visual understanding
            fs_utilization = ( 100 * int(fs_attributes.get('used',0)) ) / int(fs_attributes.get('avail') )

            # Transforming fields 'avail' and 'used' from bytes to GB
            fs_attributes['avail_gb'] = round( int(fs_attributes.get('avail', 0)) / (1024 ** 3), 2 )
            fs_attributes['used_gb'] = round(int(fs_attributes.get('used', 0)) / (1024 ** 3), 2)

            # Adding utilization percentage to the fs_attributes
            fs_attributes['used_perc'] = round(fs_utilization,2)

            # Adding FileSystem Info to the switchFileSystem List
            switchFileSystem.append(fs_attributes)

        # Returning FileSystem info detected in the Switch
        return switchFileSystem

    # Method that return the Switch Interface info
    def getSwitchIntInfo(self, swIntJson):

        # Type of downlinks Tuple
        downlinkUsageType = ('epg', 'epg,infra', 'controller', 'infra', 'l3out', 'l2out')

        # Auxilear List with the Physics Interface Info
        swIntList = []

        # Fabric Interfaces List
        swFabricIntList = []

        # Downlink Interfaces List in EPG Mode
        swDownlinkIntList = []

        # For each Interface detected in the JSON var, we add the info into the swIntList list
        for swInt in swIntJson['imdata']:

            # Auxilear Var Attributes
            attributes = swInt['l1PhysIf']['attributes']

            # Copy Attributes info for Dict Manipulation
            swInt_attributes = attributes.copy()

            # Removing unnecesary info
            swInt_attributes.pop('childAction', None)
            swInt_attributes.pop('dn', None)
            swInt_attributes.pop('modTs', None)
            swInt_attributes.pop('monPolDn', None)

            # Adding Physical Interface info to the PhyIntList List
            swIntList.append(swInt_attributes)

            # If the interface is the fabric type, we added in the swFabricIntList List
            if "fabric" in swInt_attributes.get('usage'):

                # Auxilear dictionary
                Auxilear_inter_dict = {
                    'id'        : swInt_attributes.get('id'),
                    'mtu'       : swInt_attributes.get('mtu'),
                    'speed'     : swInt_attributes.get('speed'),
                    'adminSt'   : swInt_attributes.get('adminSt'),
                    'mode'      : swInt_attributes.get('mode'),
                }

                # Adding dictinary to interface
                swFabricIntList.append(Auxilear_inter_dict)

            # Checking if the interface is the type of downlink defined in the Tuple downlinkUsageType
            elif swInt_attributes.get('usage') in downlinkUsageType:

                # Adding Downlink Interfaces to the List
                swDownlinkIntList.append(swInt_attributes)

        # Sorting list based in interface name
        swIntList.sort(key=lambda x: x['id'])

        # Returning Physical Information info detected in the APICs
        return swIntList, swFabricIntList, swDownlinkIntList

    # Method to return the LLDP Neighbor Name
    def getSwitchLldpNeightborIntInfo(self, lldpJson):

        # Auxilear Variable to retrieve the neighbor
        neighbor = None

        # We check if the lldpJson have info inside we retrieve the neghbor name
        if int(lldpJson.get('totalCount')) > 0:

            # We move for the List in the Json file
            for lldpNei in lldpJson['imdata']:

                # Auxilear Var Attributes
                attribute = lldpNei['lldpAdjEp']['attributes']

                # Setting the LLDP Neighbor Name to the neighbor auxilear var
                neighbor =  {
                    'sysName'     : attribute.get('sysName',""),
                    'neighbor_id' : attribute.get('sysDesc').split("node-")[1],
                    'destInt'     : attribute.get('portIdV',"")
                    }

        return neighbor

    # Method to return the interface Admin Status for a single interface
    def getSwitchSingleIntInfo(self, intJson):

        # Auxilear var with Adming Interface Info
        interface = {}

        # We check if the intJson variable have info inside or not
        if int(intJson.get('totalCount')) > 0:

            # For each element in the list 'imdata', we scan the interface info
            for inter in intJson.get('imdata'):

                # Auxilear Var Attribute
                attribute = inter['l1PhysIf']['attributes']

                # Adding attributes from Json var to interface dict
                interface['adminSt'] = attribute.get('adminSt')
                interface['mtu']     = attribute.get('mtu')
                interface['speed']   = attribute.get('speed')
                interface['mode']    = attribute.get('mode')

        # Returning Interface Dict with interface info
        return interface

    # Method to return the interface Operational Status for a single interface
    def getSwitchSingleOperationalIntInfo(self, operJson):

        # Auxilear var with Operational Interface Info
        Interface = {}

        # We check if the intJson variable have info inside or not
        if int(operJson.get('totalCount')) > 0:

            # For each element in the list 'imdata', we scan the interface info
            for operInt in operJson.get('imdata'):

                # Auxilear Var Attribute
                attribute = operInt['ethpmPhysIf']['attributes']

                # Adding attributes from Json var to interface dict
                Interface['accessVlan']    = attribute['accessVlan']
                Interface['allowedVlans']  = attribute['allowedVlans']
                Interface['lastErrors']    = attribute['lastErrors']
                Interface['lastLinkStChg'] = attribute['lastLinkStChg']
                Interface['operDuplex']    = attribute['operDuplex']
                Interface['operMode']      = attribute['operMode']
                Interface['operSpeed']     = attribute['operSpeed']
                Interface['operSt']        = attribute['operSt']

        # Returning Dict with Operational Status
        return Interface

    # Method to return the interface Operational Status for a single interface
    def getSwitchSingleOperationalCounterIntInfo(self, operCounterJson):

        # Auxilear var with Operational Counters of the Interface 
        Interface = {}

        # We check if the intJson variable have info inside or not
        if int(operCounterJson.get('totalCount')) > 0:

            # For each element in the list 'imdata', we scan the Interface Counters info
            for counter in operCounterJson.get('imdata'):

                # Auxilear Var Attribute
                attribute = counter['rmonEtherStats']['attributes']

                # The number of broadcast packets received on the interface.
                Interface['broadcastPkts'] = attribute['broadcastPkts']

                # The number of packets with a CRC (Cyclic Redundancy Check) error or a frame alignment error.
                # This indicates a physical layer issue, often due to a faulty cable or transceiver.
                Interface['cRCAlignErrors'] = attribute['cRCAlignErrors']

                # The number of packets that experienced a collision during transmission.
                # In modern full-duplex networks, this counter should always be "0."
                Interface['collisions'] = attribute['collisions']

                # The number of packets dropped by the interface due to congestion or resource limitations.
                Interface['dropEvents'] = attribute['dropEvents']

                # The number of packets that were shorter than the minimum valid packet size of 64 bytes, excluding packets with a CRC error. 
                # These are often caused by late collisions.
                Interface['fragments'] = attribute['fragments']

                # The number of packets that were longer than the maximum valid packet size (1518 bytes for standard Ethernet) 
                # and had a CRC error. This often points to a faulty network card.
                Interface['jabbers'] = attribute['jabbers']

                # The number of multicast packets received. Multicast packets are addressed to a group of specific devices.
                Interface['multicastPkts'] = attribute['multicastPkts']

                # The number of received packets that were larger than the maximum valid packet size but were otherwise error-free.
                Interface['oversizePkts'] = attribute['oversizePkts']

                # The total number of packets, both valid and invalid, received on the interface.
                Interface['pkts'] = attribute['pkts']

                # The number of received packets with a length between 65 and 127 bytes.
                Interface['pkts65to127Octets'] = attribute['pkts65to127Octets']

                # The number of received packets with a length between 128 and 255 bytes.
                Interface['pkts128to255Octets'] = attribute['pkts128to255Octets']

                # The number of received packets with a length between 256 and 511 bytes.
                Interface['pkts256to511Octets'] = attribute['pkts256to511Octets']

                # The number of received packets with a length between 512 and 1023 bytes.
                Interface['pkts512to1023Octets'] = attribute['pkts512to1023Octets']

                # The number of received packets with a length between 1024 and 1518 bytes.
                Interface['pkts1024to1518Octets'] = attribute['pkts1024to1518Octets']

                # The total number of octets (bytes) received on the interface, including good packets, bad packets, and inter-frame gaps.
                Interface['octets'] = attribute['octets']

                # The number of received packets with a length of exactly 64 bytes. This is the minimum valid Ethernet frame size.
                Interface['pkts64Octets'] = attribute['pkts64Octets']

                # The number of packets received without any errors. This is a crucial metric for evaluating the quality of the network link.
                Interface['rXNoErrors'] = attribute['rXNoErrors']

                # The number of received packets that exceeded the maximum frame size.
                Interface['rxGiantPkts'] = attribute['rxGiantPkts']

                # The number of received packets that were larger than the maximum size of the interface.
                Interface['rxOversizePkts'] = attribute['rxOversizePkts']

                # The number of packets transmitted from the interface without any errors.
                Interface['tXNoErrors'] = attribute['tXNoErrors']

                # The number of transmitted packets that exceeded the maximum frame size.
                Interface['txGiantPkts'] = attribute['txGiantPkts']

                # The number of transmitted packets that were larger than the maximum size of the interface.
                Interface['txOversizePkts'] = attribute['txOversizePkts']

                # The number of received packets that were smaller than the minimum valid packet size (64 bytes) but were otherwise error-free.
                Interface['undersizePkts'] = attribute['undersizePkts']

        # Returning Dict with the Operational Counters in the Interface
        return Interface

    #
    # APIC Section 
    #

    # Method that return the NTP Information from the Controllers
    def getApicNtpInfo(self, ntpJson):

        # Auxilear List with the NTP info
        NtpList = []

        # for each NTP Server detected in the JSON var, we add the info into the List
        for ntp in ntpJson['imdata']:

            # Auxilear Var Attributes
            attributes = ntp['datetimeNtpq']['attributes']

            # Copy Attributes info for Dcit Manipulation
            ntp_attributes = attributes.copy()

            # Removing Removing unnecesary info
            ntp_attributes.pop('dn', None)
            ntp_attributes.pop('childAction', None)
            ntp_attributes.pop('modTs', None)
            ntp_attributes.pop('monPolDn', None)
            ntp_attributes.pop('', None)
            ntp_attributes.pop('', None)
            ntp_attributes.pop('', None)
            ntp_attributes.pop('', None)

            # Adding NTP Server Info to the NtpList List
            NtpList.append(ntp_attributes)

        # Returning the NTP Server info detected in the Controller
        return NtpList

    # Method that return the Controller Database status from the Controllers
    def getApicDatabaseStatusInfo(self, BBDDstatusJson):

        # Auxilear List with the power supply info
        BBDDStatusList = []

        # for each entry detected in the JSON var, we add the info into the List
        for health in BBDDstatusJson['imdata']:

            # Auxilear Var Attributes
            attributes = health['infraWiNode']['attributes']

            # Copy Attributes info for Dict Manipulation
            BBDD_attributes = attributes.copy()

            # Removing Removing unnecesary info
            BBDD_attributes.pop('annotation', None)
            BBDD_attributes.pop('childAction', None)
            BBDD_attributes.pop('dn', None)
            BBDD_attributes.pop('extMngdBy', None)
            BBDD_attributes.pop('modTs', None)
            BBDD_attributes.pop('monPolDn', None)
            BBDD_attributes.pop('mutnTs', None)
            BBDD_attributes.pop('name', None)
            BBDD_attributes.pop('nameAlias', None)
            BBDD_attributes.pop('status', None)
            BBDD_attributes.pop('targetMbSn', None)
            BBDD_attributes.pop('uid', None)
            BBDD_attributes.pop('userdom', None)

            # Adding Power Supply Info to the powerSupplyList List
            BBDDStatusList.append(BBDD_attributes)

        # Returning Power Supply info detected in the APIC
        return BBDDStatusList

    # Method that return the Power Supply Information from the Controllers
    def getApicPowerSupplyInfo(self, powerSupplyJson):

        # Auxilear List with the power supply info
        powerSupplyList = []

        # for each power supply detected in the JSON var, we add the info into the List
        for ps in powerSupplyJson['imdata']:

            # Auxilear Var Attributes
            attributes = ps['eqptPsu']['attributes']

            # Copy Attributes info for Dict Manipulation
            ps_attributes = attributes.copy()

            # Removing Removing unnecesary info
            ps_attributes.pop('childAction', None)
            ps_attributes.pop('cimcVersion', None)
            ps_attributes.pop('dn', None)
            ps_attributes.pop('mfgTm', None)
            ps_attributes.pop('modTs', None)
            ps_attributes.pop('monPolDn', None)

            # Adding Power Supply Info to the powerSupplyList List
            powerSupplyList.append(ps_attributes)

        # Returning Power Supply info detected in the APIC
        return powerSupplyList

    # Method that return the power supply information from the Controllers
    def getApicFansInfo(self, fansJson):

        # Auxilear List with the FANs info
        FansList = []

        # for each FAN detected in the JSON var, we add the info into the List
        for fan in fansJson['imdata']:

            # Auxilear Var Attributes
            attributes = fan['eqptFan']['attributes']

            # Copy Attributes info for Dict Manipulation
            fan_attributes = attributes.copy()

            # Removing Removing unnecesary info
            fan_attributes.pop('childAction', None)
            fan_attributes.pop('cimcVersion', None)
            fan_attributes.pop('dir', None)
            fan_attributes.pop('dn', None)
            fan_attributes.pop('mfgTm', None)
            fan_attributes.pop('modTs', None)
            fan_attributes.pop('monPolDn', None)

            # Adding FANs Info to the FansList List
            FansList.append(fan_attributes)

        # Returning FANs info detected in the APICs
        return FansList

    # Method that return the Sensor information from the Controllers
    def getApicSensorInfo(self, sensorJson):

        # Auxilear List with the Sensor info
        SensorList = []

        # for each Sensor detected in the JSON var, we add the info into the List
        for sensor in sensorJson['imdata']:

            # Auxilear Var Attributes
            attributes = sensor['eqptSensor']['attributes']

            # Copy Attributes info for Dict Manipulation
            sensor_attributes = attributes.copy()

            # Removing Removing unnecesary info
            sensor_attributes.pop('childAction', None)
            sensor_attributes.pop('cimcVersion', None)
            sensor_attributes.pop('dn', None)
            sensor_attributes.pop('modTs', None)
            sensor_attributes.pop('monPolDn', None)
            sensor_attributes.pop('', None)
            sensor_attributes.pop('', None)

            # Adding Sensor Info to the SensorList List
            SensorList.append(sensor_attributes)

        # Sorting list based on Sensor ID for clarity
        SensorList.sort(key=lambda x: x['id'])

        # Returning Sensors info detected in the APICs
        return SensorList

    # Method that return the DIMM information from the Controllers
    def getApicDimmInfo(self, dimmJson):

        # Auxilear List with the FANs info
        DimmList = []

        # for each DIMM detected in the JSON var, we add the info into the List
        for dimm in dimmJson['imdata']:

            # Auxilear Var Attributes
            attributes = dimm['eqptDimm']['attributes']

            # Copy Attributes info for Dict Manipulation
            dimm_attributes = attributes.copy()

            # Removing Removing unnecesary info
            dimm_attributes.pop('childAction', None)
            dimm_attributes.pop('cimcVersion', None)
            dimm_attributes.pop('modTs', None)
            dimm_attributes.pop('mfgTm', None)

            # Adding DIMM Info to the SensorList List
            DimmList.append(dimm_attributes)

        # Sorting DimmList based on DIMM ID
        DimmList.sort(key=lambda x: x['id'])

        # Returning DIMM info detected in the APICs
        return DimmList

    # Method that return the Filesystem information from the Controllers
    def getApicFileSystemInfo(self, fsJson):

        # Auxilear List with the Filesystem info
        fsList = []

        # For each Filesystem detected in the JSON var, we add the info into the List
        for fs in fsJson['imdata']:

            # Auxilear Var Attributes
            attributes = fs['eqptStorage']['attributes']

            # Copy Attributes info for Dict Manipulation
            fs_attributes = attributes.copy()

            # Removing unnecesary info
            fs_attributes.pop('dn', None)
            fs_attributes.pop('firmwareVersion', None)
            fs_attributes.pop('modTs', None)
            fs_attributes.pop('monPolDn', None)
            fs_attributes.pop('nameAlias', None)

            # Adding Filesystem Info to the fsList List
            fsList.append(fs_attributes)

        # Returning Filesystem info detected in the APICs
        return fsList

    # Method that return the Physical Interface Controllers information
    def getApicPhyIntInfo(self, PhyIntJson):

        # Auxilear List with the Physics Interface Info
        PhyIntList = []

        # For each Physical Interface detected in the JSON var, we add the info into the PhyIntList list
        for phyInt in PhyIntJson['imdata']:

            # Auxilear Var Attributes
            attributes = phyInt['cnwPhysIf']['attributes']

            # Copy Attributes info for Dict Manipulation
            PhyInt_attributes = attributes.copy()

            # Removing unnecesary info
            PhyInt_attributes.pop('annotation', None)
            PhyInt_attributes.pop('childAction', None)
            PhyInt_attributes.pop('dn', None)
            PhyInt_attributes.pop('extMngdBy', None)
            PhyInt_attributes.pop('modTs', None)
            PhyInt_attributes.pop('monPolDn', None)

            # Adding Physical Interface info to the PhyIntList List
            PhyIntList.append(PhyInt_attributes)

        # Sorting list based in interface name
        PhyIntList.sort(key=lambda x: x['id'])

        # Returning Physical Information info detected in the APICs
        return PhyIntList

    # Method that return the Aggregate Interface in Controllers information
    def getApicAggyIntInfo(self, AggIntJson):

        # Auxilear List with the Physics Interface Info
        AggIntList = []

        # For each Physical Interface detected in the JSON var, we add the info into the PhyIntList list
        for aggInt in AggIntJson['imdata']:

            # Auxilear Var Attributes
            attributes = aggInt['l3EncRtdIf']['attributes']

            # Copy Attributes info for Dict Manipulation
            aggInt_attributes = attributes.copy()

            # Removing unnecesary info
            aggInt_attributes.pop('childAction', None)
            aggInt_attributes.pop('dn', None)
            aggInt_attributes.pop('ethpmCfgFailedTs', None)
            aggInt_attributes.pop('modTs', None)
            aggInt_attributes.pop('monPolDn', None)

            # Adding Physical Interface info to the PhyIntList List
            AggIntList.append(aggInt_attributes)

        # Sorting list based in interface name
        AggIntList.sort(key=lambda x: x['id'])

        # Returning Physical Information info detected in the APICs
        return AggIntList

    ######################
    # Tenant Get Methods #
    ######################

    # Method that return the full tenant subtree information
    def getTenantFullSubtreeInfo(self, tenantJson: Dict[str, Any]) -> List[Dict[str, Any]]:

        # Auxilear List with the full tenant info
        tenantList: List[Dict[str, Any]] = []

        # The 'imdata' array holds various objects. We filter to keep only true fvTenant objects.
        if tenantJson.get('imdata'):
            for obj in tenantJson['imdata']:
                # ONLY append the object if its primary key is 'fvTenant'
                if 'fvTenant' in obj:
                    tenantList.append(obj)

        # Returning the list of filtered fvTenant objects
        return tenantList
