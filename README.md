# Cisco ACI Fabric Diagnostics CLI Tool

## 🚀 Overview

The **Cisco ACI Fabric Diagnostics CLI Tool** is a Python-based utility designed to collect extensive health, configuration, and operational data from a Cisco Application Policy Infrastructure Controller (APIC) and the entire ACI fabric.

It leverages the **NetworkX** library to model the fabric as a graph, where **Nodes** represent physical devices (Spine, Leaf, APIC, Endpoints) and **Edges** represent physical and logical connections. This structure allows for comprehensive data collection and organization.

The tool provides a rich, interactive command-line interface (CLI) for real-time analysis and an export function for saving all collected data in JSON or YAML formats for external processing.

### Key Features:

* **Graph-based Modeling:** Uses `networkx` to represent the ACI fabric, including switches (Spine/Leaf), controllers (APIC), and connected endpoints (EPG Nodes).
* **Multi-threaded Data Collection:** Efficiently fetches data from the APIC using concurrent requests to minimize runtime.
* **Deep Hardware & Health Visibility:** Collects detailed information on PSUs, Fans, Supervisors, Linecards, SFPs, Faults, and File System usage for both Switches and APICs.
* **Interface-Level Diagnostics:** Gathers operational status, LLDP neighbor details, and interface counters for fabric and downlink ports.
* **Interactive CLI Menu:** Provides a structured, user-friendly menu for navigating and displaying collected data.
* **Data Export:** Allows exporting the entire graph's node data to **JSON** or **YAML** files.
* **Email Reporting (Commented out in `network_graph.py`):** Includes a class for generating and sending HTML health reports via email, indicating potential for integration with monitoring workflows.

## 📦 Prerequisites

To run this tool, you need the following:

1.  **Python 3.x**
2.  **Required Python Libraries:**
    * `networkx`
    * `requests`
    * `pyyaml`
    * `certifi`
    * `smtplib` (Standard Library, but listed for context)
    * `urllib3`
3.  **Cisco APIC Access:** A valid username and password with appropriate API access rights.

## 🛠️ Installation and Setup

### 1. Install Dependencies

You can install all necessary Python packages using `pip`:

```bash
    pip install networkx requests pyyaml certifi
```

## Configure Environment Variables

The script relies on several environment variables for secure access and configuration. These variables are defined and read in **UserClass.py** Class.

Set the following variables in your execution environment (e.g., in your shell profile or a startup script)

### Example setting environment variables in Linux/macOS:

```bash
    export USER="user"
    export UserPwd="mySecurePassword"
    export FabricGtmUrl="url"
    export FabricGraphPath="/path/to/script/root"
    export AciVer="5.2"
```

## 🚀 Usage

Execute the main script from the root directory:

```bash
    python network_graph.py
```

Upon successful execution, the script will log in to the APIC, fetch all necessary data, build the NetworkX graph, and present the main CLI menu.

## 🖥️ CLI Menu Structure

The interactive CLI provides a structured way to inspect the collected fabric data.

### Main Menu

| Option | Description |
| :--- | :--- |
| **0** | Exit the program and logout from APIC. |
| **1** | Controllers (APIC) Diagnostics Menu. |
| **2** | Switches (Spine/Leaf) Diagnostics Menu. |
| **3** | Switch Recommended Actions (e.g., Interfaces that should be down). |
| **4** | General Graph Methods (Raw node/edge attribute dump). |
| **5** | Export Data (JSON/YAML). |

### 1. Controllers (APIC) Menu

Focuses on the health and status of the APIC cluster members.

| Option | Description | Printer Method |
| :---: | :--- | :--- |
| **1** | Print APIC Database Sync Status | `printApicNodesBbddSyncStatusInfo` |
| **2** | Print APIC Filesystem Info | `printApicNodesFileSystemInfo` |
| **3** | Print APIC PSU Info | `printApicNodesPsuInfo` |
| **4** | Print APIC FAN Info | `printApicNodesFanInfo` |
| **5** | Print APIC Sensor Info | `printApicNodesSensorInfo` |
| **6** | Print APIC DIMM Info | `printApicNodesDimmsInfo` |
| **7** | Print APIC NTP Info | `printApicNodesNtpInfo` |
| **8** | Print APIC Physical Interface Info | `printApicNodesPhyIntInfo` |
| **9** | Print APIC Aggregate Interface Info | `printApicNodesAggIntInfo` |

### 2. Switches (Spine/Leaf) Menu

Provides a detailed look into the hardware, interfaces, and health of the fabric switches.

| Option | Description | Printer Method |
| :---: | :--- | :--- |
| **1** | Print Switch Node Interfaces | `getSwitchNodeInterfacesInfo` |
| **2** | Print Switch Node Supervisors | `getSwitchNodeSupervisorInfo` |
| **3** | Print Switch Node Faults | `getSwitchNodeFaultsInfo` |
| **4** | Print Spine Switch System Controllers (Spine Only) | `getSpineSwitchNodeSystemControllerInfo` |
| **5** | Print Spine Switch Fabric Modules (Spine Only) | `getSpineSwitchNodeFabricModulesInfo` |
| **6** | Print Switch Node PSUs | `getSwitchNodePsuInfo` |
| **7** | Print Switch Node Linecards | `getSwitchNodeLinecardInfo` |
| **8** | Print Switch Node SFP Info | `printSwitchNodesSfpInterfaceInfo` |
| **9** | Print Fabric Switches Filesystem | `printFabricSwitchesFilesystemNodes` |

### 3. Switch Recommended Actions Menu

Highlights potential configuration inconsistencies that should be addressed.

| Option | Description | Printer Method |
| :---: | :--- | :--- |
| **1** | Downlink Interfaces that Should be Down (Admin-Up, Oper-Down) | `getSwitchNodeInterfacesShouldBeDownInfo` |
| **2** | Fabric Interface Errors Brief | `printFabricEdgesWithErrorsCli`|
| **3** | Fabric Interface Errors Details | `printFabricEdgesWithErrorDetailsCli`|


### 3.1 Interface Error Brief

| Error Counter Type | Purpose/Significance |
| :---: | :--- |
| **cRCAlignErrors** | Packets with CRC or frame alignment errors (physical layer issue). |
| **collisions** | Packets that experienced a collision during transmission (should be 0 in full-duplex networks). |
| **dropEvents** | Packets dropped due to congestion or resource limitations. |
| **fragments** | Packets shorter than the minimum size (64 bytes) without a CRC error, often caused by late collisions. |
| **jabbers** | Packets longer than the maximum valid size (1518 bytes for standard Ethernet) with a CRC error (often points to a faulty network card). |
| **undersizePkts** | Received packets smaller than 64 bytes without a CRC error. |
| **oversizePkts** | Received packets larger than the maximum valid size but error-free. |
| **rxGiantPkts** | Received packets that exceeded the maximum frame size. |
| **rxOversizePkts** | Received packets larger than the maximum size of the interface. |
| **txGiantPkts** | Transmitted packets that exceeded the maximum frame size. |
| **txOversizePkts** | Transmitted packets larger than the maximum size of the interface. |
| **interface_operLastErrors** | A non-zero/non-empty string indicating the last error that occurred on the interface. |

### 4. General Graph Methods Menu

For developers or advanced users needing the raw data structure.

| Option | Description | Printer Method |
| :---: | :--- | :--- |
| **1** | Print Graph Nodes (Full Attribute Dump) | `printingNodeAttributes` |
| **2** | Print Graph Edges (Fabric Link Details) | `printAllFabricEdgesAttributesCli` |
| **3** | Print Graph EPG Nodes (Connected Endpoints) | `printAllNetworkDevicesNodesCli` |

### 5. Export Data Menu

Allows saving the entire node database for post-processing.

| Option | Description | Export Method |
| :---: | :--- | :--- |
| **1** | Export Graph Node JSON Format | `__save_graph_to_jsonfile` |
| **2** | Export Graph Node Yaml Format | `__save_graph_to_jsonYaml` |

### 📐 Architecture Breakdown

The project is structured with a clear separation of concerns, as seen in the file organization:

| File/Module | Description |
| :--- | :--- |
| `network_graph.py` | **Main Entry Point.** Initializes all objects, connects to APIC, builds the NetworkX graph, and starts the CLI menu. |
| `controller/aci_controller.py` | **Data Fetching Logic.** Contains `ACIController` which orchestrates API calls and concurrent data collection for each node (Switches & APICs). It manages LLDP neighbor and interface details to build the graph edges. |
| `parsers/aci_parser.py` | **Data Parsing Logic.** Contains `ACITroubleshooterParser` which takes raw JSON responses from the APIC and parses/cleans the data into standardized Python dictionaries and lists (e.g., removing unnecessary `dn`, `modTs` attributes). |
| `printers/aci_printers.py` | **CLI Output Logic.** Contains `ACITroubleshooterPrinter` with methods to format and print the structured data from the NetworkX graph into readable tables in the CLI. |
| `menu/aci_menu.py` | **User Interface.** Contains `MenuPrinter` to display the interactive menus, manage screen clearing, and call the appropriate printer methods based on user selection. |
| `aci_api_client/getCookie.py` | **API Client.** Manages the connection session, token retrieval, token refresh (`aaaRefresh`), and requests handling with the APIC API. |
| `aci_api_client/Url.py` | **API Endpoint Management.** Reads the `url.yaml` file and provides getter methods for all necessary APIC REST API endpoints. |
| `aci_api_client/UserClass.py` | **Configuration.** Retrieves user, password, APIC URL, and other necessary configuration parameters from environment variables. |
| `aci_api_client/url.yaml` | **Configuration File.** Centralized repository for all APIC REST API URI paths used by the tool. |

## 🔗 APIC API Endpoint Configuration

All API endpoints used for data collection are managed in **aci_api_client/url.yaml**. This makes the tool flexible and easier to update if APIC API paths change in future versions. The **UrlClass** dynamically reads and serves these URLs to the **ACIController**.

## 🧑💻 Development Notes

* Concurrency: The script uses **concurrent.futures.ThreadPoolExecutor** in **ACIController._process_node** to drastically reduce the time taken to collect data for each switch/APIC node, as most API calls are I/O-bound.

* Singleton Pattern: The **_PrivateCookie** metaclass implements the Singleton pattern for core classes (**getCookie**, **UrlClass**, **UserClass**, **ACIController**, **ACITroubleshooterParser**, **ACITroubleshooterPrinter**, **MenuPrinter**, **EmailReportGenerator**) to ensure only one instance of each is created, managing state and resource access efficiently.
