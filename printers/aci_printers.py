# coding=utf-8

######################################################################################################
#  Class that will print all the information collected in the network_graph.py from Cisco ACI Fabric #
######################################################################################################

##################
# Import Section #
##################

from typing import Any, Dict, Type, List
import networkx as nx

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

##########################################################################################################
# ACITroubleshooterPrinter Class that will print all the json info received from network_graph.py Script #
##########################################################################################################

class ACITroubleshooterPrinter(metaclass=_PrivateCookie):

    ########################
    # Switch Nodes Methods #
    ########################

    # Method that will print the interfaces info detected in the Switches Node in the Graph
    def getSwitchNodeInterfacesInfo(self, graph: nx.Graph) -> None:

        # Fabric Tuple to know if the Node device is a 'spine' or a 'leaf'
        fabricSwitches = ('spine', 'leaf')

        # Header for the Switch Interface table
        sw_int_header_keys = ['Node', 'Int ID', 'Admin St', 'Oper  St', 'Last Errors', 'Oper Mode', 'Oper Duplex', 'Oper Speed', 'MTU', 'Medium', 'Usage', 'Last Link Flap']
        sw_int_header_line = "{:<11} {:<8} {:<9} {:<9} {:<12} {:<10} {:<13} {:<11} {:<10} {:<20} {:<20} {:<29}".format(*sw_int_header_keys)

        # Print the header if it hasn't been printed yet
        header_text = " Switch Nodes Interface Info "
        total_width = len(sw_int_header_line)
        centered_header = header_text.center(total_width, '-')
        print("-" * len(sw_int_header_line))
        print(centered_header)
        print("-" * len(sw_int_header_line))
        print(sw_int_header_line)
        print("-" * len(sw_int_header_line))

        # Iterate through each node in the graph
        for node, attributes in graph.nodes(data=True):

            # Auxilear variable to compare the role in the if statement below
            role = attributes.get('role')

            # Check if the node is a switch and has the 'interfaces' attribute
            if role is not None and role in fabricSwitches and 'interfaces' in attributes and attributes['interfaces']:

                # Iterate through each interfaces entry for the Switch Node
                for interface in attributes['interfaces']:

                    # Find the corresponding operational info for the current interface
                    # Use a dictionary comprehension for a more efficient lookup
                    oper_info_map = {op_int['intID']: op_int for op_int in attributes.get('opt_interfaces', [])}
                    oper_info = oper_info_map.get(interface.get('id', '').lower())

                    # Initialize variables with default values
                    operSt = "down"
                    lastError = "0"
                    operMode = "trunk"
                    operDuplex = "full"
                    operSpeed = "inherit"
                    lastListStateChange = "N/A"

                    # Update variables if operational info is found
                    if oper_info and oper_info.get('operSt'):
                        operSt = oper_info['operSt'].get('operSt', operSt)
                        lastError = oper_info['operSt'].get('lastErrors', lastError)
                        operMode = oper_info['operSt'].get('operMode', operMode)
                        operDuplex = oper_info['operSt'].get('operDuplex', operDuplex)
                        operSpeed = oper_info['operSt'].get('operSpeed', operSpeed)
                        lastListStateChange = oper_info['operSt'].get('lastLinkStChg', lastListStateChange)

                    # Preparing the data tuple to be printed
                    interface_data = (
                        node,
                        interface.get('id', 'N/A'),
                        interface.get('adminSt', 'N/A'),
                        operSt,
                        lastError,
                        operMode,
                        operDuplex,
                        operSpeed,
                        interface.get('mtu', 'N/A'),
                        interface.get('medium', 'N/A'),
                        interface.get('usage', 'N/A'),
                        lastListStateChange
                    )

                    # Print the Interfaces data
                    print("{:<11} {:<8} {:<9} {:<9} {:<12} {:<10} {:<13} {:<11} {:<10} {:<20} {:<20} {:<29}".format(*interface_data))

        # Printing End separation at the end of the output
        print("-" * len(sw_int_header_line))

    # Method that will print Supervisor info detected in the Switches Node in the Graph
    def getSwitchNodeSupervisorInfo(self, graph: nx.Graph) -> None:

        # Fabric Tuple to know if the Node device is a 'spine'
        fabricSwitches = ('spine','leaf')

        # Header for the Switch Supervisor table
        sw_sup_header_keys = ['Node', 'Sup ID', 'Desc', 'HW Ver', 'Model', 'Num Ports', 'Oper Status', 'Power Status', 'S/N', 'Uptime', 'Vendor']
        sw_sup_header_line = "{:<11} {:<8} {:<17} {:<7} {:18} {:<10} {:<12} {:<13} {:<14} {:<30} {:<19}".format(*sw_sup_header_keys)

        # Print the header if it hasn't been printed yet
        header_text = " Switch Nodes Supervisor Info "
        total_width = len(sw_sup_header_line)
        centered_header = header_text.center(total_width, '-')
        print("-" * len(sw_sup_header_line))
        print(centered_header)
        print("-" * len(sw_sup_header_line))
        print(sw_sup_header_line)
        print("-" * len(sw_sup_header_line))

        # Iterate through each node in the graph
        for node, attributes in graph.nodes(data=True):

            # Auxilear variable to compare the role in the if statement below
            role = attributes.get('role')

        # Check if the node is a switch and has the 'supervisors' attribute
            if role is not None and role in fabricSwitches and 'supervisors' in attributes and attributes['supervisors']:

                # Iterate through each supervisors entry for the Switch Node
                for sup in attributes['supervisors']:

                    # Prepare the data tuple to be printed            
                    sup_data = (
                        node,
                        sup.get('id','N/A'),
                        sup.get('descr','N/A'),
                        sup.get('hwVer','N/A'),
                        sup.get('model','N/A'),
                        sup.get('numP','N/A'),
                        sup.get('operSt','N/A'),
                        sup.get('pwrSt','N/A'),
                        sup.get('ser','N/A'),
                        sup.get('upTs', 'N/A'),
                        sup.get('vendor', 'N/A')
                    )

                    # Print the filesystem data
                    print("{:<11} {:<8} {:<17} {:<7} {:18} {:<10} {:<12} {:<13} {:<14} {:<30} {:<19}".format(*sup_data))

        # Printing End separation at the end of the output
        print("-" * len(sw_sup_header_line))

    # Method that will print the Faults info detected in the Switches Node in the Graph
    def getSwitchNodeFaultsInfo(self, graph: nx.Graph) -> None:

        # Fabric Tuple to know if the Node device is a 'spine'
        fabricSwitches = ('spine','leaf')

        # Header for the Spine System Controller table
        sw_fault_header_keys = ['Node', 'Subject', 'Type', 'Code', 'Severity', 'Count', 'Cause', 'Domain', 'Rule', 'Fault Description Brief']
        sw_fault_header_line = "{:<11} {:<18} {:<15} {:<8} {:<8} {:<6} {:<25} {:<10} {:<35} {:<50}".format(*sw_fault_header_keys)

        # Print the header if it hasn't been printed yet
        header_text = " Switch Node Faults Info "
        total_width = len(sw_fault_header_line)
        centered_header = header_text.center(total_width, '-')
        print("-" * len(sw_fault_header_line))
        print(centered_header)
        print("-" * len(sw_fault_header_line))
        print(sw_fault_header_line)
        print("-" * len(sw_fault_header_line))

        # Iterate through each node in the graph
        for node, attributes in graph.nodes(data=True):

            # Auxilear variable to compare the role in the if statement below
            role = attributes.get('role')

            # Check if the node is a switch and has the 'Faults' attribute
            if role is not None and role in fabricSwitches and 'faults' in attributes and attributes['faults']:

                # Iterate through each Fault entry for the Switch Node
                for fault in attributes['faults']:

                    # Get the fault description shorten if it necessary
                    path = fault.get('descr', 'N/A')
                    if len(path) > 50:
                        short_path = path[:47] + '...'
                    else:
                        short_path = path

                    # Prepare the data tuple to be printed
                    fault_data = (
                        node,
                        fault.get('subject','N/A'),
                        fault.get('type','N/A'),
                        fault.get('code','N/A'),
                        fault.get('severity','N/A'),
                        fault.get('count','N/A'),
                        fault.get('cause','N/A'),
                        fault.get('domain','N/A'),
                        fault.get('rule','N/A'),
                        short_path
                    )

                    # Print the filesystem data
                    print("{:<11} {:<18} {:<15} {:<8} {:<8} {:<6} {:<25} {:<10} {:<35} {:<50}".format(*fault_data))

        # Printing End separation at the end of the output
        print("-" * len(sw_fault_header_line))

    # Method that will print the System Controller info detected in the Spine Node Switches in the Graph
    def getSpineSwitchNodeSystemControllerInfo(self, graph: nx.Graph) -> None:

        # Fabric Tuple to know if the Node device is a 'spine'
        fabricSwitches = ('spine')

        # Header for the Spine System Controller table
        sw_sc_header_keys = ['Node', 'SC ID', 'HW Version', 'Model', 'Operational State', 'rdSt', 'Power State',  'Type', 'Serial Number','Uptime','Vendor']
        sw_sc_header_line = "{:<15} {:<7} {:<15} {:<13} {:<20} {:<10} {:<13} {:<15} {:<17} {:<30} {:<20}".format(*sw_sc_header_keys)

        # Print the header if it hasn't been printed yet
        header_text = " Spine Switch System Controller Info "
        total_width = len(sw_sc_header_line)
        centered_header = header_text.center(total_width, '-')
        print("-" * len(sw_sc_header_line))
        print(centered_header)
        print("-" * len(sw_sc_header_line))
        print(sw_sc_header_line)
        print("-" * len(sw_sc_header_line))

        # Iterate through each node in the graph
        for node, attributes in graph.nodes(data=True):

            # Auxilear variable to compare the role in the if statement below
            role = attributes.get('role')

            # Check if the node is a switch and has the 'system_controller' attribute
            if role is not None and role in fabricSwitches and 'system_controller' in attributes and attributes['system_controller']:

                # Iterate through each System Controler entry for the Spine Switch node
                for sc in attributes['system_controller']:

                    # Prepare the data tuple to be printed
                    sc_data = (
                        node,
                        sc.get('id','N/A'),
                        sc.get('hwVer','N/A'),
                        sc.get('model','N/A'),
                        sc.get('operSt','N/A'),
                        sc.get('rdSt','N/A'),
                        sc.get('pwrSt','N/A'),
                        sc.get('type','N/A'),
                        sc.get('ser','N/A'),
                        sc.get('upTs','N/A'),
                        sc.get('vendor','N/A')
                    )

                    # Print the filesystem data
                    print("{:<15} {:<7} {:<15} {:<13} {:<20} {:<10} {:<13} {:<15} {:<17} {:<30} {:<20}".format(*sc_data))

        # Printing End separation at the end of the output
        print("-" * len(sw_sc_header_line))

    # Method that will print the Fabric Modules info detected in the Spine Node Switch in the Graph
    def getSpineSwitchNodeFabricModulesInfo(self, graph: nx.Graph) -> None:

        # Fabric Tuple to know if the Node device is a 'spine'
        fabricSwitches = ('spine')

        # Header for the Spine Fabric Module table
        sw_fm_header_keys = ['Node', 'FM ID', 'HW Version', 'Model', 'Operational State', 'rdSt', 'Serial Number', 'Uptime','Vendor']
        sw_fm_header_line = "{:<11} {:<8} {:<12} {:<17} {:<19} {:<8} {:<15} {:<30} {:<19}".format(*sw_fm_header_keys)

        # Print the header if it hasn't been printed yet
        header_text = " Spine Switch Fabric Modules Info "
        total_width = len(sw_fm_header_line)
        centered_header = header_text.center(total_width, '-')
        print("-" * len(sw_fm_header_line))
        print(centered_header)
        print("-" * len(sw_fm_header_line))
        print(sw_fm_header_line)
        print("-" * len(sw_fm_header_line))

        # Iterate through each node in the graph
        for node, attributes in graph.nodes(data=True):

            # Auxilear variable to compare the role in the if statement below
            role = attributes.get('role')

            # Check if the node is a switch and has the 'sfp' attribute
            if role is not None and role in fabricSwitches and 'fabric_modules' in attributes and attributes['fabric_modules']:

                # Iterate through each Fabric Module entry for the Spine node
                for fm in attributes['fabric_modules']:

                     # Prepare the data tuple to be printed
                    fm_data = (
                        node,
                        fm.get('id','N/A'),
                        fm.get('hwVer','N/A'),
                        fm.get('model','N/A'),
                        fm.get('operSt','N/A'),
                        fm.get('rdSt','N/A'),
                        fm.get('ser','N/A'),
                        fm.get('upTs','N/A'),
                        fm.get('vendor','N/A')
                    )

                    # Print the filesystem data
                    print("{:<11} {:<8} {:<12} {:<17} {:<19} {:<8} {:<15} {:<30} {:<19}".format(*fm_data))

        # Printing End separation at the end of the output
        print("-" * len(sw_fm_header_line))

    # Method that will print the Power Supply Units (PSUs) detected in the Switch Nodes in the Graph
    def getSwitchNodePsuInfo(self, graph: nx.Graph) -> None:

        # Fabric Tuple to know if the Node device is a 'leaf' or a 'spine'
        fabricSwitches = ('spine','leaf')

        # Header for the APIC filesystem table
        sw_psu_header_keys = ['Node', 'PSU ID', 'Operational Status', 'HW Version', 'Model', 'Serial Number', 'Vendor']
        sw_psu_header_line = "{:<13} {:<8} {:<20} {:<13} {:<20} {:<15} {:<19}".format(*sw_psu_header_keys)

        # Print the header if it hasn't been printed yet
        header_text = " Switch Power Supply Units Info "
        total_width = len(sw_psu_header_line)
        centered_header = header_text.center(total_width, '-')
        print("-" * len(sw_psu_header_line))
        print(centered_header)
        print("-" * len(sw_psu_header_line))
        print(sw_psu_header_line)
        print("-" * len(sw_psu_header_line))

        # Iterate through each node in the graph
        for node, attributes in graph.nodes(data=True):

            # Auxilear variable to compare the role in the if statement below
            role = attributes.get('role')

            # Check if the node is a switch and has the 'psus' attribute
            if role is not None and role in fabricSwitches and 'psus' in attributes and attributes['psus']:

                # Iterate through each filesystem entry for the Controller node
                for psu in attributes['psus']:

                    # Prepare the data tuple to be printed
                    psu_data = (
                        node,
                        psu.get('id','N/A'),
                        psu.get('operSt','N/A'),
                        psu.get('hwVer','N/A'),
                        psu.get('model','N/A'),
                        psu.get('ser','N/A'),
                        psu.get('vendor','N/A'),
                    )

                    # Print the filesystem data
                    print("{:<13} {:<8} {:<20} {:<13} {:<20} {:<15} {:<19}".format(*psu_data))

        # Printing End separation at the end of the output
        print("-" * len(sw_psu_header_line))

    # Method that will print the Linecards detected in the Switch Node in the Graph
    def getSwitchNodeLinecardInfo(self, graph: nx.Graph) -> None:

        # Fabric Tuple to know if the Node device is a 'leaf' or a 'spine'
        fabricSwitches = ('spine','leaf')

        # Header for the APIC filesystem table
        sw_linecard_header_keys = ['Node', 'Linecard ID', 'Hardware Version', 'Model', 'Operational State', 'rdSt', 'Serial Number', 'Uptime', 'Vendor']
        sw_linecard_header_line = "{:<12} {:<13} {:<18} {:<18} {:<20} {:<8} {:<15} {:<30} {:<20}".format(*sw_linecard_header_keys)

        # Print the header if it hasn't been printed yet
        header_text = " Switch Linecard Info "
        total_width = len(sw_linecard_header_line)
        centered_header = header_text.center(total_width, '-')
        print("-" * len(sw_linecard_header_line))
        print(centered_header)
        print("-" * len(sw_linecard_header_line))
        print(sw_linecard_header_line)
        print("-" * len(sw_linecard_header_line))

        # Iterate through each node in the graph
        for node, attributes in graph.nodes(data=True):

            # Auxilear variable to compare the role in the if statement below
            role = attributes.get('role')

            # Check if the node is a switch and has the 'sfp' attribute
            if role is not None and role in fabricSwitches and 'linecard' in attributes and attributes['linecard']:

                # Iterate through each filesystem entry for the Controller node
                for linec in attributes['linecard']:

                    # Prepare the data tuple to be printed
                    linecard_data = (
                        node,
                        linec.get('id','N/A'),
                        linec.get('hwVer','N/A'),
                        linec.get('model','N/A'),
                        linec.get('operSt','N/A'),
                        linec.get('rdSt','N/A'),
                        linec.get('ser','N/A'),
                        linec.get('upTs','N/A'),
                        linec.get('vendor','N/A')
                    )

                    # Print the filesystem data
                    print("{:<12} {:<13} {:<18} {:<18} {:<20} {:<8} {:<15} {:<30} {:<20}".format(*linecard_data))

        # Printing End separation at the end of the output
        print("-" * len(sw_linecard_header_line))

    # Method that will print the SFP Interface Information collected from the Switches Node in the Graph
    def printSwitchNodesSfpInterfaceInfo(self, graph: nx.Graph) -> None:

        # Fabric Tuple to know if the Node device is a 'leaf' or a 'spine'
        fabricSwitches = ('spine','leaf')

        # Header for the Switch SFP table
        sw_sfp_header_keys = ['Node', 'Interface ID', 'actualType', 'Flag', 'S/N', 'guiCiscoEID', 'guiCiscoPID', 'guiCiscoPN']
        sw_sfp_header_line = "{:<12} {:<16} {:<13} {:<8} {:<16} {:<19} {:<19} {:<15}".format(*sw_sfp_header_keys)

        header_text = " Switch SFP Info "
        total_width = len(sw_sfp_header_line)
        centered_header = header_text.center(total_width, '-')
        print("-" * len(sw_sfp_header_line))
        print(centered_header)
        print("-" * len(sw_sfp_header_line))
        print(sw_sfp_header_line)
        print("-" * len(sw_sfp_header_line))

        # Iterate through each node in the graph
        for node, attributes in graph.nodes(data=True):

            # Auxilear variable to compare the role in the if statement below
            role = attributes.get('role')

            # Check if the node is a switch and has the 'sfp' attribute
            if role is not None and role in fabricSwitches and 'sfp' in attributes and attributes['sfp']:

                # Iterate through each sfp entry for the Controller node
                for sfp in attributes['sfp']:

                    # Prepare the data tuple to be printed
                    sfp_data = (
                        node,
                        sfp.get('int_id','N/A'),
                        sfp.get('actualType','N/A'),
                        sfp.get('flags','N/A'),
                        sfp.get('guiSN','N/A'),
                        sfp.get('guiCiscoEID','N/A'),
                        sfp.get('guiCiscoPID','N/A'),
                        sfp.get('guiCiscoPN','N/A')
                    )

                    # Print the sfp data
                    print("{:<12} {:<16} {:<13} {:<8} {:<16} {:<19} {:<19} {:<15}".format(*sfp_data))

        # Printing End separation at the end of the output
        print("-" * len(sw_sfp_header_line))

    # Method that prints detailed diagnostic information for all SFPs (Temperature, Power, Voltage).
    def printSwitchSfpDiagnostics(self, graph: nx.Graph) -> None:

        # Fabric Tuple to know if the Node device is a 'leaf' or a 'spine'
        fabricSwitches = ('spine', 'leaf')

        # Define acceptable ranges (simplified logic for demonstration)
        # In a real environment, these limits would be fetched from ACI MOs (e.g., eqptFcotDiags)
        TEMP_MAX = 75.0
        TEMP_MIN = 0.0
        VOLT_MAX = 3.6
        VOLT_MIN = 3.0

        # Power is typically measured in dBm or mW. Limits vary by optic type.
        # Use a simplified threshold for flag checks based on the unit being mW or a generic range.
        RX_PWR_LOW_MW = 0.05 # ~-13dBm, indicating very low receive power
        TX_PWR_LOW_MW = 0.05

        print("-" * 120)
        print(" SFP DIAGNOSTIC DETAILS (POWER, TEMP, VOLTAGE) ".center(120, '='))
        print("-" * 120)

        sfps_checked = 0

        for node, attributes in graph.nodes(data=True):
            role = attributes.get('role')

            if role in fabricSwitches and 'sfp' in attributes and attributes['sfp']:

                print(f"\n<<< Node: {node} >>>")
                print("=" * (len(node) + 12))

                # Prepare the main table header
                header_keys = ['Int ID', 'Type', 'S/N', 'State', 'Temp (C)', 'Voltage (V)', 'Flags']
                header_line = "{:<10} {:<10} {:<15} {:<10} {:<10} {:<12} {:<30}".format(*header_keys)

                print(header_line)
                print("-" * 120)

                for sfp in attributes['sfp']:
                    sfps_checked += 1

                    # Core Attributes
                    int_id = sfp.get('int_id', 'N/A')
                    actual_type = sfp.get('actualType', 'N/A')
                    serial_num = sfp.get('guiSN', 'N/A')

                    # Diagnostic Values (handle N/A from the parser)
                    temp_c = sfp.get('temp', 'N/A')
                    volt_v = sfp.get('volt', 'N/A')
                    oper_status = sfp.get('operSt', 'N/A')

                    # Set Health Flags
                    flags = []

                    # Check operational status (often determined by the SFP's internal flags)
                    if sfp.get('flags', 'N/A') != 'ok':
                        flags.append(f"FLAGS:{sfp.get('flags', 'N/A').upper()}")

                    # Check operational status field if present
                    if oper_status != 'ok' and oper_status != 'N/A':
                        flags.append(f"STATUS:{oper_status.upper()}")

                    try:
                        temp = float(temp_c)
                        if temp > TEMP_MAX:
                            flags.append("HIGH TEMP")
                        elif temp < TEMP_MIN:
                            flags.append("LOW TEMP")
                    except (ValueError, TypeError):
                        pass

                    try:
                        volt = float(volt_v)
                        if volt > VOLT_MAX:
                            flags.append("HIGH VOLTAGE")
                        elif volt < VOLT_MIN:
                            flags.append("LOW VOLTAGE")
                    except (ValueError, TypeError):
                        pass

                    # Format data for the main row
                    main_data = (
                        int_id,
                        actual_type,
                        serial_num,
                        sfp.get('flags', 'N/A'),
                        temp_c,
                        volt_v,
                        ", ".join(flags) if flags else "OK"
                    )

                    # Print main SFP row
                    print("{:<10} {:<10} {:<15} {:<10} {:<10} {:<12} {:<30}".format(*main_data))

                    # Print Tx/Rx Details
                    tx_pwr = sfp.get('txPwr', 'N/A')
                    rx_pwr = sfp.get('rxPwr', 'N/A')
                    bias_c = sfp.get('bias', 'N/A')

                    power_flags = []

                    # Flag low Rx/Tx power
                    try:
                        if rx_pwr != 'N/A' and float(rx_pwr) < RX_PWR_LOW_MW:
                             power_flags.append("RX_LOW")
                        if tx_pwr != 'N/A' and float(tx_pwr) < TX_PWR_LOW_MW:
                             power_flags.append("TX_LOW")
                    except (ValueError, TypeError):
                        pass

                    # Only print the detail line if we have power or bias info
                    if tx_pwr != 'N/A' or rx_pwr != 'N/A' or bias_c != 'N/A':
                         print(f"  |-> Power: Tx {tx_pwr}mW | Rx {rx_pwr}mW | Bias {bias_c}mA | Power Health: {', '.join(power_flags) if power_flags else 'OK'}")

                print("-" * 120)

        if sfps_checked == 0:
             print("No SFP data was collected from fabric switches.")

        print("\n" + "=" * 120)
        print(" END OF SFP DIAGNOSTIC REPORT ".center(120, '='))
        print("=" * 120)

    # Method that will print all the Filesystem feching from the Switches node in the Graph
    def printFabricSwitchesFilesystemNodes(self, graph: nx.Graph) -> None:

        # Fabric Tuple to know if the Node device is a Fabric Switch
        fabricSwitches = ('spine','leaf')

        # Header for the filesystem table
        fs_header_keys = ['Node', 'Path', 'Available (MB)', 'Used (MB)', 'Used (%)', 'Memory Alert']
        fs_header_line = "{:<12} {:<55} {:<15} {:<12} {:<10} {:<12}".format(*fs_header_keys)

        print("-" * len(fs_header_line))
        filesystem_header=" File System Information "
        #print("------------------------------------------------- File System Information ----------------------------------------------")
        total_width = len(fs_header_line)
        centered_header = filesystem_header.center(total_width, '-')
        print(centered_header)
        print("-" * len(fs_header_line))
        print(fs_header_line)
        print("-" * len(fs_header_line))

        # For each node in the graph, check for filesystem attributes
        for node, attributes in graph.nodes(data=True):

            # We check if if the attribute
            if (attributes.get('role') in fabricSwitches) and ('filesystem' in attributes) and (attributes['filesystem']):

                # Iterate through each filesystem entry for the node
                for fs in attributes['filesystem']:

                    path = fs.get('path', 'N/A')
                    if len(path) > 55:
                        short_path = path[:51] + '...'
                    else:
                        short_path = path

                    # Prepare the data tuple to be printed
                    fs_data = (
                        node,
                        short_path,
                        fs.get('avail', 'N/A'),
                        fs.get('used', 'N/A'),
                        str(fs.get('used_perc', 'N/A')) + "%",
                        fs.get('memAlert', 'N/A')
                    )

                    # Print the filesystem data
                    print("{:<12} {:<55} {:<15} {:<12} {:<10} {:<12}".format(*fs_data))

        # Printing End separation at the end of the output
        print("-" * len(fs_header_line))

    # Method that will print all the Switches Nodes detected in the Fabric
    def printFabricSwitchesNodes(self, graph: nx.Graph) -> None:

        # Fabric Tuple to know if the Node device is a Fabric Switch
        fabricSwitches = ('spine','leaf')

        # Switch headers for clarity
        switch_header_keys = ['Node', 'id', 'role', 'model', 'version', 'address', 'serial', 'adSt', 'fabricSt']
        switch_header_line = "{:<20} {:<5} {:<15} {:<20} {:<15} {:<15} {:<20} {:<5} {:<10}".format(*switch_header_keys)

        #Auxilear variable to print the header only once
        header_printed = True

        # For each Node attribute, we print the info in the CLI
        for node, attributes in graph.nodes(data=True):

            # We print the content if the element is a leaf or spine switch
            if attributes.get('role') in fabricSwitches:

                # Printing header in the CLI
                if header_printed:
                    print("-" * len(switch_header_line))
                    print(switch_header_line)
                    print("-" * len(switch_header_line))
                    header_printed = False

                # Prepare the data tuple to be printed
                node_data = (
                    node,
                    attributes.get('id', 'N/A'),
                    attributes.get('role', 'N/A'),
                    attributes.get('model', 'N/A'),
                    attributes.get('version', 'N/A'),
                    attributes.get('address', 'N/A'),
                    attributes.get('serial', 'N/A'),
                    attributes.get('adSt', 'N/A'),
                    attributes.get('fabricSt', 'N/A')
                )

                # Printing Switch Attributes
                print("{:<20} {:<5} {:<15} {:<20} {:<15} {:<15} {:<20} {:<5} {:<10}".format(*node_data))

        # Printing End separation at the end of the output
        print("-" * len(switch_header_line))

    # Method that print all Controllers Nodes detected in the Fabric
    def printFabriControllersNodes(self, graph: nx.Graph) -> None:

        # Fabric Tuple to know if the Node device is a Controller
        fabricController = ('controller')

        # Print the header only once
        header_printed = True

        # Controller Headers for clarity 
        controller_header_keys = ['Node', 'id', 'role', 'apicType', 'model', 'version', 'address', 'serial', 'adSt', 'fabricSt']
        controller_header_line = "{:<20} {:<5} {:<15} {:<10} {:<20} {:<10} {:<15} {:<20} {:<5} {:<10}".format(*controller_header_keys)

        # For each Node attribute, we print the info in the CLI
        for node, attributes in graph.nodes(data=True):

            # Auxilear Variable to detect if the node in the graph have a Fabric Controller
            role = attributes.get('role')

            # Check if the node is a fabric element
            if role is not None and role in fabricController:

                # Printing the header only once
                if header_printed:

                    # Printing controller headers
                    print("-" * len(controller_header_line))
                    print(controller_header_line)
                    print("-" * len(controller_header_line))
                    header_printed = False

                # Preparing the data tuple format to be printed
                node_data = (
                    node,
                    attributes.get('id', 'N/A'),
                    attributes.get('role', 'N/A'),
                    attributes.get('apicType', 'N/A'),
                    attributes.get('model', 'N/A'),
                    attributes.get('version', 'N/A'),
                    attributes.get('address', 'N/A'),
                    attributes.get('serial', 'N/A'),
                    attributes.get('adSt', 'N/A'),
                    attributes.get('fabricSt', 'N/A')
                )

                # Printing Controller Attributes
                print("{:<20} {:<5} {:<15} {:<10} {:<20} {:<10} {:<15} {:<20} {:<5} {:<10}".format(*node_data))

        # Printing End separation at the end of the output
        print("-" * len(controller_header_line))

    ###########################################################
    # Switch Nodes Methods to Recommend Actions in the Fabric #
    ###########################################################

    # Printing Recommended Interfaces Actions in the fabric
    def getSwitchNodeInterfacesShouldBeDownInfo(self, graph: nx.Graph) -> None:

        # Fabric Tuple to know if the Node device is a 'spine' or a 'leaf'
        fabricSwitches = ('spine', 'leaf')

        # Header for the Switch Interface table
        sw_int_header_keys = ['Node', 'Int ID', 'Admin St', 'Oper  St']
        sw_int_header_line = "{:<13} {:<10} {:<11} {:<11}".format(*sw_int_header_keys)

        # Print the header if it hasn't been printed yet
        header_text = " Switch Nodes Interface that should be down "
        total_width = len(sw_int_header_line)
        centered_header = header_text.center(total_width, '-')
        print("-" * len(sw_int_header_line))
        print(centered_header)
        print("-" * len(sw_int_header_line))
        print(sw_int_header_line)
        print("-" * len(sw_int_header_line))

        # Iterate through each node in the graph
        for node, attributes in graph.nodes(data=True):

            # Auxilear variable to compare the role in the if statement below
            role = attributes.get('role')

            # Check if the node is a switch and has the 'interfaces' attribute
            if role is not None and role in fabricSwitches and 'interfaces' in attributes and attributes['interfaces']:

                # Iterate through each interfaces entry for the Switch Node
                for interface in attributes['interfaces']:

                    # Find the corresponding operational info for the current interface
                    # Use a dictionary comprehension for a more efficient lookup
                    oper_info_map = {op_int['intID']: op_int for op_int in attributes.get('opt_interfaces', [])}
                    oper_info = oper_info_map.get(interface.get('id', '').lower())

                    # Initialize variables with default values
                    operSt = "down"

                    # Update variables if operational info is found
                    if oper_info and oper_info.get('operSt'):
                        operSt = oper_info['operSt'].get('operSt', operSt)

                    if interface.get('adminSt') == "up" and operSt == "down":

                        # Preparing the data tuple to be printed
                        interface_data = (
                            node,
                            interface.get('id', 'N/A'),
                            interface.get('adminSt', 'N/A'),
                            operSt,
                        )

                        # Print the Interfaces data
                        print("{:<13} {:<10} {:<11} {:<11}".format(*interface_data))

        # Printing End separation at the end of the output
        print("-" * len(sw_int_header_line))

    ######################
    # APIC Nodes Methods #
    ######################

    # Method that will print all the NTP info from the Controllers Node in the Graph
    def printApicNodesNtpInfo(self, graph: nx.Graph) -> None:

        # Fabric Tuple to know if the Node device is a controller
        fabricController = ('controller')

        # Header for the APIC filesystem table
        apic_ntp_header_keys = ['Node', 'NTP Server IP', 'Authentication', 'Delay', 'Jitter', 'Reach', 'Reference ID', 'Stratum', 'Relationship', 'Sync Status', 'Last Respond (sec)']
        apic_ntp_header_line = "{:<12} {:<16} {:<17} {:<7} {:<8} {:<8} {:<13} {:<10} {:<15} {:<25} {:<20}".format(*apic_ntp_header_keys)

        header_text = " APIC NTP Information "
        total_width = len(apic_ntp_header_line)
        centered_header = header_text.center(total_width, '-')
        print("-" * len(apic_ntp_header_line))
        print(centered_header)
        print("-" * len(apic_ntp_header_line))
        print(apic_ntp_header_line)
        print("-" * len(apic_ntp_header_line))

        # Iterate through each node in the graph
        for node, attributes in graph.nodes(data=True):

            # Auxilear variable to compare the role in the if statement below
            role = attributes.get('role')

            # Check if the node is a controller (APIC) and has the 'apic_ntp' attribute
            if role is not None and role in fabricController and 'apic_ntp' in attributes and attributes['apic_ntp']:

                # Iterate through each Physical Interface entry for the Controller node
                for ntp in attributes['apic_ntp']:

                    # Improving Output Quality, If the type is 'u' means
                    # the communication between Controller and NTP Server is Unicast
                    typeNtp = ""
                    if ntp.get('t') == "u":
                        typeNtp = "Unicast"
                    else:
                        typeNtp = ntp.get('t')

                    # Improving Qurput Quality, if the 'tally' field is equal to '*'
                    # means that is the best NTP Server available
                    syncStatus = ""
                    if ntp.get('tally') == "*":
                        syncStatus = "Optimal NTP Server Sync"
                    else:
                        syncStatus = ntp.get('tally')

                    # Prepare the data tuple to be printed
                    ntp_data = (
                        node,
                        ntp.get('remote', 'N/A'),
                        ntp.get('auth', 'N/A'),
                        ntp.get('delay', 'N/A'),
                        ntp.get('jitter', 'N/A'),
                        ntp.get('reach', 'N/A'),
                        ntp.get('refid', 'N/A'),
                        ntp.get('stratum', 'N/A'),
                        typeNtp,
                        syncStatus,
                        ntp.get('when', 'N/A')
                    )

                    # Print the filesystem data
                    print("{:<12} {:<16} {:<17} {:<7} {:<8} {:<8} {:<13} {:<10} {:<15} {:<25} {:<20}".format(*ntp_data))

        # Printing End separation at the end of the output
        print("-" * len(apic_ntp_header_line))

    # Method that will print all the Filesystem feching from the Controlers Node in the Graph
    def printApicNodesFileSystemInfo(self, graph: nx.Graph) -> None:

        # Fabric Tuple to know if the Node device is a controller
        fabricController = ('controller')

        # Header for the APIC filesystem table
        apic_fs_header_keys = ['Node', 'Path', 'Mount', 'File System', 'Oper Status', 'Cap Utilized (%)']
        apic_fs_header_line = "{:<15} {:<30} {:<30} {:<25} {:<15} {:<16}".format(*apic_fs_header_keys)

        # Print the header only once
        header_printed = True

        # Iterate through each node in the graph
        for node, attributes in graph.nodes(data=True):

            # Auxilear variable to compare the role in the if statement below
            role = attributes.get('role')

            # Check if the node is a controller (APIC) and has the 'apic_filesystem' attribute
            if role is not None and role in fabricController and 'apic_filesystem' in attributes and attributes['apic_filesystem']:

                # Print the header if it hasn't been printed yet
                if header_printed:
                    header_text = " APIC File System Information "
                    total_width = len(apic_fs_header_line)
                    centered_header = header_text.center(total_width, '-')
                    print("-" * len(apic_fs_header_line))
                    print(centered_header)
                    print("-" * len(apic_fs_header_line))
                    header_printed = False

                # Printing header for each Controller detected in the Graph
                print(apic_fs_header_line)
                print("-" * len(apic_fs_header_line))

                # Iterate through each filesystem entry for the Controller node
                for fs in attributes['apic_filesystem']:

                    # Get the path and shorten it if necessary
                    path = fs.get('name', 'N/A')
                    if len(path) > 27:
                        short_path = path[:24] + '...'
                    else:
                        short_path = path

                    # Get the path and shorten it if necessary
                    mountPath = fs.get('mount', 'N/A')
                    if len(mountPath) > 27:
                        short_mount_path = mountPath[:24] + '...'
                    else:
                        short_mount_path = mountPath

                    # Get the path and shorten it if necessary
                    filesystemPath = fs.get('fileSystem', 'N/A')
                    if len(filesystemPath) > 24:
                        short_fspath_path = filesystemPath[:21] + '...'
                    else:
                        short_fspath_path = filesystemPath

                    # Prepare the data tuple to be printed
                    fs_data = (
                        node,
                        short_path,
                        short_mount_path,
                        short_fspath_path,
                        fs.get('operSt', 'N/A'),
                        fs.get('capUtilized', 'N/A') + "%"
                    )

                    # Print the filesystem data
                    print("{:<15} {:<30} {:<30} {:<25} {:<15} {:<16}".format(*fs_data))

                # Printing End separation at the end of the output
                print("-" * len(apic_fs_header_line))

    # Method that will print all the Controllers Power Supply Info
    def printApicNodesPsuInfo(self, graph: nx.Graph) -> None:

        # Fabric Tuple to know if the Node device is a controller
        fabricController = ('controller')

        # Header for the APIC DIMMs table
        apic_psu_header_keys = ['Node', 'PSU ID', 'Descr', 'Model', 'HW Ver', 'Operational St', 'S/N', 'Vendor']
        apic_psu_header_line = "{:<12} {:<10} {:<16} {:<18} {:<10} {:<15} {:<13} {:<17}".format(*apic_psu_header_keys)

        header_text = " APIC PSUs Information "
        total_width = len(apic_psu_header_line)
        centered_header = header_text.center(total_width, '-')
        print("-" * len(apic_psu_header_line))
        print(centered_header)
        print("-" * len(apic_psu_header_line))
        print(apic_psu_header_line)
        print("-" * len(apic_psu_header_line))

        # Iterate through each node in the graph
        for node, attributes in graph.nodes(data=True):

            # Auxilear variable to compare the role in the if statement below
            role = attributes.get('role')

            # Check if the node is a controller (APIC) and has the 'apic_power_supplies' attribute
            if role is not None and role in fabricController and 'apic_power_supplies' in attributes and attributes['apic_power_supplies']:

                # Iterate through each filesystem entry for the Controller node
                for psu in attributes['apic_power_supplies']:

                    # Prepare the data tuple to be printed
                    psu_data = (
                        node,
                        psu.get('id', 'N/A'),
                        psu.get('descr', 'N/A'),
                        psu.get('model', 'N/A'),
                        psu.get('hwVer', 'N/A'),
                        psu.get('operSt', 'N/A'),
                        psu.get('ser', 'N/A'),
                        psu.get('vendor', 'N/A')
                    )

                    # Print the filesystem data
                    print("{:<12} {:<10} {:<16} {:<18} {:<10} {:<15} {:<13} {:<17}".format(*psu_data))

        # Printing End separation at the end of the output
        print("-" * len(apic_psu_header_line))

    # Method that will print all the Controllers FANs Info
    def printApicNodesFanInfo(self, graph: nx.Graph) -> None:

        # Fabric Tuple to know if the Node device is a controller
        fabricController = ('controller')

        # Header for the APIC DIMMs table
        apic_fan_header_keys = ['Node', 'FAN ID', 'Description', 'Operational St', 'Speed', 'Max Speed', 'Vendor']
        apic_fan_header_line = "{:<12} {:<8} {:<17} {:<15} {:<14} {:<13} {:<18}".format(*apic_fan_header_keys)

        header_text = " APIC FANs Information "
        total_width = len(apic_fan_header_line)
        centered_header = header_text.center(total_width, '-')
        print("-" * len(apic_fan_header_line))
        print(centered_header)
        print("-" * len(apic_fan_header_line))
        print(apic_fan_header_line)
        print("-" * len(apic_fan_header_line))

        # Iterate through each node in the graph
        for node, attributes in graph.nodes(data=True):

            # Auxilear variable to compare the role in the if statement below
            role = attributes.get('role')

            # Check if the node is a controller (APIC) and has the 'apic_fans' attribute
            if role is not None and role in fabricController and 'apic_fans' in attributes and attributes['apic_fans']:

                # Iterate through each filesystem entry for the Controller node
                for fan in attributes['apic_fans']:

                    # Prepare the data tuple to be printed
                    fan_data = (
                        node,
                        fan.get('id', 'N/A'),
                        fan.get('descr', 'N/A'),
                        fan.get('operSt', 'N/A'),
                        fan.get('speed', 'N/A'),
                        fan.get('maxSpeed', 'N/A'),
                        fan.get('vendor', 'N/A')
                    )

                    # Print the filesystem data
                    print("{:<12} {:<8} {:<17} {:<15} {:<14} {:<13} {:<18}".format(*fan_data))

        # Printing End separation at the end of the output
        print("-" * len(apic_fan_header_line))

    # Method that will print all the Controller Sensors Info
    def printApicNodesSensorInfo(self, graph: nx.Graph) -> None:

        # Fabric Tuple to know if the Node device is a controller
        fabricController = ('controller')

        # Header for the APIC Sensor table
        apic_sensor_header_keys = ['Node', 'Sensor ID', 'Sensor Type', 'Operational St', 'minor Thrshold', 'Major Thresh', 'Value', 'Vendor', 'Description']
        apic_sensor_header_line = "{:<12} {:<10} {:<13} {:<15} {:<16} {:<14} {:<10} {:<19} {:<49}".format(*apic_sensor_header_keys)

        header_text = " APIC Sensors Information "
        total_width = len(apic_sensor_header_line)
        centered_header = header_text.center(total_width, '-')
        print("-" * len(apic_sensor_header_line))
        print(centered_header)
        print("-" * len(apic_sensor_header_line))
        print(apic_sensor_header_line)
        print("-" * len(apic_sensor_header_line))

        # Iterate through each node in the graph
        for node, attributes in graph.nodes(data=True):

            # Auxilear variable to compare the role in the if statement below
            role = attributes.get('role')

            # Check if the node is a controller (APIC) and has the 'apic_sensor' attribute
            if role is not None and role in fabricController and 'apic_sensor' in attributes and attributes['apic_sensor']:

                # Iterate through each filesystem entry for the Controller node
                for sensor in attributes['apic_sensor']:

                    # Prepare the data tuple to be printed
                    sensor_data = (
                        node,
                        sensor.get('id', 'N/A'),
                        sensor.get('type', 'N/A'),
                        sensor.get('operSt', 'N/A'),
                        sensor.get('minorThresh', 'N/A'),
                        sensor.get('majorThresh', 'N/A'),
                        sensor.get('value', 'N/A'),
                        sensor.get('vendor', 'N/A'),
                        sensor.get('descr', 'N/A')
                    )

                    # Print the filesystem data
                    print("{:<12} {:<10} {:<13} {:<15} {:<16} {:<14} {:<10} {:<19} {:<49}".format(*sensor_data))

        # Printing End separation at the end of the output
        print("-" * len(apic_sensor_header_line))

    # Method that will print all the DIMMS info feching from the Controllers Node in the Graph
    def printApicNodesDimmsInfo(self, graph: nx.Graph) -> None:

        # Fabric Tuple to know if the Node device is a controller
        fabricController = ('controller')

        # Header for the APIC DIMMs table
        apic_dimm_header_keys = ['Node', 'DIMM ID', 'Acc', 'Cap', 'Model', 'Operational St', 'S/N', 'Type']
        apic_dimm_header_line = "{:<12} {:<10} {:<13} {:<10} {:<17} {:<15} {:<20} {:<10}".format(*apic_dimm_header_keys)

        header_text = " APIC DIMMs Information "
        total_width = len(apic_dimm_header_line)
        centered_header = header_text.center(total_width, '-')
        print("-" * len(apic_dimm_header_line))
        print(centered_header)
        print("-" * len(apic_dimm_header_line))
        print(apic_dimm_header_line)
        print("-" * len(apic_dimm_header_line))

        # Iterate through each node in the graph
        for node, attributes in graph.nodes(data=True):

            # Auxilear variable to compare the role in the if statement below
            role = attributes.get('role')

            # Check if the node is a controller (APIC) and has the 'apic_dimm' attribute
            if role is not None and role in fabricController and 'apic_dimm' in attributes and attributes['apic_dimm']:

                # Iterate through each filesystem entry for the Controller node
                for dimm in attributes['apic_dimm']:

                    # Prepare the data tuple to be printed
                    dimm_data = (
                        node,
                        dimm.get('id', 'N/A'),
                        dimm.get('acc', 'N/A'),
                        dimm.get('cap', 'N/A'),
                        dimm.get('model', 'N/A'),
                        dimm.get('operSt', 'N/A'),
                        dimm.get('ser', 'N/A'),
                        dimm.get('type', 'N/A')
                    )

                    # Print the filesystem data
                    print("{:<12} {:<10} {:<13} {:<10} {:<17} {:<15} {:<20} {:<10}".format(*dimm_data))

        # Printing End separation at the end of the output
        print("-" * len(apic_dimm_header_line))

    # Method that will print all the Aggregate Interfaces detected in the Controllers Node in the Graph
    def printApicNodesAggIntInfo(self, graph: nx.Graph) -> None:

        # Fabric Tuple to know if the Node device is a controller
        fabricController = ('controller')

        # Header for the APIC Physical Interfaces table
        apic_aggint_header_keys = ['Node', 'Agg Int ID', 'Int Name', 'Admin State', 'MTU','MPLS MTU', 'MAC Address']
        apic_aggint_header_line = "{:<12} {:<12} {:<13} {:<12} {:<6} {:<9} {:<17}".format(*apic_aggint_header_keys)

        header_text = " APIC Aggregate Interface Information "
        total_width = len(apic_aggint_header_line)
        centered_header = header_text.center(total_width, '-')
        print("-" * len(apic_aggint_header_line))
        print(centered_header)
        print("-" * len(apic_aggint_header_line))
        print(apic_aggint_header_line)
        print("-" * len(apic_aggint_header_line))

        # Iterate through each node in the graph
        for node, attributes in graph.nodes(data=True):

            # Auxilear variable to compare the role in the if statement below
            role = attributes.get('role')

            # Check if the node is a controller (APIC) and has the 'apic_aggint' attribute
            if role is not None and role in fabricController and 'apic_aggint' in attributes and attributes['apic_aggint']:

                # Iterate through each Aggregate Interface entry for the Controller node
                for aggint in attributes['apic_aggint']:

                    # Prepare the data tuple to be printed
                    aggint_data = (
                        node,
                        aggint.get('id', 'N/A'),
                        aggint.get('name', 'N/A'),
                        aggint.get('adminSt', 'N/A'),
                        aggint.get('mtu', 'N/A'),
                        aggint.get('mplsMtu', 'N/A'),
                        aggint.get('routerMac', 'N/A')
                    )

                    # Print the filesystem data
                    print("{:<12} {:<12} {:<13} {:<12} {:<6} {:<9} {:<17}".format(*aggint_data))

        # Printing End separation at the end of the output
        print("-" * len(apic_aggint_header_line))

    # Method that will print all the BBDD Sync Status from the Controllers Node in the Graph
    def printApicNodesBbddSyncStatusInfo(self, graph) -> None:

        # Fabric Tuple to know if the Node device is a controller
        fabricController = ('controller')

        # Header for the APIC Physical Interfaces table
        apic_bbddSync_header_keys = ['Node', 'APIC ID', 'POD ID', 'Health Status', 'Controller IP', 'Admin State','APIC Mode', 'Unique Identifier (UUID)', 'Oper State']
        apic_bbddSync_header_line = "{:<12} {:<8} {:<8} {:<15} {:<14} {:<12} {:<10} {:<37} {:<10}".format(*apic_bbddSync_header_keys)

        header_text = " APIC BBDD Sync Status Information "
        total_width = len(apic_bbddSync_header_line)
        centered_header = header_text.center(total_width, '-')
        print("-" * len(apic_bbddSync_header_line))
        print(centered_header)
        print("-" * len(apic_bbddSync_header_line))
        print(apic_bbddSync_header_line)
        print("-" * len(apic_bbddSync_header_line))

        # Iterate through each node in the graph
        for node, attributes in graph.nodes(data=True):

            # Auxilear variable to compare the role in the if statement below
            role = attributes.get('role')

            # Check if the node is a controller (APIC) and has the 'apic_bbdd_sync' attribute
            if role is not None and role in fabricController and 'apic_bbdd_sync' in attributes and attributes['apic_bbdd_sync']:

                # Iterate through each BBDD entry for the Controller node
                for bbdd in attributes['apic_bbdd_sync']:

                    # Prepare the data tuple to be printed
                    bbdd_data = (
                        node,
                        bbdd.get('id', 'N/A'),
                        bbdd.get('podId', 'N/A'),
                        bbdd.get('health', 'N/A'),
                        bbdd.get('addr', 'N/A'),
                        bbdd.get('adminSt', 'N/A'),
                        bbdd.get('apicMode', 'N/A'),
                        bbdd.get('chassis', 'N/A'),
                        bbdd.get('operSt', 'N/A')
                    )

                    # Print the filesystem data
                    print("{:<12} {:<8} {:<8} {:<15} {:<14} {:<12} {:<10} {:<37} {:<10}".format(*bbdd_data))

        # Printing End separation at the end of the output
        print("-" * len(apic_bbddSync_header_line))

    # Method that will print all the Physical Interfaces detected in the Controllers Node in the Graph
    def printApicNodesPhyIntInfo(self, graph: nx.Graph) -> None:

        # Fabric Tuple to know if the Node device is a controller
        fabricController = ('controller')

        # Header for the APIC Physical Interfaces table
        apic_phyint_header_keys = ['Node', 'Int ID', 'Admin State', 'Operational St', 'Speed','Mode', 'MTU', 'Medium']
        apic_phyint_header_line = "{:<12} {:<10} {:<13} {:<15} {:<7} {:<9} {:<7} {:<14}".format(*apic_phyint_header_keys)

        header_text = " APIC Physical Interface Information "
        total_width = len(apic_phyint_header_line)
        centered_header = header_text.center(total_width, '-')
        print("-" * len(apic_phyint_header_line))
        print(centered_header)
        print("-" * len(apic_phyint_header_line))
        print(apic_phyint_header_line)
        print("-" * len(apic_phyint_header_line))

        # Iterate through each node in the graph
        for node, attributes in graph.nodes(data=True):

            # Auxilear variable to compare the role in the if statement below
            role = attributes.get('role')

            # Check if the node is a controller (APIC) and has the 'apic_phyint' attribute
            if role is not None and role in fabricController and 'apic_phyint' in attributes and attributes['apic_phyint']:

                # Iterate through each Physical Interface entry for the Controller node
                for phyint in attributes['apic_phyint']:

                    # Prepare the data tuple to be printed
                    phyint_data = (
                        node,
                        phyint.get('id', 'N/A'),
                        phyint.get('adminSt', 'N/A'),
                        phyint.get('operSt', 'N/A'),
                        phyint.get('speed', 'N/A'),
                        phyint.get('mode', 'N/A'),
                        phyint.get('mtu', 'N/A'),
                        phyint.get('medium', 'N/A')
                    )

                    # Print the filesystem data
                    print("{:<12} {:<10} {:<13} {:<15} {:<7} {:<9} {:<7} {:<14}".format(*phyint_data))

        # Printing End separation at the end of the output
        print("-" * len(apic_phyint_header_line))

    #########################
    # General Print Methods #
    #########################

    # General Method that print all the General Fabric Attributes from the Fabric Edges in the Graph
    def printAllFabricEdgesAttributesCli(self, graph: nx.Graph) -> None:

        # For each Edge in the Graph, if the interface is the Type Fabric
        # We print all the counter found in the Dict
        for edge1, edge2, data in graph.edges(data=True):
            if data:
                if not data.get('downlink'):
                    self.__privatePrintFabricEdgesAttributesCli(edge1, edge2, data)

    # General Method that print all the EPG Nodes in the Graph
    def printAllNetworkDevicesNodesCli(self, graph: nx.Graph) -> None:

        # Header for the Fabric Attributes table
        epg_header_keys = [' Index ', 'Network Device Name', 'Lead Name', 'Leaf Int', 'Oper Mode', 'Oper Speed', 'Oper Vlans', 'lastLinkStChg']
        epg_header_line = " {:<9} {:<34} {:<11} {:<9} {:<13} {:<13} {:<40} {:<40}".format(*epg_header_keys)

        # Header content declaration and print
        header_text = " Network Devices in the Graph "
        total_width = len(epg_header_line)
        centered_header = header_text.center(total_width, '-')
        print("-" * len(epg_header_line))
        print(centered_header)
        print("-" * len(epg_header_line))
        print(epg_header_line)
        print("-" * len(epg_header_line))

        # Auxilear variable to print all the Exter connected to the Fabric
        index = 1

        # Iterate through each node in the graph
        for edge1, edge2, attributes in graph.edges(data=True):

            # if the Node has no attributes means
            # is a EPG Node
            if attributes.get('downlink'):

                # Prepare the data tuple to be printed
                attr_data = (
                    index,
                    edge2,
                    edge1,
                    attributes.get('leaf_int', 'N/A'),
                    attributes.get('operMode', 'N/A'),
                    attributes.get('operSpeed', 'N/A'),
                    attributes.get('operVlans', 'N/A'),
                    attributes.get('lastLinkStChg', 'N/A')
                )

                # Increasing auxilear var by 1
                index += 1

                # Print the filesystem data
                print("   {:<7} {:<34} {:<11} {:<9} {:<13} {:<13} {:<40} {:<40}".format(*attr_data))

        # Printing End separation at the end of the output
        print("-" * len(epg_header_line))

    # General Method that print all the General Fabric Attributes from the Fabric Nodes in the Graph
    def printAllFabricNodesAttributesCli(self, graph: nx.Graph) -> None:

        # Auxilear Tuples for Resources feching depending on device role
        fabric_role = {'leaf', 'spine', 'controller'}

        # Header for the Fabric Attributes table
        apic_fa_header_keys = ['Node', 'Fabric ID', 'Model', 'IP Address', 'Version', 'S/N', 'Fabric State', 'Role', 'User Domain', 'Vendor']
        apic_fa_header_line = "{:<12} {:<10} {:<17} {:<12} {:<16} {:<13} {:<14} {:<12} {:<12} {:<18}".format(*apic_fa_header_keys)

        header_text = " Fabric Node Vector "
        total_width = len(apic_fa_header_line)
        centered_header = header_text.center(total_width, '-')
        print("-" * len(apic_fa_header_line))
        print(centered_header)
        print("-" * len(apic_fa_header_line))
        print(apic_fa_header_line)
        print("-" * len(apic_fa_header_line))

        # Iterate through each node in the graph
        for node, attributes in graph.nodes(data=True):

            # Auxilear variable to compare the role in the if statement below
            role_type = attributes.get('role')

            # Check if the node is a controller (APIC) and has the 'apic_sensor' attribute
            if role_type is not None and role_type in fabric_role:

                # Prepare the data tuple to be printed
                attr_data = (
                    node,
                    attributes.get('id','N/A'),
                    attributes.get('model', 'N/A'),
                    attributes.get('address', 'N/A'),
                    attributes.get('version', 'N/A'),
                    attributes.get('serial', 'N/A'),
                    attributes.get('fabricSt', 'N/A'),
                    attributes.get('role', 'N/A'),
                    attributes.get('userdom', 'N/A'),
                    attributes.get('vendor', 'N/A')
                )

                # Print the filesystem data
                print("{:<12} {:<10} {:<17} {:<12} {:<16} {:<13} {:<14} {:<12} {:<12} {:<18}".format(*attr_data))

        # Printing End separation at the end of the output
        print("-" * len(apic_fa_header_line))

    # General Method that print all the attributes detected in the Edge List
    def printingAllEdgeAttributes(self, graph: nx.Graph) -> None:

        # Section for validating edge attributes
        print("\nValidating Edge Attributes:")
        for u, v, data in graph.edges(data=True):
            print(f"Edge from {u} to {v} has attributes: {data}")

    # General Method that receive a graph from main program and print the results in the CLI
    def printingNodeAttributes(self, graph: nx.Graph) -> None:

        # Auxilear Tuples for Resources feching depending on device role
        switch_role = {'leaf', 'spine'}

        # For each Node attribute, we print the info in the CLI
        for node, attributes in graph.nodes(data=True):

            # Printing Node Name
            print("Node: " + node)

            # Feching all the attributes contained in the Dict
            for key, attr in attributes.items():

                # Avoiding print empty attributes
                if attr != "":

                    #####################
                    # Printing PSU Info #
                    #####################

                    if key == 'psus':

                        # We only enter if the node role is a switch
                        if attributes.get('role') in switch_role:

                            # Printing the key value for each data in the PSU ID
                            print(" - " + key + ":")

                            # For each Data in the PSU List, we print each value
                            for psu in attr:

                                # Printing the key value for each data in the PSU ID
                                print("   - psuID: " + str(psu.get('id', 'N/A')))

                                # For each Data in the PSU List, we print in the terminal
                                for psuKey, psuAttr in psu.items():
                                    if psuKey != 'id':
                                        if psuAttr != "":
                                            print("      - " + psuKey + ": " + str(psuAttr))

                    #############################
                    # Printing Suppervisor Info #
                    #############################

                    elif key == 'supervisors':

                        # We only enter if the node role is a switch
                        if attributes.get('role') in switch_role:

                            # Printing Supervisor section in the CLI
                            print(" - " + key + ":")

                            # We print all the suppervisors detected in the switch
                            for sup in attr:

                                # Printing Supervisor ID
                                print("   - supID: " + str(sup.get('id', 'N/A')))

                                # For each element in the suppervisor list, we print in the cli
                                for supKey, supAttr in sup.items():
                                    if supKey != 'id':
                                        if supAttr != "":
                                            print("      - " + supKey + ": " + str(supAttr))

                    ###############################
                    # Printing Fabric Module Info #
                    ###############################

                    elif key == 'fabric_modules':

                        # Printing Fabric Module section in the CLI
                        print(" - " + key + ":")

                        # We print all the Fabric Module detected in the switch
                        for fm in attr:

                            # Printing Fabric Module ID
                            print("   - fmID: " + str(fm.get('id', 'N/A')))

                            # For each element in the suppervisor list, we print in the cli
                            for fmKey, fmAttr in fm.items():
                                if supKey != 'id':
                                    if fmAttr != "":
                                        print("      - " + fmKey + ": " + str(fmAttr))

                    ##########################################
                    # Printing System Controller Module Info #
                    ##########################################

                    elif key == 'system_controller':

                        # Printing System Controller Module section in the CLI
                        print(" - " + key + ":")

                        # We print all the System Controller Module detected in the switch
                        for sc in attr:

                            # Printing Fabric Module ID
                            print("   - scID: " + str(sc.get('id', 'N/A')))

                            # For each element in the suppervisor list, we print in the cli
                            for scKey, scAttr in sc.items():
                                if scKey != 'id':
                                    if scAttr != "":
                                        print("      - " + scKey + ": " + str(scAttr))

                    ##################################
                    # Printing Linecards Module Info #
                    ##################################

                    elif key == 'linecard':

                        # Printing Linecard Module section in the CLI
                        print(" - " + key + ":")

                        # We print all the Linecards Module detected in the switch
                        for lc in attr:

                            # Printing Fabric Module ID
                            print("   - lcID: " + str(lc.get('id', 'N/A')))

                            # For each element in the linecard list, we print in the cli
                            for lcKey, lcAttr in lc.items():
                                if lcKey != 'id':
                                    if lcAttr != "":
                                        print("      - " + lcKey + ": " + str(lcAttr))

                    ############################
                    # Printing Interfaces Info #
                    ############################

                    elif key == 'interfaces':

                        # Printing interfaces section in the CLI
                        print(" - " + key + ":")

                        # We print all the interfaces Module detected in the switch
                        for interface in attr:

                            # Printing interfaces ID
                            print("   - Interface ID: " + str(interface.get('id', 'N/A')))

                            # For each element in the interfaces list, we print in the cli
                            for interfaceKey, interfaceAttr in interface.items():
                                if interfaceKey != 'id':
                                    if interfaceAttr != "":
                                        print("      - " + interfaceKey + ": " + str(interfaceAttr))

                    #######################################
                    # Printing Operational Interface Info #
                    #######################################

                    elif key == 'opt_interfaces':

                        # Printing Operational Interfaces section in the CLI
                        print(" - " + key + ":")

                        # We print all the interfaces
                        for interface in attr:

                            # Get the interface ID. Note the key is 'intID', not 'id'.
                            int_id = interface.get('intID', 'N/A')
                            print("   - Opt Interface ID: " + str(int_id))

                            # Access the 'operSt' dictionary and iterate through its key-value pairs
                            oper_status = interface.get('operSt', {})
                            for key, value in oper_status.items():
                                # Check if the value is not an empty string or None before printing
                                if value:
                                    print("      - " + key + ": " + str(value))

                    ################################
                    # Printing SFP Interfaces Info #
                    ################################

                    elif key == 'sfp':

                        # Printing SFP Interfaces section in the CLI
                        print(" - " + key + ":")

                        # We print all the SFP Interfaces detected in the switch
                        for interfaceSfp in attr:

                            # Printing Interfaces ID
                            print("   - Interface ID: " + str(interfaceSfp.get('int_id', 'N/A')))

                            # For each element in the SFP Interfaces list, we print in the cli
                            for interfaceSfpKey, interfaceSfpAttr in interfaceSfp.items():
                                if interfaceSfpKey != 'int_id':
                                    if interfaceSfpAttr != "":
                                        print("      - " + interfaceSfpKey + ": " + str(interfaceSfpAttr))

                    ############################
                    # Printing Faults Detected #
                    ############################

                    elif key == 'faults':

                        # Printing faults section in the CLI
                        print(" - " + key + ":")

                        # We print all the faults Module detected in the switch
                        for fault in attr:

                            # Printing Fabric Module ID
                            print("   - Fault ID: " + str(fault.get('code', 'N/A')))

                            # For each element in the linecard list, we print in the cli
                            for fauKey, fauAttr in fault.items():
                                if fauKey != 'code':
                                    if fauAttr != "":
                                        print("      - " + fauKey + ": " + str(fauAttr))

                    #####################################
                    # Printing filesystem info detected #
                    #####################################

                    elif key == 'filesystem':

                        # Printing Filesystem section in the CLI
                        print(" - " + key + ":")

                        # We print all the directories detected in the Filesystem
                        for filesystem in attr:

                            # Sorted list with dictionary content (return a list)
                            sortDict = sorted(filesystem)

                            # Printing Directory name
                            print("   - dirName: " + str(filesystem.get('path', 'N/A')))

                            # For each element in the linecard list, we print in the cli
                            for dirKey in sortDict:
                                if dirKey != 'code' and filesystem[dirKey] != "":
                                    print("      - " + dirKey + ": " + str(filesystem[dirKey]))

                    #######################
                    #     APIC Section    #
                    #######################

                    #######################################
                    # Printing Power Supply info Detected #
                    #######################################

                    elif key == 'apic_power_supplies':

                        # Printing power supplies section in the CLI
                        print(" - " + key + ":")

                        # We print all the Power Supply Module detected in the switch
                        for ps in attr:

                            # Printing Power Supply ID
                            print("   - Power Supply ID: " + str(ps.get('id', 'N/A')))

                            # For each element in the Power Supply list, we print in the cli
                            for psKey, psAttr in ps.items():
                                if psKey != 'code':
                                    if psAttr != "":
                                        print("      - " + psKey + ": " + str(psAttr))

                    #####################################
                    # Printing NTP Server Info Detected #
                    #####################################

                    elif key == 'apic_ntp':

                        # Printing NTP Section in the CLI
                        print(" - " + key + ":")

                        # We print all the NTP Server detected in the switch
                        for ntp in attr:

                            # Printing Power Supply ID
                            print("   - NTP Server: " + str(ntp.get('remote', 'N/A')))

                            # For each element in the Power Supply list, we print the info in the CLI
                            for ntpKey, ntpAttr in ntp.items():
                                if ntpKey != 'remote':
                                    if ntpAttr != "":
                                        print("      - " + ntpKey + ": " + str(ntpAttr))

                    ###########################################
                    # Printing BBDD Sync Status Info Detected #
                    ###########################################

                    elif key == 'apic_bbdd_sync':

                        # Printing BBDD Sync Status Section in the CLI
                        print(" - " + key + ":")

                        # We print all the BBDD Sync Status detected in the switch
                        for sync in attr:

                            # Printing APIC ID
                            print("   - APIC ID: " + str(sync.get('id', 'N/A')))

                            # For each element in the BBDD Sync Status, we print the info in the CLI
                            for syncKey, syncAttr in sync.items():
                                if syncKey != 'id':
                                    if syncAttr != "":
                                        print("      - " + syncKey + ": " + str(syncAttr))

                    ###############################
                    # Printing FANs info Detected #
                    ###############################

                    elif key == 'apic_fans':

                        # Printing FANs section in the CLI
                        print(" - " + key + ":")

                        # We print all the FANs Module detected in the switch
                        for ps in attr:

                            # Printing FAN ID
                            print("   - Fan ID: " + str(ps.get('id', 'N/A')))

                            # For each element in the FANs list, we print in the cli
                            for psKey, psAttr in ps.items():
                                if psAttr != "":
                                    print("      - " + psKey + ": " + str(psAttr))

                    ##################################
                    # Printing Sensors info Detected #
                    ##################################

                    elif key == 'apic_sensor':

                        # Printing Sensor section in the CLI
                        print(" - " + key + ":")

                        # We print all the Sensor Module detected in the switch
                        for sensor in attr:

                            # Printing Sensor ID
                            print("   - Sensor ID: " + str(sensor.get('id', 'N/A')))


                            # For each element in the Sensor list, we print in the cli
                            for sensorKey, sensorAttr in sensor.items():
                                if sensorAttr != "":
                                    print("      - " + sensorKey + ": " + str(sensorAttr))

                    ###############################
                    # Printing DIMM info Detected #
                    ###############################

                    elif key == 'apic_dimm':

                        # Printing DIMM section in the CLI
                        print(" - " + key + ":")

                        # We print all the DIMMs detected in the switch
                        for dimm in attr:

                            # Printing DIMM ID
                            print("   - DIMM ID: " + str(dimm.get('id', 'N/A')))

                            # For each element in the DIMM list, we print in the cli
                            for dimmKey, dimmAttr in dimm.items():
                                if dimmAttr != "":
                                    print("      - " + dimmKey + ": " + str(dimmAttr))

                    #####################################
                    # Printing FileSystem info Detected #
                    #####################################

                    elif key == 'apic_filesystem':

                        # Printing FileSystem section in the CLI
                        print(" - " + key + ":")

                        # We print all the FileSystem detected in the switch
                        for fs in attr:

                            # Printing FileSystem Path Name
                            print("   - FileSystem Path Name: " + str(fs.get('name', 'N/A')))

                            # For each element in the FileSystem list, we print in the cli
                            for fsKey, fsAttr in fs.items():
                                if fsAttr != "":
                                    print("      - " + fsKey + ": " + str(fsAttr))

                    #############################################
                    # Printing Physical Interface info Detected #
                    #############################################

                    elif key == 'apic_phyint':

                        # Printing Physical Interface section in the CLI
                        print(" - " + key + ":")

                        # We print all the Physical Interface detected in the switch
                        for phyint in attr:

                            # Printing Physical Interface Path Name
                            print("   - Physical Interface ID: " + str(phyint.get('id', 'N/A')))

                            # For each element in the Physical Interface list, we print in the cli
                            for phyintKey, phyintAttr in phyint.items():
                                if phyintAttr != "":
                                    print("      - " + phyintKey + ": " + str(phyintAttr))

                    ##############################################
                    # Printing Aggregate Interface info Detected #
                    ##############################################

                    elif key == 'apic_aggint':

                        # Printing Aggregate Interface section in the CLI
                        print(" - " + key + ":")

                        # We print all the Aggregate Interface detected in the switch
                        for aggint in attr:

                            # Printing Aggregate Interface Path Name
                            print("   - Aggregate Interface ID: " + str(aggint.get('id', 'N/A')))

                            # For each element in the Aggregate Interface list, we print in the cli
                            for aggintKey, aggintAttr in aggint.items():
                                if aggintAttr != "":
                                    print("      - " + aggintKey + ": " + str(aggintAttr))

                    else:
                        # Printing Attribute name and value for non-list attributes
                        print(" - " + key + ": " + str(attr))

    ##################################
    # Specific Methods for Edge info #
    ##################################

    # General Method that prints fabric edge links reporting errors in the interface counters
    def printFabricEdgesWithErrorsCli(self, graph: nx.Graph) -> None:

        # Define error keys to check in both source and destination interface counters
        error_keys = [
            'source_cRCAlignErrors', 'source_collisions', 'source_dropEvents',
            'source_fragments', 'source_jabbers', 'source_undersizePkts',
            'source_oversizePkts', 'source_rxGiantPkts', 'source_rxOversizePkts',
            'source_txGiantPkts', 'source_txOversizePkts', 'source_interface_operLastErrors',
            'dest_cRCAlignErrors', 'dest_collisions', 'dest_dropEvents',
            'dest_fragments', 'dest_jabbers', 'dest_undersizePkts',
            'dest_oversizePkts', 'dest_rxGiantPkts', 'dest_rxOversizePkts',
            'dest_txGiantPkts', 'dest_txOversizePkts', 'dest_interface_operLastErrors',
        ]

        # Header for the error-focused table
        header_keys = ['Source Node', 'Source Int', 'Dest Node', 'Dest Int', 'Errors Detected?']
        header_line = "{:<15} {:<12} {:<15} {:<12} {:<20}".format(*header_keys)

        # Print header
        header_text = " Fabric Edges Reporting Interface Errors "
        total_width = len(header_line)
        centered_header = header_text.center(total_width, '-')
        print("-" * total_width)
        print(centered_header)
        print("-" * total_width)
        print(header_line)
        print("-" * total_width)

        # Flag to track if any error was found
        errors_found = False

        # Iterate through all edges
        for u, v, data in graph.edges(data=True):

            # Skip downlink edges (focus on fabric interconnects)
            if data.get('downlink'):
                continue

            # Check if any error counter has a non-zero/non-None value
            has_errors = False
            for key in error_keys:
                # Retrieve the value, safely converting it to an integer, defaulting to 0
                try:
                    # Treat 'N/A' or missing keys as 0
                    value = int(data.get(key, 0) or 0)
                except ValueError:
                    # Handle cases where value might be a non-numeric string like "N/A"
                    value = 0

                # Check for "lastErrors" value being non-zero/non-empty
                if 'operLastErrors' in key and data.get(key) not in [None, '0', '', 'N/A']:
                    has_errors = True
                    break

                # Check for counter values being greater than zero
                if value > 0:
                    has_errors = True
                    break

            if has_errors:
                errors_found = True

                # Prepare the data tuple to be printed
                edge_data = (
                    u,
                    data.get('source_interface_id', 'N/A'),
                    v,
                    data.get('dest_interface_id', 'N/A'),
                    "YES (Review Counters)"
                )

                # Print the edge data
                print("{:<15} {:<12} {:<15} {:<12} {:<20}".format(*edge_data))

        # Print message if no errors were found
        if not errors_found:
            print("{:<64}".format("No fabric edges reported interface errors."))

        # Print end separation
        print("-" * total_width)

    # Method that prints fabric edge links reporting errors with detailed counter information
    def printFabricEdgesWithErrorDetailsCli(self, graph: nx.Graph) -> None:

        # Define error keys to check (same as before)
        error_keys = [
            'source_cRCAlignErrors', 'source_collisions', 'source_dropEvents',
            'source_fragments', 'source_jabbers', 'source_undersizePkts',
            'source_oversizePkts', 'source_rxGiantPkts', 'source_rxOversizePkts',
            'source_txGiantPkts', 'source_txOversizePkts', 'source_interface_operLastErrors',
            'dest_cRCAlignErrors', 'dest_collisions', 'dest_dropEvents',
            'dest_fragments', 'dest_jabbers', 'dest_undersizePkts',
            'dest_oversizePkts', 'dest_rxGiantPkts', 'dest_rxOversizePkts',
            'dest_txGiantPkts', 'dest_txOversizePkts', 'dest_interface_operLastErrors',
        ]

        # Flag to track if any error was found
        errors_found = False

        # Iterate through all edges
        for u, v, data in graph.edges(data=True):

            # Skip downlink edges (focus on fabric interconnects)
            if data.get('downlink'):
                continue

            # Check if any error counter has a non-zero/non-None value
            has_errors = False
            error_details = {} # Store non-zero errors for printing

            for key in error_keys:
                raw_value = data.get(key)
                value = 0

                # Check for "lastErrors" value being non-zero/non-empty string
                if 'operLastErrors' in key:
                    if raw_value not in [None, '0', '', 'N/A']:
                        has_errors = True
                        error_details[key] = raw_value

                # Check for counter values being greater than zero
                else:
                    try:
                        value = int(raw_value or 0)
                    except (ValueError, TypeError):
                        value = 0 # If it's a non-numeric string, treat as 0 for this check

                    if value > 0:
                        has_errors = True
                        error_details[key] = value

            if has_errors:
                errors_found = True

                # Print the summary header for this specific edge
                summary_header = f" ERRORS DETECTED on Edge: {u} ({data.get('source_interface_id', 'N/A')}) <-> {v} ({data.get('dest_interface_id', 'N/A')}) "
                summary_line_width = 80 # Fixed width for this sub-table
                print("\n" + "#" * summary_line_width)
                print(summary_header.center(summary_line_width, '#'))
                print("#" * summary_line_width)

                # Prepare and print the detailed error table

                # Keys to map source/dest prefixes to clean column headers
                # (Attribute, Source Key, Destination Key)
                printable_error_map = [
                    ("CRC/Align Errors", 'source_cRCAlignErrors', 'dest_cRCAlignErrors'),
                    ("Collisions", 'source_collisions', 'dest_collisions'),
                    ("Drop Events", 'source_dropEvents', 'dest_dropEvents'),
                    ("Fragments", 'source_fragments', 'dest_fragments'),
                    ("Jabbers", 'source_jabbers', 'dest_jabbers'),
                    ("Undersize Pkts", 'source_undersizePkts', 'dest_undersizePkts'),
                    ("Oversize Pkts", 'source_oversizePkts', 'dest_oversizePkts'),
                    ("Rx Giant Pkts", 'source_rxGiantPkts', 'dest_rxGiantPkts'),
                    ("Rx Oversize Pkts", 'source_rxOversizePkts', 'dest_rxOversizePkts'),
                    ("Tx Giant Pkts", 'source_txGiantPkts', 'dest_txGiantPkts'),
                    ("Tx Oversize Pkts", 'source_txOversizePkts', 'dest_txOversizePkts'),
                    ("Last Errors (Text)", 'source_interface_operLastErrors', 'dest_interface_operLastErrors'),
                ]

                # Detailed table header
                detail_header_keys = ['Error Type', f'Source: {u}', f'Dest: {v}']
                detail_header_line = "{:<30} {:<24} {:<24}".format(*detail_header_keys)

                print(detail_header_line)
                print("-" * summary_line_width)

                # Print details for non-zero errors
                for attr_name, src_key, dest_key in printable_error_map:
                    src_val = error_details.get(src_key)
                    dest_val = error_details.get(dest_key)

                    # Only print rows where at least one side has a non-zero/non-empty error
                    if src_val is not None or dest_val is not None:
                        # Convert number to string, format "N/A" if None
                        src_display = str(src_val) if src_val is not None else "N/A"
                        dest_display = str(dest_val) if dest_val is not None else "N/A"

                        print("{:<30} {:<24} {:<24}".format(attr_name, src_display, dest_display))

                print("-" * summary_line_width)

        # Print overall status at the end
        if not errors_found:
            print("\n" + "-" * summary_line_width)
            print("No fabric edges reported interface errors with non-zero counters.".center(summary_line_width))
            print("-" * summary_line_width)

    ########################
    # Tenant Print Methods #
    ########################

    # Method that will print all the Tenants and their immediate children (like APs and EPGs)
    def printFabricTenantInfo(self, graph: nx.Graph) -> None:

        # Look for the dedicated Fabric Root Node where global config is stored
        tenant_root_node = next((data for node, data in graph.nodes(data=True) if node == "Fabric_Config_Root"), None)

        if not tenant_root_node or not tenant_root_node.get('tenants'):
            print("❌ No Tenant Configuration data found in the graph (Fabric_Config_Root node).")
            if tenant_root_node and tenant_root_node.get('error'):
                 print(f"Error encountered during fetch: {tenant_root_node['error']}")
            print("-" * 80)
            return

        print("-" * 80)
        print(" Fabric Tenant Configuration Summary ".center(80, '-'))
        print("-" * 80)

        # The 'tenants' attribute contains a list of objects, one for each fvTenant
        all_tenants = tenant_root_node.get('tenants', [])

        if not all_tenants:
            print("No Tenants configured in the fabric.")

        for tenant_obj in all_tenants:
            # Safely navigate to the tenant attributes
            tenant_attr = tenant_obj.get('fvTenant', {}).get('attributes', {})
            tenant_name = tenant_attr.get('name', 'N/A')

            # 💡 NEW: Skip the default "common" and "mgmt" tenants for cleaner output
            if tenant_name in ['mgmt', 'common', 'N/A']:
                continue

            print("\n" + f" Tenant: {tenant_name} ".center(80, '='))
            print(f"  |-> Name Alias: {tenant_attr.get('nameAlias', 'N/A')}")
            print(f"  |-> Dn: uni/tn-{tenant_name}")

            # Initialize counters for this tenant
            ap_count = 0
            epg_count = 0
            l3out_count = 0
            vrf_count = 0 # 💡 NEW counter for VRFs
            other_children = 0

            # Get the list of direct children objects under the fvTenant
            children = tenant_obj.get('fvTenant', {}).get('children', [])

            for child in children:

                # Check for Application Profiles (fvAp)
                if 'fvAp' in child:
                    ap_count += 1
                    ap_attr = child['fvAp']['attributes']
                    ap_name = ap_attr.get('name', 'N/A')
                    print(f"  |--- Application Profile: {ap_name}")

                    # Check for EPGs (fvAEPg) inside the Application Profile
                    ap_children = child['fvAp'].get('children', [])
                    for ap_child in ap_children:
                        if 'fvAEPg' in ap_child:
                            epg_count += 1
                            epg_name = ap_child['fvAEPg']['attributes'].get('name', 'N/A')
                            print(f"  |-----> EPG: {epg_name} (DN: {ap_child['fvAEPg']['attributes'].get('dn')})")
                        # You can add logic here to parse Contracts (vzBrCP) or other objects if needed.

                # Check for L3Outs (l3extOut)
                elif 'l3extOut' in child:
                    l3out_count += 1
                    l3out_name = child['l3extOut']['attributes'].get('name', 'N/A')
                    print(f"  |--- L3Out: {l3out_name} (DN: {child['l3extOut']['attributes'].get('dn')})")

                # 💡 NEW: Check for VRFs (fvCtx)
                elif 'fvCtx' in child:
                    vrf_count += 1
                    vrf_name = child['fvCtx']['attributes'].get('name', 'N/A')
                    print(f"  |--- VRF (Context): {vrf_name} (DN: {child['fvCtx']['attributes'].get('dn')})")

                # Count other top-level children (e.g., vzBrCP/contracts, faultInst)
                else:
                    other_children += 1

            print(f"\n  Summary for {tenant_name}:")
            print(f"  - Total Application Profiles: {ap_count}")
            print(f"  - Total EPGs Found: {epg_count}")
            print(f"  - Total L3Outs Found: {l3out_count}")
            print(f"  - Total VRFs Found: {vrf_count}") # 💡 NEW VRF line
            print(f"  - Other top-level objects: {other_children}")

        print("\n" + "=" * 80)

    # Method that prints a simple list of all EPGs detected, organized by Tenant and Application Profile.
    def printTenantEpgList(self, graph: nx.Graph) -> None:

        # Look for the dedicated Fabric Root Node where global config is stored
        tenant_root_node = next((data for node, data in graph.nodes(data=True) if node == "Fabric_Config_Root"), None)

        if not tenant_root_node or not tenant_root_node.get('tenants'):
            print("❌ No Tenant Configuration data found in the graph (Fabric_Config_Root node).")
            if tenant_root_node and tenant_root_node.get('error'):
                 print(f"Error encountered during fetch: {tenant_root_node['error']}")
            print("-" * 80)
            return

        print("-" * 80)
        print(" EPG List per Tenant and Application Profile ".center(80, '-'))
        print("-" * 80)

        all_tenants = tenant_root_node.get('tenants', [])

        if not all_tenants:
            print("No Tenants configured in the fabric.")

        epgs_found = 0

        for tenant_obj in all_tenants:
            # 1. Get Tenant Info
            tenant_attr = tenant_obj.get('fvTenant', {}).get('attributes', {})
            tenant_name = tenant_attr.get('name', 'N/A')

            # Skip the default tenants for a focused list
            if tenant_name in ['mgmt', 'common', 'N/A']:
                continue

            print(f"\n--- TENANT: {tenant_name} ({tenant_attr.get('nameAlias', 'N/A')}) ---")

            # 2. Iterate over direct children (looking for Application Profiles)
            children = tenant_obj.get('fvTenant', {}).get('children', [])

            tenant_has_apgs = False

            for child in children:

                # Check for Application Profiles (fvAp)
                if 'fvAp' in child:
                    tenant_has_apgs = True
                    ap_attr = child['fvAp']['attributes']
                    ap_name = ap_attr.get('name', 'N/A')

                    print(f"  |-> Application Profile: {ap_name}")

                    # 3. Iterate over children of the Application Profile (looking for EPGs)
                    ap_children = child['fvAp'].get('children', [])

                    ap_has_epgs = False

                    for ap_child in ap_children:
                        if 'fvAEPg' in ap_child:
                            ap_has_epgs = True
                            epgs_found += 1
                            epg_attr = ap_child['fvAEPg']['attributes']
                            epg_name = epg_attr.get('name', 'N/A')
                            epg_pcTag = epg_attr.get('pcTag', 'N/A')

                            print(f"    |---> EPG: {epg_name} (PC Tag: {epg_pcTag})")

                    if not ap_has_epgs:
                         print("    |---> No EPGs found in this Application Profile.")

            if not tenant_has_apgs:
                 print("  |-> No Application Profiles found.")

        print("\n" + "=" * 80)
        print(f"Total EPGs found across custom tenants: {epgs_found}")
        print("=" * 80)

    # Method that prints full details for all EPGs, mirroring the 'show epg detail' command structure.
    def printEpgDetails(self, graph: nx.Graph) -> None:

        # Look for the dedicated Fabric Root Node
        tenant_root_node = next((data for node, data in graph.nodes(data=True) if node == "Fabric_Config_Root"), None)

        if not tenant_root_node or not tenant_root_node.get('tenants'):
            print("❌ No Tenant Configuration data found in the graph (Fabric_Config_Root node).")
            if tenant_root_node and tenant_root_node.get('error'):
                 print(f"Error encountered during fetch: {tenant_root_node['error']}")
            print("-" * 80)
            return

        print("-" * 100)
        print(" FULL EPG CONFIGURATION DETAILS ".center(100, '='))
        print("-" * 100)

        all_tenants = tenant_root_node.get('tenants', [])

        if not all_tenants:
            print("No Tenants configured in the fabric.")
            return

        for tenant_obj in all_tenants:
            tenant_attr = tenant_obj.get('fvTenant', {}).get('attributes', {})
            tenant_name = tenant_attr.get('name', 'N/A')

            if tenant_name in ['mgmt', 'common', 'N/A']:
                continue

            # ----------------------------------------------------------------------
            # Start EPG Search within Tenant
            # ----------------------------------------------------------------------
            tenant_children = tenant_obj.get('fvTenant', {}).get('children', [])

            for ap_child in tenant_children:
                if 'fvAp' in ap_child:
                    ap_name = ap_child['fvAp']['attributes'].get('name', 'N/A')
                    ap_epgs = ap_child['fvAp'].get('children', [])

                    for epg_child in ap_epgs:
                        if 'fvAEPg' in epg_child:
                            epg_obj = epg_child['fvAEPg']
                            epg_attr = epg_obj.get('attributes', {})
                            epg_name = epg_attr.get('name', 'N/A')
                            epg_children = epg_obj.get('children', [])

                            # --- 1. EPG Header ---
                            print("\n" + "#" * 90)
                            print(f" EPG: {epg_name} ({tenant_name}/{ap_name}) ".center(90, '#'))
                            print("#" * 90)

                            # --- 2. Core EPG Data Section ---
                            self._print_epg_core_data(tenant_name, ap_name, epg_attr, epg_children)

                            # --- 3. Contract Details Section ---
                            self._print_epg_contracts(epg_children)

                            # --- 4. Domain and Path Attachments Section (VMM, Static, VPC) ---
                            self._print_epg_attachments(epg_children)

        print("\n" + "=" * 100)
        print(" END OF EPG DETAIL REPORT ".center(100, '='))
        print("=" * 100)

    # Method that prints full details for all Bridge Domains (BDs) detected per Tenant.
    def printBdDetails(self, graph: nx.Graph) -> None:

        # Look for the dedicated Fabric Root Node
        tenant_root_node = next((data for node, data in graph.nodes(data=True) if node == "Fabric_Config_Root"), None)

        if not tenant_root_node or not tenant_root_node.get('tenants'):
            print("❌ No Tenant Configuration data found in the graph (Fabric_Config_Root node).")
            if tenant_root_node and tenant_root_node.get('error'):
                 print(f"Error encountered during fetch: {tenant_root_node['error']}")
            print("-" * 80)
            return

        print("-" * 100)
        print(" BRIDGE DOMAIN (BD) CONFIGURATION DETAILS ".center(100, '='))
        print("-" * 100)

        all_tenants = tenant_root_node.get('tenants', [])

        if not all_tenants:
            print("No Tenants configured in the fabric.")
            return

        for tenant_obj in all_tenants:
            tenant_attr = tenant_obj.get('fvTenant', {}).get('attributes', {})
            tenant_name = tenant_attr.get('name', 'N/A')

            # Skip only the 'N/A' tenants, include 'common' and 'mgmt' since BDs are often there
            if tenant_name == 'N/A':
                continue

            # ----------------------------------------------------------------------
            # Start BD Search within Tenant
            # ----------------------------------------------------------------------
            tenant_children = tenant_obj.get('fvTenant', {}).get('children', [])

            for child in tenant_children:
                if 'fvBD' in child:
                    bd_obj = child['fvBD']
                    bd_attr = bd_obj.get('attributes', {})
                    bd_name = bd_attr.get('name', 'N/A')
                    bd_children = bd_obj.get('children', [])

                    # --- 1. BD Header ---
                    print("\n" + "#" * 90)
                    print(f" BRIDGE DOMAIN: {bd_name} (Tenant: {tenant_name}) ".center(90, '#'))
                    print("#" * 90)

                    # --- 2. Core BD Data Section ---
                    self._print_bd_core_data(tenant_name, bd_attr, bd_children)

        print("\n" + "=" * 100)
        print(" END OF BRIDGE DOMAIN DETAIL REPORT ".center(100, '='))
        print("=" * 100)

    # Method that prints full details for all VRFs (fvCtx) detected per Tenant.
    def printVrfDetails(self, graph: nx.Graph) -> None:

        # Look for the dedicated Fabric Root Node
        tenant_root_node = next((data for node, data in graph.nodes(data=True) if node == "Fabric_Config_Root"), None)

        if not tenant_root_node or not tenant_root_node.get('tenants'):
            print("❌ No Tenant Configuration data found in the graph (Fabric_Config_Root node).")
            if tenant_root_node and tenant_root_node.get('error'):
                 print(f"Error encountered during fetch: {tenant_root_node['error']}")
            print("-" * 80)
            return

        print("-" * 100)
        print(" VRF (Context) CONFIGURATION DETAILS ".center(100, '='))
        print("-" * 100)

        all_tenants = tenant_root_node.get('tenants', [])

        if not all_tenants:
            print("No Tenants configured in the fabric.")
            return

        for tenant_obj in all_tenants:
            tenant_attr = tenant_obj.get('fvTenant', {}).get('attributes', {})
            tenant_name = tenant_attr.get('name', 'N/A')

            # Skip 'N/A' tenants
            if tenant_name == 'N/A':
                continue

            # ----------------------------------------------------------------------
            # Start VRF Search within Tenant
            # ----------------------------------------------------------------------
            tenant_children = tenant_obj.get('fvTenant', {}).get('children', [])

            for child in tenant_children:
                if 'fvCtx' in child:
                    vrf_obj = child['fvCtx']
                    vrf_attr = vrf_obj.get('attributes', {})
                    vrf_name = vrf_attr.get('name', 'N/A')
                    vrf_children = vrf_obj.get('children', [])

                    # --- 1. VRF Header ---
                    print("\n" + "#" * 90)
                    print(f" VRF: {vrf_name} (Tenant: {tenant_name}) ".center(90, '#'))
                    print("#" * 90)

                    # --- 2. Core VRF Data Section and Per-Node Deployment ---
                    self._print_vrf_core_data(tenant_name, vrf_attr, vrf_children)

        print("\n" + "=" * 100)
        print(" END OF VRF DETAIL REPORT ".center(100, '='))
        print("=" * 100)

    # Method that prints full details for all L3Outs (l3extOut) detected per Tenant.
    def printL3OutDetails(self, graph: nx.Graph) -> None:

        # Look for the dedicated Fabric Root Node
        tenant_root_node = next((data for node, data in graph.nodes(data=True) if node == "Fabric_Config_Root"), None)

        if not tenant_root_node or not tenant_root_node.get('tenants'):
            print("❌ No Tenant Configuration data found in the graph (Fabric_Config_Root node).")
            if tenant_root_node and tenant_root_node.get('error'):
                 print(f"Error encountered during fetch: {tenant_root_node['error']}")
            print("-" * 80)
            return

        print("-" * 100)
        print(" L3OUT (EXTERNAL NETWORK) CONFIGURATION DETAILS ".center(100, '='))
        print("-" * 100)

        all_tenants = tenant_root_node.get('tenants', [])

        if not all_tenants:
            print("No Tenants configured in the fabric.")
            return

        for tenant_obj in all_tenants:
            tenant_attr = tenant_obj.get('fvTenant', {}).get('attributes', {})
            tenant_name = tenant_attr.get('name', 'N/A')

            # Skip 'N/A' tenants
            if tenant_name == 'N/A':
                continue

            # ----------------------------------------------------------------------
            # Start L3Out Search within Tenant
            # ----------------------------------------------------------------------
            tenant_children = tenant_obj.get('fvTenant', {}).get('children', [])

            for child in tenant_children:
                if 'l3extOut' in child:
                    l3out_obj = child['l3extOut']
                    l3out_attr = l3out_obj.get('attributes', {})
                    l3out_name = l3out_attr.get('name', 'N/A')
                    l3out_children = l3out_obj.get('children', [])

                    # --- 1. L3Out Header ---
                    print("\n" + "#" * 90)
                    print(f" L3OUT: {l3out_name} (Tenant: {tenant_name}) ".center(90, '#'))
                    print("#" * 90)

                    # --- 2. Core L3Out Data Section and VRF/Route Policy ---
                    self._print_l3out_core_data(tenant_name, l3out_attr, l3out_children)

                    # --- 3. External EPGs (l3extInstP) ---
                    self._print_l3out_ext_epgs(l3out_children)

                    # --- 4. Node and Interface Details (l3extLNode/l3extLIf) ---
                    self._print_l3out_node_interfaces(l3out_children)

        print("\n" + "=" * 100)
        print(" END OF L3OUT DETAIL REPORT ".center(100, '='))
        print("=" * 100)

    # Method that prints full details for all Contracts (vzBrCP) detected per Tenant.
    def printContractDetails(self, graph: nx.Graph) -> None:

        # Look for the dedicated Fabric Root Node
        tenant_root_node = next((data for node, data in graph.nodes(data=True) if node == "Fabric_Config_Root"), None)

        if not tenant_root_node or not tenant_root_node.get('tenants'):
            print("❌ No Tenant Configuration data found in the graph (Fabric_Config_Root node).")
            if tenant_root_node and tenant_root_node.get('error'):
                 print(f"Error encountered during fetch: {tenant_root_node['error']}")
            print("-" * 80)
            return

        print("-" * 100)
        print(" CONTRACT (vzBrCP) CONFIGURATION DETAILS ".center(100, '='))
        print("-" * 100)

        all_tenants = tenant_root_node.get('tenants', [])

        if not all_tenants:
            print("No Tenants configured in the fabric.")
            return

        for tenant_obj in all_tenants:
            tenant_attr = tenant_obj.get('fvTenant', {}).get('attributes', {})
            tenant_name = tenant_attr.get('name', 'N/A')

            # Skip 'N/A' tenants
            if tenant_name == 'N/A':
                continue

            # ----------------------------------------------------------------------
            # Start Contract Search within Tenant
            # ----------------------------------------------------------------------
            tenant_children = tenant_obj.get('fvTenant', {}).get('children', [])

            for child in tenant_children:
                if 'vzBrCP' in child:
                    contract_obj = child['vzBrCP']
                    contract_attr = contract_obj.get('attributes', {})
                    contract_name = contract_attr.get('name', 'N/A')
                    contract_children = contract_obj.get('children', [])

                    # --- 1. Contract Header ---
                    print("\n" + "#" * 90)
                    print(f" CONTRACT: {contract_name} (Tenant: {tenant_name}) ".center(90, '#'))
                    print("#" * 90)

                    # --- 2. Core Contract Data Section (Scope, Target) ---
                    self._print_contract_core_data(tenant_name, contract_attr)

                    # --- 3. Contract Subjects and Filters ---
                    self._print_contract_subjects_and_filters(contract_children)

        print("\n" + "=" * 100)
        print(" END OF CONTRACT DETAIL REPORT ".center(100, '='))
        print("=" * 100)

    # Method that prints full details for all Filters (vzFilter) detected per Tenant.
    def printFilterDetails(self, graph: nx.Graph) -> None:

        # Look for the dedicated Fabric Root Node
        tenant_root_node = next((data for node, data in graph.nodes(data=True) if node == "Fabric_Config_Root"), None)

        if not tenant_root_node or not tenant_root_node.get('tenants'):
            print("❌ No Tenant Configuration data found in the graph (Fabric_Config_Root node).")
            if tenant_root_node and tenant_root_node.get('error'):
                 print(f"Error encountered during fetch: {tenant_root_node['error']}")
            print("-" * 80)
            return

        print("-" * 100)
        print(" FILTER (vzFilter) CONFIGURATION DETAILS ".center(100, '='))
        print("-" * 100)

        all_tenants = tenant_root_node.get('tenants', [])

        if not all_tenants:
            print("No Tenants configured in the fabric.")
            return

        for tenant_obj in all_tenants:
            tenant_attr = tenant_obj.get('fvTenant', {}).get('attributes', {})
            tenant_name = tenant_attr.get('name', 'N/A')

            # Skip 'N/A' tenants
            if tenant_name == 'N/A':
                continue

            # ----------------------------------------------------------------------
            # Start Filter Search within Tenant
            # ----------------------------------------------------------------------
            tenant_children = tenant_obj.get('fvTenant', {}).get('children', [])

            for child in tenant_children:
                if 'vzFilter' in child:
                    filter_obj = child['vzFilter']
                    filter_attr = filter_obj.get('attributes', {})
                    filter_name = filter_attr.get('name', 'N/A')
                    filter_children = filter_obj.get('children', [])

                    # --- 1. Filter Header ---
                    print("\n" + "#" * 90)
                    print(f" FILTER: {filter_name} (Tenant: {tenant_name}) ".center(90, '#'))
                    print("#" * 90)

                    # --- 2. Core Filter Data Section (Description) ---
                    self._print_filter_core_data(tenant_attr, filter_attr)

                    # --- 3. Filter Entries ---
                    self._print_filter_entries(filter_children)

        print("\n" + "=" * 100)
        print(" END OF FILTER DETAIL REPORT ".center(100, '='))
        print("=" * 100)

    # Method that prints detailed information for all Endpoints (fvCEp) and their IP addresses (fvIp)
    # detected across all EPGs per Tenant/AP.
    def printEndpointDetails(self, graph: nx.Graph) -> None:

        # Look for the dedicated Fabric Root Node
        tenant_root_node = next((data for node, data in graph.nodes(data=True) if node == "Fabric_Config_Root"), None)

        if not tenant_root_node or not tenant_root_node.get('tenants'):
            print("❌ No Tenant Configuration data found in the graph (Fabric_Config_Root node).")
            if tenant_root_node and tenant_root_node.get('error'):
                 print(f"Error encountered during fetch: {tenant_root_node['error']}")
            print("-" * 80)
            return

        print("-" * 100)
        print(" ENDPOINT (fvCEp/fvIp) CONFIGURATION DETAILS ".center(100, '='))
        print("-" * 100)

        all_tenants = tenant_root_node.get('tenants', [])

        if not all_tenants:
            print("No Tenants configured in the fabric.")
            return

        endpoints_found = 0

        for tenant_obj in all_tenants:
            tenant_attr = tenant_obj.get('fvTenant', {}).get('attributes', {})
            tenant_name = tenant_attr.get('name', 'N/A')

            # Skip 'N/A' tenants
            if tenant_name == 'N/A':
                continue

            # --- 1. Tenant Header ---
            print("\n" + "=" * 90)
            print(f" TENANT: {tenant_name} ".center(90, '='))
            print("=" * 90)

            tenant_children = tenant_obj.get('fvTenant', {}).get('children', [])

            for ap_child in tenant_children:
                if 'fvAp' in ap_child:
                    ap_name = ap_child['fvAp']['attributes'].get('name', 'N/A')
                    ap_epgs = ap_child['fvAp'].get('children', [])

                    for epg_child in ap_epgs:
                        if 'fvAEPg' in epg_child:
                            epg_name = epg_child['fvAEPg']['attributes'].get('name', 'N/A')
                            epg_children = epg_child['fvAEPg'].get('children', [])

                            epg_endpoints = []

                            # Find Endpoints (fvCEp) inside EPG
                            for ep_child in epg_children:
                                if 'fvCEp' in ep_child:
                                    ep_obj = ep_child['fvCEp']
                                    ep_attr = ep_obj['attributes']
                                    ep_children = ep_obj.get('children', [])

                                    # Collect IPs (fvIp) associated with this Endpoint
                                    ip_list = []
                                    for ip_child in ep_children:
                                        if 'fvIp' in ip_child:
                                            ip_list.append(ip_child['fvIp']['attributes'].get('addr', 'N/A'))

                                    # Extract location/path information
                                    path_info = "N/A"
                                    for path_child in ep_children:
                                        if 'fvRsCEpToPathEp' in path_child:
                                            path_dn = path_child['fvRsCEpToPathEp']['attributes'].get('tDn', '')
                                            # Example DN: topology/pod-1/paths-1234/pathep-[eth1/1]
                                            if path_dn:
                                                # Extract Node ID and Interface
                                                path_info = path_dn.split('/paths-')[-1].replace('/pathep-[', ' int-')
                                                path_info = path_info.replace(']', '')
                                                break

                                    epg_endpoints.append({
                                        'mac': ep_attr.get('mac', 'N/A'),
                                        'ip': ', '.join(ip_list) if ip_list else 'N/A',
                                        'status': ep_attr.get('status', 'N/A'),
                                        'pcTag': ep_attr.get('pcTag', 'N/A'),
                                        'encap': ep_attr.get('encap', 'N/A'),
                                        'is_local': ep_attr.get('isLocal', 'yes'),
                                        'path_info': path_info
                                    })
                                    endpoints_found += 1

                            # --- Print EPG Details if Endpoints were found ---
                            if epg_endpoints:
                                print(f"\n--- Application Profile: {ap_name} / EPG: {epg_name} ---")

                                # Prepare table header
                                header_keys = ['MAC Address', 'IP Address(es)', 'PC Tag', 'Encap', 'Path/VPC Location', 'Local?', 'Status']
                                header_line = "{:<18} {:<30} {:<8} {:<10} {:<30} {:<7} {:<10}".format(*header_keys)

                                print(header_line)
                                print("-" * 125)

                                for ep in epg_endpoints:
                                    print("{:<18} {:<30} {:<8} {:<10} {:<30} {:<7} {:<10}".format(
                                        ep['mac'],
                                        ep['ip'],
                                        ep['pcTag'],
                                        ep['encap'],
                                        ep['path_info'],
                                        ep['is_local'],
                                        ep['status']
                                    ))
                                print("-" * 125)

        print("\n" + "=" * 100)
        print(f" TOTAL ENDPOINTS FOUND: {endpoints_found} ".center(100, '='))
        print("=" * 100)

    #################################
    # Private General Print Methods #
    #################################

    # Private Method that will print all the Edge Attributes for the Cisco ACI Fabric
    def __privatePrintFabricEdgesAttributesCli(self, edge1: str, edge2: str, data: Dict[str, Any]) -> None:

        # Define Edge Column Headers
        header_edge_keys = [edge1, edge2]
        header_edge_line = "{:<45} {:<45}".format(*header_edge_keys)

        # Print a Edge combined header
        print("-" * (len(header_edge_line) + 1))
        print(f" {edge1} Interface {data['source_interface_id']} -- {edge2} Interface {data['dest_interface_id']} ".center(len(header_edge_line) + 1, '-'))
        print("-" * (len(header_edge_line) + 1))

        # Separate data for source and destination
        source_data = {key.replace('source_', ''): value for key, value in data.items() if key.startswith('source_')}
        dest_data = {key.replace('dest_', ''): value for key, value in data.items() if key.startswith('dest_')}

        # Define the sections and their keys
        interface_details_keys = [
            'interface_id', 'interface_adminSt', 'interface_operSt', 'interface_mode', 'interface_mtu',
            'interface_speed', 'interface_operSpeed', 'interface_operOperDuplex', 'interface_operLastLinkStChg'
        ]
        packet_stats_keys = [
            'pkts', 'octets', 'broadcastPkts', 'multicastPkts',
            'pkts64Octets', 'pkts65to127Octets', 'pkts128to255Octets',
            'pkts256to511Octets', 'pkts512to1023Octets', 'pkts1024to1518Octets'
        ]
        error_stats_keys = [
            'dropEvents', 'cRCAlignErrors', 'collisions', 'fragments', 'jabbers',
            'undersizePkts', 'oversizePkts', 'txOversizePkts', 'rxOversizePkts',
            'txGiantPkts', 'rxGiantPkts', 'tXNoErrors', 'rXNoErrors'
        ]

        # Define column headers
        header_keys = ['Attribute', 'Source', 'Destination']
        header_line = "{:<30} {:<30} {:<30}".format(*header_keys)

        # Print a combined header
        print("-" * len(header_line))
        print(" Interface Comparison ".center(len(header_line), '-'))
        print("-" * len(header_line))

        # Print tables for each section

        # Interface Details Table
        print(" Interface Details ".center(len(header_line), '-'))
        print(header_line)
        print("-" * len(header_line))
        for key in interface_details_keys:
            source_val = source_data.get(key, 'N/A')
            dest_val = dest_data.get(key, 'N/A')
            print("{:<30} {:<30} {:<30}".format(key.replace('interface_', '').replace('_', ' ').title(), source_val, dest_val))
        print("-" * len(header_line))

        # Packet Statistics Table
        print("\n" + " Packet Statistics ".center(len(header_line), '-'))
        print(header_line)
        print("-" * len(header_line))
        for key in packet_stats_keys:
            source_val = source_data.get(key, 'N/A')
            dest_val = dest_data.get(key, 'N/A')
            print("{:<30} {:<30} {:<30}".format(key.replace('_', ' ').title(), source_val, dest_val))
        print("-" * len(header_line))

        # Error Statistics Table
        print("\n" + " Error Statistics ".center(len(header_line), '-'))
        print(header_line)
        print("-" * len(header_line))
        for key in error_stats_keys:
            source_val = source_data.get(key, 'N/A')
            dest_val = dest_data.get(key, 'N/A')
            print("{:<30} {:<30} {:<30}".format(key.replace('_', ' ').title(), source_val, dest_val))
        print("-" * len(header_line))

    # Helper function to print core EPG attributes (BD, Isolation, Policy Tags)
    def _print_epg_core_data(self, tenant_name: str, ap_name: str, epg_attr: Dict[str, Any], epg_children: List[Dict[str, Any]]) -> None:

        # Helper to find linked object DNs (like BD or Domain)
        def find_linked_dn(children: List[Dict[str, Any]], target_class: str) -> str:
            for child in children:
                if target_class in child:
                    # Return the DN of the target class or its relation object
                    dn = child[target_class]['attributes'].get('tDn') if target_class.startswith('fvRs') else child[target_class]['attributes'].get('dn')
                    # Extract name from DN: 'uni/tn-T/BD-B' -> 'B'
                    if dn:
                        return dn.split('-')[-1].split('/')[0]
            return 'N/A'

        # Fetch BD (fvRsBd) and Vlan Domains (fvRsDomAtt)
        bd_name = find_linked_dn(epg_children, 'fvRsBd')
        vlan_domain = find_linked_dn(epg_children, 'fvRsDomAtt').replace('uni/phys-', '').replace('uni/vmmp-', '')

        print("\n--- Core EPG Configuration ---")
        print(f"{'Tenant':<25}: {tenant_name}")
        print(f"{'Application Profile':<25}: {ap_name}")
        print(f"{'EPG Name':<25}: {epg_attr.get('name', 'N/A')}")
        print(f"{'Bridge Domain (BD)':<25}: {bd_name}")
        print(f"{'Intra EPG Isolation':<25}: {epg_attr.get('pcEnfPref', 'unenforced')}")
        print(f"{'Policy Control Tag':<25}: {epg_attr.get('pcTag', 'N/A')}")
        print(f"{'QoS Class':<25}: {epg_attr.get('prio', 'unspecified')}")
        print(f"{'Vlan Domains Attached':<25}: {vlan_domain}")

    # Helper function to extract and print Contract information
    def _print_epg_contracts(self, epg_children: List[Dict[str, Any]]) -> None:

        provided = []
        consumed = []

        for child in epg_children:
            # Consumed Contracts (fvRsCons)
            if 'fvRsCons' in child:
                tDn = child['fvRsCons']['attributes'].get('tnVzBrCPName', 'N/A')
                # tDn is the contract name, e.g., 'CON-COMPUTE_VM_MANAGER-FILTER'
                if tDn != 'N/A':
                    consumed.append(tDn)

            # Provided Contracts (fvRsProv)
            elif 'fvRsProv' in child:
                tDn = child['fvRsProv']['attributes'].get('tnVzBrCPName', 'N/A')
                if tDn != 'N/A':
                    provided.append(tDn)

        print("\n--- Contract Details ---")

        # Format list into multiline output like the CLI example
        def format_contract_list(contracts: List[str], header: str):
            if not contracts:
                print(f"{header:<25}: None")
                return

            # Print first contract on the same line as the header
            print(f"{header:<25}: {contracts[0]}")
            # Print remaining contracts indented
            for contract in contracts[1:]:
                print(f"{'':<25}  {contract}")

        format_contract_list(consumed, "Consumed Contracts")
        format_contract_list(provided, "Provided Contracts")

    # Helper function to extract and print Path and Domain attachments
    def _print_epg_attachments(self, epg_children: List[Dict[str, Any]]) -> None:

        static_paths = []

        for child in epg_children:
            # Static Paths/VPC (fvRsPathAtt)
            if 'fvRsPathAtt' in child:
                path_attr = child['fvRsPathAtt']['attributes']
                tDn = path_attr.get('tDn', 'N/A')
                encap = path_attr.get('encap', 'N/A')
                mode = path_attr.get('mode', 'N/A')

                # tDn example: 'topology/pod-1/paths-1205-1206/extpaths-vpc-INTPOL-CC2_CNS1P113-A_INFR A_PROD_STORAGE/pathep-[eth1/1]'
                path_segments = tDn.split('/')

                # Extract Node IDs (e.g., 1205 1206) and Interface Name (e.g., vpc INTPOL-...)
                node_ids = ""
                interface_name = ""

                for segment in path_segments:
                    if segment.startswith('paths-'):
                        node_ids = segment.replace('paths-', '').replace('-', ' ')
                    elif segment.startswith('extpaths-'):
                        # Extract VPC/Path name
                        interface_name = segment.replace('extpaths-', '').replace('[', '').replace(']', '').replace('pathep-', '')

                static_paths.append({
                    'node': node_ids,
                    'interface': interface_name,
                    'encap': encap,
                    'mode': mode
                })

        print("\n--- Path and Domain Attachments ---")

        # VMM Domains (Simplified - only checking if domains are present)
        vmm_domain_found = any('fvRsDomAtt' in child and child['fvRsDomAtt']['attributes'].get('tDn', '').startswith('uni/vmmp') for child in epg_children)
        print(f"VMM Domains Found?: {'Yes' if vmm_domain_found else 'No'}")

        # Static Paths / VPC Links
        print("\nStatic Paths / VPC Links:")
        if not static_paths:
            print("  No Static Paths or VPC links found.")
        else:
            header_keys = ['Node ID(s)', 'Interface/VPC Name', 'Mode', 'Encap']
            header_line = "{:<12} {:<40} {:<10} {:<15}".format(*header_keys)
            print(header_line)
            print("-" * 79)

            for path in static_paths:
                print("{:<12} {:<40} {:<10} {:<15}".format(
                    path['node'],
                    path['interface'],
                    path['mode'],
                    path['encap']
                ))

    # Helper function to print core BD attributes (VRF, L2/L3 settings, ARP)
    def _print_bd_core_data(self, tenant_name: str, bd_attr: Dict[str, Any], bd_children: List[Dict[str, Any]]) -> None:

        # Helper to find linked object name (from a relation/tDn)
        def find_linked_name(children: List[Dict[str, Any]], target_class: str) -> str:
            for child in children:
                if target_class in child:
                    # Target DN is uni/tn-T/ctx-V
                    dn = child[target_class]['attributes'].get('tDn', 'N/A')
                    # Extract name: 'V'
                    if dn != 'N/A':
                        return dn.split('-')[-1]
            return 'N/A'

        # Helper to find specific child attributes
        def find_child_attr(children: List[Dict[str, Any]], target_class: str, attr_key: str) -> str:
            for child in children:
                if target_class in child:
                    return child[target_class]['attributes'].get(attr_key, 'N/A')
            return 'N/A'

        # --- Core BD Details ---
        vrf_name = find_linked_name(bd_children, 'fvRsCtx')
        mac_address = bd_attr.get('mac', '00:22:BD:F8:FF:FF') # Default MAC if missing

        # --- BD Attribute Extraction ---
        print("\n--- Bridge-Domain Detailed Information ---")
        print(f"{'Tenant':<30}: {tenant_name}")
        print(f"{'Bridge Domain':<30}: {bd_attr.get('name', 'N/A')}")
        print(f"{'MAC Address':<30}: {mac_address}")
        print(f"{'MTU':<30}: {bd_attr.get('gipo', 'inherit')}") # gipo attribute is often used for MTU inheritance
        print(f"{'VRF (Context)':<30}: {vrf_name}")
        print(f"{'Type':<30}: {bd_attr.get('type', 'regular')}")
        print(f"{'Description':<30}: {bd_attr.get('descr', '')}")
        print(f"{'Multi Destination (Flood)':<30}: {bd_attr.get('unkMcastAct', 'flood')}")
        print(f"{'L2 Unknown Unicast':<30}: {bd_attr.get('unkMacUcastAct', 'proxy')}")
        print(f"{'L3 Unknown Multicast':<30}: {bd_attr.get('unkIpMcastAct', 'flood')}")
        print(f"{'Unicast Routing':<30}: {'yes' if bd_attr.get('unicastRoute') == 'yes' else 'no'}")
        print(f"{'ARP Flooding':<30}: {'yes' if bd_attr.get('arpFlood') == 'yes' else 'no'}")
        print(f"{'PIM Enabled':<30}: {'yes' if bd_attr.get('multiDstPktAct') == 'bd-flood' else 'no'}") # Rough check for PIM-related setting
        print(f"{'Endpoint Move Detection':<30}: {bd_attr.get('hostBasedRouting', 'garp')}")

        # --- Endpoint Retention Policy (fvEpRetPol) ---
        ep_ret_pol_dn = find_linked_name(bd_children, 'fvRsEpRetPol')

        # Find the specific fvEpRetPol object's attributes from the tenant children list if it's referenced
        ret_pol_attr = {}
        for child in bd_children:
            if 'fvEpRetPol' in child:
                ret_pol_attr = child['fvEpRetPol']['attributes']
                break

        print("\n--- Endpoint Retention Policy Info ---")
        print(f"  {'Endpoint Retention Policy applied':<30}: {ep_ret_pol_dn}")

        # Default ACI timers or values from the attributes
        print(f"  {'Bounce Age Interval (sec.)':<30}: {ret_pol_attr.get('bounceAge', '630')}")
        print(f"  {'Hold Interval (sec.)':<30}: {ret_pol_attr.get('hold', '300')}")
        print(f"  {'Local Endpoint Age Interval (sec.)':<30}: {ret_pol_attr.get('localAge', '900')}")

        # 🛑 CHANGE THIS LINE 🛑
        print(f"  {'Move Frequency (sec.)':<30}: {ret_pol_attr.get('moveFreq', '256')}")
        # WAS: print(f"  {'Move Frequency (sec.)':<30}: {ret_pol_pol_attr.get('moveFreq', '256')}")

        print(f"  {'Remote Endpoint Age Interval (sec.)':<30}: {ret_pol_attr.get('remoteAge', '300')}")
        print("-" * 90)

    # Helper function to print core VRF attributes and per-node deployment status
    def _print_vrf_core_data(self, tenant_name: str, vrf_attr: Dict[str, Any], vrf_children: List[Dict[str, Any]]) -> None:

        # Helper to extract and format Contract information (shared with EPG method)
        def format_contract_list(children: List[Dict[str, Any]], header: str, target_class: str) -> str:
            contracts = []
            for child in children:
                if target_class in child:
                    tDn = child[target_class]['attributes'].get('tnVzBrCPName', 'N/A')
                    if tDn != 'N/A':
                        contracts.append(tDn)

            if not contracts:
                return '-'

            # Join contracts, trimming to a reasonable length for the first line
            # Additional contracts will be printed below the table
            return ",".join(contracts)

        # Contracts are related to the VRF via fvCtx.
        consumed_contracts_str = format_contract_list(vrf_children, "Consumed Contracts", 'vzRsCons')
        provided_contracts_str = format_contract_list(vrf_children, "Provided Contracts", 'vzRsProv')

        # --- VRF Global Details Table Header ---
        header_keys = ['Tenant', 'VRF', 'VXLAN Encap', 'Policy Enforced', 'Policy Tag', 'Consumed Contracts', 'Provided Contracts', 'Description']
        header_line = "{:<12} {:<15} {:<15} {:<17} {:<11} {:<22} {:<22} {:<30}".format(*header_keys)

        print("\nVRF Information:")
        print(header_line)
        print("-" * len(header_line))

        # --- VRF Global Details Data Row ---
        vrf_data = (
            tenant_name,
            vrf_attr.get('name', 'N/A'),
            vrf_attr.get('pcTag', 'N/A'), # ACI often stores VNID (VXLAN Encap) in 'pcTag' for the VRF
            vrf_attr.get('pcEnfPref', 'unenforced'),
            vrf_attr.get('pcTag', 'N/A'),
            consumed_contracts_str.split(',')[0], # Use only the first contract for the table row
            provided_contracts_str.split(',')[0], # Use only the first contract for the table row
            vrf_attr.get('descr', '')
        )
        # Note: I used 'pcTag' twice based on common ACI MO structures. If you have a true 'vxlanEncap' attribute, you should use that instead.

        print("{:<12} {:<15} {:<15} {:<17} {:<11} {:<22} {:<22} {:<30}".format(
            tenant_name,
            vrf_attr.get('name', 'N/A'),
            vrf_attr.get('pcTag', 'N/A'),
            vrf_attr.get('pcEnfPref', 'unenforced'),
            vrf_attr.get('pcTag', 'N/A'),
            consumed_contracts_str.split(',')[0],
            provided_contracts_str.split(',')[0],
            vrf_attr.get('descr', '')
        ))
        print("-" * len(header_line))

        # --- Print remaining contracts if any ---
        if len(consumed_contracts_str.split(',')) > 1 or len(provided_contracts_str.split(',')) > 1:
            print("Remaining Contracts:")
            # Print consumed contracts
            for contract in consumed_contracts_str.split(',')[1:]:
                 print(f"{'':<60} Consumed: {contract.strip()}")
            # Print provided contracts
            for contract in provided_contracts_str.split(',')[1:]:
                 print(f"{'':<60} Provided: {contract.strip()}")
            print("-" * len(header_line))

        # --- VRF Per-Node Deployment Information ---
        per_node_info = []
        for child in vrf_children:
            # vnetInstP holds per-node operational information (fvCtx is the config, vnetInstP is the operational object)
            if 'vnetInstP' in child:
                node_deployment = child['vnetInstP']['attributes']
                per_node_info.append(node_deployment)

        print("\nper-Node Information:")
        if not per_node_info:
            print("No per-Node deployment data found (likely not deployed or cluster info missing).")
            return

        # Per-Node Table Header
        node_header_keys = ['Node', 'Admin State', 'Oper State', 'Oper State Reason', 'Creation Time', 'Modification Time']
        node_header_line = "{:<10} {:<15} {:<15} {:<20} {:<30} {:<30}".format(*node_header_keys)

        print(node_header_line)
        print("-" * len(node_header_line))

        # Per-Node Data Rows
        for node_data in per_node_info:
            print("{:<10} {:<15} {:<15} {:<20} {:<30} {:<30}".format(
                node_data.get('nodeId', 'N/A'),
                node_data.get('adminState', 'N/A'),
                node_data.get('operState', 'N/A'),
                node_data.get('operStateQual', ''), # Usually empty if state is 'up'
                node_data.get('modTs', 'N/A'),
                node_data.get('modTs', 'N/A') # ACI usually uses 'modTs' for creation time in operational objects too
            ))
        print("-" * len(node_header_line))

    # Helper function to print core L3Out attributes (VRF, AS, Route Policies)
    def _print_l3out_core_data(self, tenant_name: str, l3out_attr: Dict[str, Any], l3out_children: List[Dict[str, Any]]) -> None:

        # Helper to find linked object name (from a relation/tDn)
        def find_linked_name(children: List[Dict[str, Any]], target_class: str) -> str:
            for child in children:
                if target_class in child:
                    # Target DN is uni/tn-T/ctx-V
                    dn = child[target_class]['attributes'].get('tDn', 'N/A')
                    # Extract name: 'V'
                    if dn != 'N/A':
                        return dn.split('-')[-1].split('/')[0]
            return 'N/A'

        # Fetch VRF (l3extRsVrf)
        vrf_name = find_linked_name(l3out_children, 'l3extRsVrf')

        # Determine ASN (often found in l3extOut attributes directly or l3extRsVrf)
        asn = l3out_attr.get('asn', 'N/A') # Common for tenant L3Outs

        print("\n--- Core L3Out Configuration ---")
        print(f"{'Tenant':<25}: {tenant_name}")
        print(f"{'L3Out Name':<25}: {l3out_attr.get('name', 'N/A')}")
        print(f"{'VRF (Context)':<25}: {vrf_name}")
        print(f"{'Description':<25}: {l3out_attr.get('descr', '')}")
        print(f"{'ASN (E.g., for BGP)':<25}: {asn}")

        # Route Policies (l3extRsRedistributePol / l3extRsEppAd / etc.)
        route_policies = []
        for child in l3out_children:
            # Check common route policy relations
            if 'l3extRsRedistributePol' in child:
                route_policies.append(f"Redistribute Policy: {child['l3extRsRedistributePol']['attributes'].get('tDn', 'N/A').split('/')[-1]}")
            if 'l3extRsEppAd' in child:
                route_policies.append(f"Egress Policy: {child['l3extRsEppAd']['attributes'].get('tDn', 'N/A').split('/')[-1]}")

        print(f"{'Route Policies':<25}: {route_policies[0] if route_policies else 'None'}")
        for policy in route_policies[1:]:
             print(f"{'':<25}  {policy}")
        print("-" * 50)

    # Helper function to extract and print External EPGs (l3extInstP)
    def _print_l3out_ext_epgs(self, l3out_children: List[Dict[str, Any]]) -> None:

        ext_epg_list = []

        for child in l3out_children:
            if 'l3extInstP' in child:
                ext_epg = child['l3extInstP']['attributes']
                ext_epg_children = child['l3extInstP'].get('children', [])

                # Extract contracts provided/consumed by this External EPG
                provided = []
                consumed = []
                subnet_count = 0

                for epg_child in ext_epg_children:
                    if 'vzRsProv' in epg_child:
                        provided.append(epg_child['vzRsProv']['attributes'].get('tnVzBrCPName', 'N/A'))
                    elif 'vzRsCons' in epg_child:
                        consumed.append(epg_child['vzRsCons']['attributes'].get('tnVzBrCPName', 'N/A'))
                    elif 'l3extSubnet' in epg_child:
                        subnet_count += 1

                ext_epg_list.append({
                    'name': ext_epg.get('name', 'N/A'),
                    'provided': provided,
                    'consumed': consumed,
                    'subnets': subnet_count
                })

        print("\n--- External EPGs (Network Instances) ---")
        if not ext_epg_list:
            print("No External EPGs (l3extInstP) found.")
            return

        for epg in ext_epg_list:
            print(f"  External EPG: {epg['name']}")
            print(f"    |-> Provided Contracts: {', '.join(epg['provided']) or 'None'}")
            print(f"    |-> Consumed Contracts: {', '.join(epg['consumed']) or 'None'}")
            print(f"    |-> Subnet Count: {epg['subnets']}")
        print("-" * 50)

    # Helper function to extract and print Logical Node and Interface details
    def _print_l3out_node_interfaces(self, l3out_children: List[Dict[str, Any]]) -> None:

        node_details = []

        for child in l3out_children:
            if 'l3extLNode' in child:
                node_obj = child['l3extLNode']
                node_attr = node_obj['attributes']
                node_children = node_obj.get('children', [])

                lifs = []
                for node_child in node_children:
                    if 'l3extLIf' in node_child:
                        lif_attr = node_child['l3extLIf']['attributes']
                        lif_children = node_child['l3extLIf'].get('children', [])

                        # Find interface reference (e.g., L3 port, SVI, SVI on VPC)
                        path_dn = 'N/A'
                        for lif_child in lif_children:
                            if 'l3extRsLIfPCons' in lif_child:
                                path_dn = lif_child['l3extRsLIfPCons']['attributes'].get('tDn', 'N/A')

                        lifs.append({
                            'id': lif_attr.get('name', 'N/A'),
                            'encap': lif_attr.get('encap', 'N/A'),
                            'ifType': lif_attr.get('routerId', 'N/A'), # 'routerId' is often used to hold the interface type logic
                            'path': path_dn
                        })

                node_details.append({
                    'name': node_attr.get('name', 'N/A'),
                    'id': node_attr.get('id', 'N/A'),
                    'router_id': node_attr.get('routerId', 'N/A'),
                    'loopback': node_attr.get('loopbackIfId', 'N/A'),
                    'interfaces': lifs
                })

        print("\n--- Logical Node and Interface Deployment ---")
        if not node_details:
            print("No Logical Nodes (l3extLNode) configured.")
            return

        for node_detail in node_details:
            print(f"  Logical Node: {node_detail['name']} (Node ID: {node_detail['id']})")
            print(f"    |-> Router ID: {node_detail['router_id']}")
            print(f"    |-> Loopback Interface: {node_detail['loopback']}")

            if node_detail['interfaces']:
                print(f"    |-> Interfaces ({len(node_detail['interfaces'])}):")

                header_keys = ['LIF Name', 'Encap', 'Path/VPC Reference']
                header_line = "{:<15} {:<10} {:<60}".format(*header_keys)
                print(f"{'':<8}{header_line}")
                print(f"{'':<8}{'-' * 85}")

                for lif in node_detail['interfaces']:
                    # Simple extraction of interface name from the DN
                    path_name = lif['path'].split('[')[-1].replace(']', '') if '[' in lif['path'] else lif['path']

                    print("{:<8}{:<15} {:<10} {:<60}".format(
                        '',
                        lif['id'],
                        lif['encap'],
                        path_name
                    ))
            else:
                 print("    |-> No Logical Interfaces found.")

        print("-" * 50)

        # Helper function to print core Contract attributes (Scope, Target, etc.)
    def _print_contract_core_data(self, tenant_name: str, contract_attr: Dict[str, Any]) -> None:

        print("\n--- Core Contract Configuration ---")
        print(f"{'Tenant':<25}: {tenant_name}")
        print(f"{'Contract Name':<25}: {contract_attr.get('name', 'N/A')}")
        print(f"{'Scope':<25}: {contract_attr.get('scope', 'context')}")
        print(f"{'Target DCI Type':<25}: {contract_attr.get('targetDscp', 'unspecified')}")
        print(f"{'Name Alias':<25}: {contract_attr.get('nameAlias', 'N/A')}")
        print("-" * 50)

    # Helper function to extract and print Contract Subjects and their Filters
    def _print_contract_subjects_and_filters(self, contract_children: List[Dict[str, Any]]) -> None:

        subject_list = []

        # 1. Iterate through children to find subjects (vzSubj)
        for child in contract_children:
            if 'vzSubj' in child:
                subject_obj = child['vzSubj']
                subject_attr = subject_obj['attributes']
                subject_children = subject_obj.get('children', [])

                subject_detail = {
                    'name': subject_attr.get('name', 'N/A'),
                    'reverse_filter': subject_attr.get('revFltPorts', 'no'),
                    'filters': []
                }

                # 2. Iterate through subject children to find filter relations (vzRsSubjFiltAtt)
                for subj_child in subject_children:
                    if 'vzRsSubjFiltAtt' in subj_child:
                        filter_attr = subj_child['vzRsSubjFiltAtt']['attributes']
                        # tDn format: uni/tn-T/flt-F (F is the filter name)
                        tDn = filter_attr.get('tDn', 'N/A')
                        filter_name = tDn.split('-')[-1] if tDn != 'N/A' else 'N/A'

                        subject_detail['filters'].append({
                            'name': filter_name,
                            'direction': filter_attr.get('directives', 'both'),
                            'tDn': tDn
                        })

                subject_list.append(subject_detail)

        print("\n--- Subjects and Filters ---")
        if not subject_list:
            print("No Subjects (vzSubj) defined in this Contract.")
            return

        for subject in subject_list:
            print(f"  Subject: {subject['name']}")
            print(f"    |-> Reverse Filter Ena: {subject['reverse_filter']}")

            if subject['filters']:
                print("    |-> Filters:")

                header_keys = ['Filter Name', 'Direction']
                header_line = "{:<20} {:<15}".format(*header_keys)
                print(f"{'':<10}{header_line}")
                print(f"{'':<10}{'-' * 35}")

                for filter_detail in subject['filters']:
                    print("{:<10}{:<20} {:<15}".format(
                        '',
                        filter_detail['name'],
                        filter_detail['direction']
                    ))
            else:
                 print("    |-> No Filters associated with this Subject.")

        print("-" * 50)

    # Helper function to print core Filter attributes (Description)
    def _print_filter_core_data(self, tenant_attr: Dict[str, Any], filter_attr: Dict[str, Any]) -> None:

        print("\n--- Core Filter Configuration ---")
        print(f"{'Description':<25}: {filter_attr.get('descr', 'N/A')}")
        print("-" * 50)


    # Helper function to extract and print Filter Entries (vzEntry)
    def _print_filter_entries(self, filter_children: List[Dict[str, Any]]) -> None:

        entry_list = []

        # 1. Iterate through children to find entries (vzEntry)
        for child in filter_children:
            if 'vzEntry' in child:
                entry_attr = child['vzEntry']['attributes']

                entry_list.append({
                    'name': entry_attr.get('name', 'N/A'),
                    'ethertype': entry_attr.get('etherT', 'ip'),
                    'protocol': entry_attr.get('prot', 'unspecified'),
                    'd_from': entry_attr.get('dFromPort', 'unspecified'),
                    'd_to': entry_attr.get('dToPort', 'unspecified'),
                    's_from': entry_attr.get('sFromPort', 'unspecified'),
                    's_to': entry_attr.get('sToPort', 'unspecified'),
                    'tcp_flags': entry_attr.get('tcpRules', 'not-applicable')
                })

        print("\n--- Filter Entries (vzEntry) ---")
        if not entry_list:
            print("No Entries (vzEntry) defined in this Filter.")
            return

        # Prepare table header
        header_keys = ['Entry Name', 'EtherType', 'Protocol', 'Dst Port From', 'Dst Port To', 'Src Port From', 'Src Port To', 'TCP Flags']
        header_line = "{:<15} {:<10} {:<10} {:<15} {:<15} {:<15} {:<15} {:<15}".format(*header_keys)

        print(header_line)
        print("-" * 110)

        for entry in entry_list:
            print("{:<15} {:<10} {:<10} {:<15} {:<15} {:<15} {:<15} {:<15}".format(
                entry['name'],
                entry['ethertype'],
                entry['protocol'],
                entry['d_from'],
                entry['d_to'],
                entry['s_from'],
                entry['s_to'],
                entry['tcp_flags']
            ))

        print("-" * 110)
