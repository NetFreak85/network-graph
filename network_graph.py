####################################################################################
# Cisco ACI Troubleshooting Script based on Graphs with library NetworkX           #
# The Script connect to the Cisco ACI APIC to fetch all the following information: #
# Hardware:                                                                        #
#    Switches:                                                                     #
#       - Chasis Info                                                              #
#       - Supervisor                                                               #
#       - Linecards                                                                #
#           - Ports Adming Status                                                  #
#           - Ports Operational Status                                             #
#           - EPGs deployed per Interface based                                    # 
#       - Fans                                                                     #
#       - Power Supply Units (PSU)                                                 #
#       - File System                                                              #
#       - Fabric Modules (Only for Spine Swiches)                                  #
#       - System Controller (Only for Spine Switches)                              #
#     Controllers:                                                                 #
#                                                                                  #
####################################################################################

##################
# Import Section #
##################

from aci_api_client.getCookie import getCookie
from aci_api_client.Url import UrlClass
from aci_api_client.UserClass import UserClass
from menu.aci_menu import MenuPrinter
from controller.aci_controller import ACIController
from report.email_reporter import EmailReportGenerator
import networkx as nx

#######################
# Function Definition #
#######################

################
# Main Program #
################

if __name__ == '__main__':

    # Generating a networkx Graph Object
    network_graph: nx.Graph = nx.Graph()

    # Object that will print in the CLI all the information collected in the Graph
    #myPrinter = ACITroubleshooterPrinter()

    # Object that will print the Menu for the User
    Menu: MenuPrinter = MenuPrinter()

    # Object that will grant access to the Cisco ACI Fabric
    User: UserClass = UserClass()

    # Object that provide the uris necesaries for restconf queries
    Urls: UrlClass = UrlClass()

    # Object that provide the Nodes and Edges list
    AciController: ACIController = ACIController()

    # Object that will perform the restconf querie
    main_cookie: getCookie = getCookie(User.user, User.pwd, User.base_url, Urls.getTokenV5())

    # List of nodes detected in the Cisco ACI Fabric
    nodeList: list = []

    # List of Edges detected in the Cisco ACI Fabric
    edgeList: list = []

    # Feching Node List information
    nodeList, edgeList = AciController.getNodesList(main_cookie, Urls, User)

    # Adding nodes to the Network Graph Object from Node List
    network_graph.add_nodes_from(nodeList)

    # Adding Edges to the Network Graph Object from edge List
    network_graph.add_edges_from(edgeList)

    #email_report_gen = EmailReportGenerator(
    #    User.getEmailSender(),
    #    User.getSmtpServer(),
    #    User.getUserEmailToken(),
    #    User.getEmailReceiver(),
    #    User.getSmtpServerPort()
    #    )

    ## Send the report
    #email_report_gen.send_report(nodeList, edgeList, subject="ACI Fabric Report")

    # Printing Menu Based on the Graph 'network_graph' created with the aci_controller Class
    Menu.mainMenu(network_graph)

    # Logout from Cisco ACI Token
    main_cookie.aaaLogout()
