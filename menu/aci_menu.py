# coding=utf-8

######################################################################################################
#  Class that will print all the information collected in the network_graph.py from Cisco ACI Fabric #
######################################################################################################

##################
# Import Section #
##################

from printers.aci_printers import ACITroubleshooterPrinter
from aci_api_client.UserClass import UserClass
from typing import Any, Type
import os
import json
import yaml

###########################
# Private Singleton Class #
###########################

class _PrivateCookie(type):

    _instances: dict[Type[Any], Any] = {}

    def __call__(cls, *args, **kwargs):

        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]

#########################################################
# MenuPrinter Class that will print the Menu to print   #
# the info from the NetworkX Graph                      #
#########################################################

class MenuPrinter(metaclass=_PrivateCookie):

    def __init__(self):
        self.__printer = ACITroubleshooterPrinter()

    ##################
    # Public Methods #
    ##################

    # Method that print main menu and capture
    # User option selection
    def mainMenu(self, graph):

        # Auxilear Variable to the while loop
        whileScriptIsExecuted = True

        # While user don't press option '0'
        # The Script Execution Continue
        while whileScriptIsExecuted:

            # Cleaning CLI
            self.__clear_screen()

            # Displaying Main Menu
            self.__display_menu()

            # Waiting for user option selection
            choice = input("Enter your choice: ")
            print()

            if choice == '0':
                whileScriptIsExecuted = False

            # Printing Controller Menu
            elif choice == '1':
                self.__displayApicMenu(graph)

            # Printing Switch Menu
            elif choice == '2':
                self.__displaySwitchMenu(graph)

            # Printing Switch Recommended Actions
            elif choice == '3':
                self.__displaySwitcImprovementhMenu(graph)

            # Printing General Graph Methods
            elif choice == '4':
                self.__displayGeneralGraphMethod(graph)

            # Printing Export Data Section
            elif choice == '5':
                self.__displayExportData(graph)

            # Printing Tenant Section
            elif choice == '6':
                self.__displayTenantMeny(graph)

            # Wrong Option Selected
            else:
                print("Invalid choice. Please try again.")

    ################################
    # Private Methods in the Class #
    ################################

    # Clearing CLI Content for clarity
    def __clear_screen(self):
        _ = os.system('clear')

    # Private Method that print the main menu with the script banner
    def __display_menu(self):

        # Header for the Fabric Attributes table
        menu_header_keys = [' Menu Option ', ' Option Description ']
        menu_header_line = "|{:<14} {:<39}|".format(*menu_header_keys)

        # Auxilear variable to print Script Banner
        banner = '''
+-------------------------------------------------------------------------------------------------------------------+
|   ____ _                    _    ____ ___   _   _      _                      _       ____                 _      |
|  / ___(_)___  ___ ___      / \  / ___|_ _| | \ | | ___| |___      _____  _ __| | __  / ___|_ __ __ _ _ __ | |__   |
| | |   | / __|/ __/ _ \    / _ \| |    | |  |  \| |/ _ \ __\ \ /\ / / _ \| '__| |/ / | |  _| '__/ _` | '_ \| '_ \  |
| | |___| \__ \ (_| (_) |  / ___ \ |___ | |  | |\  |  __/ |_ \ V  V / (_) | |  |   <  | |_| | | | (_| | |_) | | | | |
|  \____|_|___/\___\___/  /_/   \_\____|___| |_| \_|\___|\__| \_/\_/ \___/|_|  |_|\_\  \____|_|  \__,_| .__/|_| |_| |
|                                                                                                     |_|           |
+-------------------------------------------------------------------------------------------------------------------+'''
        # Printing Banner into the CLI
        print(banner)

        # Declaring & Printing Menu Banner
        header_text = " Cisco ACI Diagnostic CLI Tool "
        total_width = len(menu_header_line)
        centered_header = header_text.center(total_width, '-')
        print("")
        print("-" * len(menu_header_line))
        print(centered_header)
        print("-" * len(menu_header_line))
        print(menu_header_line)

        # Printing Meny
        print("+" + "-" * (len(menu_header_line) - 2) + "+")
        print("|     0.         Exit                                  |")
        print("|     1.         Controllers                           |")
        print("|     2.         Switches                              |")
        print("|     3.         Switch Recommended Actions            |")
        print("|     4.         General Graph Methods                 |")
        print("|     5.         Export Data                           |")
        print("|     6.         Tenant Section                        |")
        print("+" + "-" * (len(menu_header_line) - 2) + "+")
        print("-" * len(menu_header_line))

    # Menu that will print 
    def __displayApicMenu(self, graph):

        # Clearing CLI Terminal
        self.__clear_screen()

        # Header for the Controller  table
        menu_header_keys = [' Controller Menu ', ' Option Description ']
        menu_header_line = "|{:<19} {:<39}|".format(*menu_header_keys)

        # Banner declaration
        banner = '''
+-----------------------------------------------------------------------------------+
|   ____            _             _ _             ____            _   _             |
|  / ___|___  _ __ | |_ _ __ ___ | | | ___ _ __  / ___|  ___  ___| |_(_) ___  _ __  |
| | |   / _ \| '_ \| __| '__/ _ \| | |/ _ \ '__| \___ \ / _ \/ __| __| |/ _ \| '_ \ |
| | |__| (_) | | | | |_| | | (_) | | |  __/ |     ___) |  __/ (__| |_| | (_) | | | ||
|  \____\___/|_| |_|\__|_|  \___/|_|_|\___|_|    |____/ \___|\___|\__|_|\___/|_| |_||
+-----------------------------------------------------------------------------------+
'''
        #Printing Banner into the CLI
        print(banner)

        # Auxilear Variable to the while loop
        whileControllerSectionIsExecuted = True

        # While user don't press option '0'
        # The Script Execution Continue
        while whileControllerSectionIsExecuted:

            # Declaring & Printing Menu Banner
            header_text = " Cisco ACI Controller Menu "
            total_width = len(menu_header_line)
            centered_header = header_text.center(total_width, '-')

            # Printing Menu
            print("")
            print("-" * len(menu_header_line))
            print(centered_header)
            print("-" * len(menu_header_line))
            print(menu_header_line)
            print("+" + "-" * (len(menu_header_line) - 2) + "+")

            #Printing available optiones in the APIC Section
            print("|       0.            Exit                                  |")
            print("|       1.            Print APIC Database Sync Status       |")
            print("|       2.            Print APIC Filesystem Info            |")
            print("|       3.            Print APIC PSU Info                   |")
            print("|       4.            Print APIC FAN Info                   |")
            print("|       5.            Print APIC Sensor Info                |")
            print("|       6.            Print APIC DIMM Info                  |")
            print("|       7.            Print APIC NTP Info                   |")
            print("|       8.            Print APIC Physical Interface Info    |")
            print("|       9.            Print APIC Aggregate Interface Info   |")
            print("+" + "-" * (len(menu_header_line) - 2) + "+")

            # Waiting for user option selection
            choice = input("Enter your choice: ")
            print()

            # Exit the Controller Section
            if choice == '0':
                whileControllerSectionIsExecuted = False

            # Printing APICs BBDD Sync Status
            elif choice == '1':
                self.__printer.printApicNodesBbddSyncStatusInfo(graph)
                input()
                self.__clear_screen()

            # Printing Controller Filesystem Info
            elif choice == '2':
                self.__printer.printApicNodesFileSystemInfo(graph)
                input()
                self.__clear_screen()

            # Printing Controller PSU Info
            elif choice == '3':
                self.__printer.printApicNodesPsuInfo(graph)
                input()
                self.__clear_screen()

            # Printing Controller FAN Info
            elif choice == '4':
                self.__printer.printApicNodesFanInfo(graph)
                input()
                self.__clear_screen()

            # Printing Controller Sensors Info
            elif choice == '5':
                self.__printer.printApicNodesSensorInfo(graph)
                input()
                self.__clear_screen()

            # Printing Controller DIMMs Info
            elif choice == '6':
                self.__printer.printApicNodesDimmsInfo(graph)
                input()
                self.__clear_screen()

            # Printing Controller NTP Info
            elif choice == '7':
                self.__printer.printApicNodesNtpInfo(graph)
                input()
                self.__clear_screen()

            # Printing Controller Physical Interface Info
            elif choice == '8':
                self.__printer.printApicNodesPhyIntInfo(graph)
                input()
                self.__clear_screen()

            # Printing Controller Aggregate Interface Info
            elif choice == '9':
                self.__printer.printApicNodesAggIntInfo(graph)
                input()
                self.__clear_screen()

            # Wrong option selected
            else:
                print("Invalid choice. Please try again.")

    # Menu that will print 
    def __displaySwitchMenu(self, graph):

        # Clearing CLI Terminal
        self.__clear_screen()

        # Header for the Switch table
        menu_header_keys = [' Switch Menu ', ' Option Description ']
        menu_header_line = "|{:<19} {:<39}|".format(*menu_header_keys)

        # Banner declaration
        banner = '''
+---------------------------------------------------------------------+
|  ____          _ _       _       ____            _   _              |
| / ___|_      _(_) |_ ___| |__   / ___|  ___  ___| |_(_) ___  _ __   |
| \___ \ \ /\ / / | __/ __| '_ \  \___ \ / _ \/ __| __| |/ _ \| '_ \  |
|  ___) \ V  V /| | || (__| | | |  ___) |  __/ (__| |_| | (_) | | | | |
| |____/ \_/\_/ |_|\__\___|_| |_| |____/ \___|\___|\__|_|\___/|_| |_| |
|                                                                     |
+---------------------------------------------------------------------+
'''
        #Printing Banner into the CLI
        print(banner)

        # Auxilear Variable for the while loop
        whileSwitchSectionIsExecuted = True

        # While the variable 'whileSwitchSectionIsExecuted' is True
        # We print the menu content
        while whileSwitchSectionIsExecuted:

            # Declaring & Printing Menu Banner
            header_text = " Cisco ACI Switch Menu "
            total_width = len(menu_header_line)
            centered_header = header_text.center(total_width, '-')

            # Printing Menu
            print("")
            print("-" * len(menu_header_line))
            print(centered_header)
            print("-" * len(menu_header_line))
            print(menu_header_line)
            print("+" + "-" * (len(menu_header_line) - 2) + "+")
            print("|       0.            Exit                                  |")
            print("|       1.            Print Switch Node Interfaces          |")
            print("|       2.            Print Switch Node Supervisors         |")
            print("|       3.            Print Switch Node Faults              |")
            print("|       4.            Print Spine Switch System Controllers |")
            print("|       5.            Print Spine Switch Fabric Modules     |")
            print("|       6.            Print Switch Node PSUs                |")
            print("|       7.            Print Switch Node Linecards           |")
            print("|       8.            Print Switch Node SFP Info            |")
            print("|       9.            Print Fabric Switches Filesystem      |")
            print("+" + "-" * (len(menu_header_line) - 2) + "+")

            # Waiting for user option selection
            choice = input("Enter your choice: ")
            print()

            # Exit the Controller Section
            if choice == '0':
                whileSwitchSectionIsExecuted = False

            # Printing Cisco ACI Switch Interfaces
            elif choice == '1':
                self.__printer.getSwitchNodeInterfacesInfo(graph)
                input()
                self.__clear_screen()

            # Printing Cisco ACI Switch Supervisors
            elif choice == '2':
                self.__printer.getSwitchNodeSupervisorInfo(graph)
                input()
                self.__clear_screen()

            # Printing Cisco ACI Switch Faults
            elif choice == '3':
                self.__printer.getSwitchNodeFaultsInfo(graph)
                input()
                self.__clear_screen()

            # Printing Cisco ACI Switch Controllers
            elif choice == '4':
                self.__printer.getSpineSwitchNodeSystemControllerInfo(graph)
                input()
                self.__clear_screen()

            # Printing Cisco ACI Switch Fabric Modules
            elif choice == '5':
                self.__printer.getSpineSwitchNodeFabricModulesInfo(graph)
                input()
                self.__clear_screen()

            # Printing Cisco ACI Switch PSUs
            elif choice == '6':
                self.__printer.getSwitchNodePsuInfo(graph)
                input()
                self.__clear_screen()

            # Printing Cisco ACI Linecards
            elif choice == '7':
                self.__printer.getSwitchNodeLinecardInfo(graph)
                input()
                self.__clear_screen()

            # Printing Cisco ACI SFP
            elif choice == '8':
                self.__printer.printSwitchNodesSfpInterfaceInfo(graph)
                input()
                self.__clear_screen()

            # Printing Cisco ACI Filesystem
            elif choice == '9':
                self.__printer.printFabricSwitchesFilesystemNodes(graph)
                input()

            # Wrong Option Selected
            else:
                print("Invalid choice. Please try again.")

   # Menu that will print the improvement Posible in the Graph
    def __displaySwitcImprovementhMenu(self, graph):

        # Clearing CLI Terminal
        self.__clear_screen()

        # Header for the Switch table
        menu_header_keys = [' Improvement Menu ', ' Option Description ']
        menu_header_line = "|{:<19} {:<46}|".format(*menu_header_keys)

        # Banner declaration
        banner = '''
+-------------------------------------------------------------------------------------------------------+
|  ____          _ _       _       ___                                                         _        |
| / ___|_      _(_) |_ ___| |__   |_ _|_ __ ___  _ __  _ __ _____   _____ _ __ ___   ___ _ __ | |_ ___  |
| \___ \ \ /\ / / | __/ __| '_ \   | || '_ ` _ \| '_ \| '__/ _ \ \ / / _ \ '_ ` _ \ / _ \ '_ \| __/ __| |
|  ___) \ V  V /| | || (__| | | |  | || | | | | | |_) | | | (_) \ V /  __/ | | | | |  __/ | | | |_\__ \ |
| |____/ \_/\_/ |_|\__\___|_| |_| |___|_| |_| |_| .__/|_|  \___/ \_/ \___|_| |_| |_|\___|_| |_|\__|___/ |
|                                               |_|                                                     |
+-------------------------------------------------------------------------------------------------------+

'''
        #Printing Banner into the CLI
        print(banner)

        # Auxilear Variable for the while loop
        whileSwitchImprovementIsExecuted = True

        # While the variable 'whileSwitchImprovementIsExecuted' is True
        # we print the Improvement Menu
        while whileSwitchImprovementIsExecuted:

            # Declaring & Printing Menu Banner
            header_text = " Cisco ACI Switch Improvement Menu "
            total_width = len(menu_header_line)
            centered_header = header_text.center(total_width, '-')

            # Printing Menu
            print("")
            print("-" * len(menu_header_line))
            print(centered_header)
            print("-" * len(menu_header_line))
            print(menu_header_line)
            print("+" + "-" * (len(menu_header_line) - 2) + "+")
            print("|        0.           Exit                                         |")
            print("|        1.           Downlink Interfaces that Should be Down      |")
            print("|        2.           Fabric Interfaces with Errors Summary        |")
            print("|        3.           Fabric Interfaces with Errors Detailed       |")
            print("|        4.           SFP Diagnostic Report (Temp, Power, Volt)    |")
            print("+" + "-" * (len(menu_header_line) - 2) + "+")

            # Waiting for user option selection
            choice = input("Enter your choice: ")
            print()

            # Exit the Controller Section
            if choice == '0':
                whileSwitchImprovementIsExecuted = False

            # Printing Cisco ACI Switch Interfaces
            elif choice == '1':
                self.__printer.getSwitchNodeInterfacesShouldBeDownInfo(graph)
                input()
                self.__clear_screen()

            # Printing Cisco ACI Interfaces with error (Summary)
            elif choice == '2':
                self.__printer.printFabricEdgesWithErrorsCli(graph)
                input()
                self.__clear_screen()

            # Printing Cisco ACI Interfaces with Errors (Details)
            elif choice == '3':
                self.__printer.printFabricEdgesWithErrorDetailsCli(graph)
                input()
                self.__clear_screen()

            # Printing SFP Diagnostic Report (New)
            elif choice == '4':
                self.__printer.printSwitchSfpDiagnostics(graph)
                input()
                self.__clear_screen()

            # Wrong Option Selected
            else:
                print("Invalid choice. Please try again.")

    # Displaying General Graph Methods Menu
    def __displayGeneralGraphMethod(self, graph):

       # Clearing CLI Terminal
        self.__clear_screen()

        # Header for the Switch table
        menu_header_keys = [' Menu ', ' Option Description ']
        menu_header_line = "|{:<19} {:<39}|".format(*menu_header_keys)

        # Banner Declaration
        banner = '''
+-----------------------------------------------------------------------------------------------------------+
|   ____                           _    ____                 _       __  __      _   _               _      |
|  / ___| ___ _ __   ___ _ __ __ _| |  / ___|_ __ __ _ _ __ | |__   |  \/  | ___| |_| |__   ___   __| |___  |
| | |  _ / _ \ '_ \ / _ \ '__/ _` | | | |  _| '__/ _` | '_ \| '_ \  | |\/| |/ _ \ __| '_ \ / _ \ / _` / __| |
| | |_| |  __/ | | |  __/ | | (_| | | | |_| | | | (_| | |_) | | | | | |  | |  __/ |_| | | | (_) | (_| \__ \ |
|  \____|\___|_| |_|\___|_|  \__,_|_|  \____|_|  \__,_| .__/|_| |_| |_|  |_|\___|\__|_| |_|\___/ \__,_|___/ |
|                                                     |_|                                                   |
+-----------------------------------------------------------------------------------------------------------+
'''

        #Printing Banner into the CLI
        print(banner)

        # Auxilear Variable for the while loop
        whileGeneralGraphMethodIsExecuted = True

        # While the variable 'whileSwitchImprovementIsExecuted' is True
        # we print the Improvement Menu
        while whileGeneralGraphMethodIsExecuted:

            # Declaring & Printing Menu Banner
            header_text = " General Graph Methods Menu "
            total_width = len(menu_header_line)
            centered_header = header_text.center(total_width, '-')

            # Printing Menu
            print("")
            print("-" * len(menu_header_line))
            print(centered_header)
            print("-" * len(menu_header_line))
            print(menu_header_line)
            print("+" + "-" * (len(menu_header_line) - 2) + "+")
            print("|       0.            Exit                                  |")
            print("|       1.            Print Graph Nodes                     |")
            print("|       2.            Print Graph Edges                     |")
            print("|       3.            Print Graph EPG Nodes                 |")
            print("+" + "-" * (len(menu_header_line) - 2) + "+")

            # Waiting for user option selection
            choice = input("Enter your choice: ")
            print()

            # Exit the Controller Section
            if choice == '0':
                whileGeneralGraphMethodIsExecuted = False

            # Printing All Graph Nodes Elements
            elif choice == '1':
                self.__printer.printingNodeAttributes(graph)
                input()
                self.__clear_screen()

            # Printing All Graph Edges Elements
            elif choice == '2':
                self.__printer.printAllFabricEdgesAttributesCli(graph)
                input()
                self.__clear_screen()

            # Printing All Graph Edges Elements
            elif choice == '3':
                self.__printer.printAllNetworkDevicesNodesCli(graph)
                input()
                self.__clear_screen()

            # Wrong Option Selected
            else:
                print("Invalid choice. Please try again.")

     # Displaying General Graph Methods Menu
    def __displayTenantMeny(self, graph):

       # Clearing CLI Terminal
        self.__clear_screen()

        # Header for the Switch table
        menu_header_keys = [' Menu ', ' Option Description ']
        menu_header_line = "|{:<19} {:<39}|".format(*menu_header_keys)

        # Banner Declaration
        banner = '''
+-----------------------------------------------------------------+
|  _____                      _      ____             __ _        |
| |_   _|__ _ __   __ _ _ __ | |_   / ___|___  _ __  / _(_) __ _  |
|   | |/ _ \ '_ \ / _` | '_ \| __| | |   / _ \| '_ \| |_| |/ _` | |
|   | |  __/ | | | (_| | | | | |_  | |__| (_) | | | |  _| | (_| | |
|   |_|\___|_| |_|\__,_|_| |_|\__|  \____\___/|_| |_|_| |_|\__, | |
|                                                            |__/ |
|                                                                 |
+-----------------------------------------------------------------+
'''

        #Printing Banner into the CLI
        print(banner)

        # Auxilear Variable for the while loop
        whileTenantMethodIsExecuted = True

        # While the variable 'whileSwitchImprovementIsExecuted' is True
        # we print the Improvement Menu
        while whileTenantMethodIsExecuted:

            # Declaring & Printing Menu Banner
            header_text = " General Graph Methods Menu "
            total_width = len(menu_header_line)
            centered_header = header_text.center(total_width, '-')

            # Printing Menu
            print("")
            print("-" * len(menu_header_line))
            print(centered_header)
            print("-" * len(menu_header_line))
            print(menu_header_line)
            print("+" + "-" * (len(menu_header_line) - 2) + "+")
            print("|       0.            Exit                                  |")
            print("|       1.            Tenant Config Brief.                  |")
            print("|       2.            EPG List by Tenant/AP Brief           |")
            print("|       3.            Print EPG Full Details                |")
            print("|       4.            Print Bridge Domain Full Details      |")
            print("|       5.            Print VRF Full Details                |")
            print("|       6.            Print L3Out Full Details              |")
            print("|       7.            Print Contract Full Details           |")
            print("|       8.            Print Filter Full Details             |")
            print("|       9.            Print Endpoint (MAC/IP) Details       |")
            print("+" + "-" * (len(menu_header_line) - 2) + "+")

            # Waiting for user option selection
            choice = input("Enter your choice: ")
            print()

            # Exit the Controller Section
            if choice == '0':
                whileTenantMethodIsExecuted = False

            # Printing Tenant Info
            elif choice == '1':
                self.__printer.printFabricTenantInfo(graph)
                input()
                self.__clear_screen()

            # Printing EPG List
            elif choice == '2':
                self.__printer.printTenantEpgList(graph)
                input()
                self.__clear_screen()

            # Printing EPG Full Details
            elif choice == '3':
                self.__printer.printEpgDetails(graph)
                input()
                self.__clear_screen()

            # Printing Bridge Domain Full Details
            elif choice == '4':
                self.__printer.printBdDetails(graph)
                input()
                self.__clear_screen()

            # Printing VRF Full Details
            elif choice == '5':
                self.__printer.printVrfDetails(graph)
                input()
                self.__clear_screen()

            # Printing L3Out Full Details
            elif choice == '6':
                self.__printer.printL3OutDetails(graph)
                input()
                self.__clear_screen()

            # Printing Contract Full Details
            elif choice == '7':
                self.__printer.printContractDetails(graph)
                input()
                self.__clear_screen()

            # Printing Filter Full Details
            elif choice == '8':
                self.__printer.printFilterDetails(graph)
                input()
                self.__clear_screen()

            # Printing Endpoint Details
            elif choice == '9':
                self.__printer.printEndpointDetails(graph)
                input()
                self.__clear_screen()

            # Wrong Option Selected
            else:
                print("Invalid choice. Please try again.")

    # Export Data Private Method
    def __displayExportData(self, graph):

       # Clearing CLI Terminal
        self.__clear_screen()

        # Header for the Switch table
        menu_header_keys = [' Menu ', ' Option Description ']
        menu_header_line = "|{:<19} {:<39}|".format(*menu_header_keys)

        # Banner Declaration
        banner = '''
+----------------------------------------------------------------------------------------------------------------------------------------------+
|  _____                       _     _   _           _                      _    __  __   ____                 _       ____    _  _____  _     |
| | ____|_  ___ __   ___  _ __| |_  | \ | | _____  _| |___      _____  _ __| | __\ \/ /  / ___|_ __ __ _ _ __ | |__   |  _ \  / \|_   _|/ \    |
| |  _| \ \/ / '_ \ / _ \| '__| __| |  \| |/ _ \ \/ / __\ \ /\ / / _ \| '__| |/ / \  /  | |  _| '__/ _` | '_ \| '_ \  | | | |/ _ \ | | / _ \   |
| | |___ >  <| |_) | (_) | |  | |_  | |\  |  __/>  <| |_ \ V  V / (_) | |  |   <  /  \  | |_| | | | (_| | |_) | | | | | |_| / ___ \| |/ ___ \  |
| |_____/_/\_\ .__/ \___/|_|   \__| |_| \_|\___/_/\_\\__|  \_/\_/ \___/|_|  |_|\_\/_/\_\  \____|_|  \__,_| .__/|_| |_| |____/_/   \_\_/_/   \_\ |
|            |_|                                                                                        |_|                                    |
+----------------------------------------------------------------------------------------------------------------------------------------------+
'''

        #Printing Banner into the CLI
        print(banner)

        # Auxilear Variable for the while loop
        whileExportGraphMethodIsExecuted = True

        # While the variable 'whileSwitchImprovementIsExecuted' is True
        # we print the Improvement Menu
        while whileExportGraphMethodIsExecuted:

            # Declaring & Printing Menu Banner
            header_text = " Export NetworkX Graph Node Data "
            total_width = len(menu_header_line)
            centered_header = header_text.center(total_width, '-')

            # Printing Menu
            print("")
            print("-" * len(menu_header_line))
            print(centered_header)
            print("-" * len(menu_header_line))
            print(menu_header_line)
            print("+" + "-" * (len(menu_header_line) - 2) + "+")
            print("|       0.            Exit                                  |")
            print("|       1.            Export Graph Node JSON Format         |")
            print("|       2.            Export Graph Node Yaml Format         |")
            print("+" + "-" * (len(menu_header_line) - 2) + "+")

                        # Waiting for user option selection
            choice = input("Enter your choice: ")
            print()

            # Exit the Controller Section
            if choice == '0':
                whileExportGraphMethodIsExecuted = False

            # Printing All Graph Nodes Elements
            elif choice == '1':
                self.__save_graph_to_jsonfile(graph)
                input()
                self.__clear_screen()

            # Printing All Graph Edges Elements
            elif choice == '2':
                self.__save_graph_to_jsonYaml(graph)
                input()
                self.__clear_screen()

            # Wrong Option Selected
            else:
                print("Invalid choice. Please try again.")

    # Export method to save the Graph Data to a JSON file
    def __save_graph_to_jsonfile(self, graph):

        # List to hold the nodes data
        nodes_data = []

        # Iterate through all the nodes in the graph
        for node, attributes in graph.nodes(data=True):

            # Create a dictionary for the current node
            if attributes:
                node_data = {
                    "node": node,
                    "attributes": attributes
                }

            # Inserting the Fabric Node in the Graph inside the list
            nodes_data.append(node_data)

        # Saving the Graph Nodes List 'nodes_data' into the file
        try:
            with open(UserClass().Path + "GraphNodesData.json", 'w') as f:
                json.dump(nodes_data, f, indent=4)
                print(f" ✨ ✨ ✨ Graph data successfully saved in JSON format. ✨ ✨ ✨")

        except Exception as e:
            print(f"An error occurred while saving the file: {e} ❌")

    # Export method to save the Graph Data to a YAML file
    def __save_graph_to_jsonYaml(self, graph):

        # List to hold the nodes data
        nodes_data = []

        # Iterate through all the nodes in the graph
        for node, attributes in graph.nodes(data=True):

            # Create a dictionary for the current node
            if attributes:
                node_data = {
                    "node": node,
                    "attributes": attributes
                }

            # Inserting the Fabric Node in the Graph inside the list
            nodes_data.append(node_data)

        # Saving the Graph Nodes List 'nodes_data' into the file
        try:

            with open(UserClass().Path + "GraphNodesData.yaml", 'w') as f:
                yaml.dump(nodes_data, f, indent=4, sort_keys=False)
                print(f" ✨ ✨ ✨ Graph data successfully saved in YAML format. ✨ ✨ ✨")

        except Exception as e:
            print(f"An error occurred while saving the file: {e} ❌")
