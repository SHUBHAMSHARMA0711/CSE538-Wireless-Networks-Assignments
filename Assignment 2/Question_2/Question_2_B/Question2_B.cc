#include "ns3/applications-module.h"
#include "ns3/core-module.h"
#include "ns3/csma-module.h"
#include "ns3/internet-module.h"
#include "ns3/mobility-module.h"
#include "ns3/network-module.h"
#include "ns3/point-to-point-module.h"
#include "ns3/ssid.h"
#include "ns3/yans-wifi-helper.h"

#include "tcp-example.h"

// Network Topology
//
//   Wifi 169.1.2.0
//                   AP
//  *  *    *    *    *
//  |  |    |    |    |    169.1.1.0
//  W4 W3   W2   W1  R1 -------------- R2   C2   C3
//                   |  point-to-point  |    |    |
//                 ====                 ============
//                 |                   ETH 169.1.4.0
//                 C1
//                 169.1.3.0

using namespace ns3;

int main(int argc, char* argv[])
{
    int R1 = 0;
    int R2 = 1;

    /* Created two Routers, R1 and R2, connected directly through a P2P link.*/

    NodeContainer router;
    router.Create(2);

    PointToPointHelper pointToPoint_Between_R1_R2;
    pointToPoint_Between_R1_R2.SetDeviceAttribute("DataRate", StringValue("100Mbps"));
    pointToPoint_Between_R1_R2.SetChannelAttribute("Delay", StringValue("2ms"));

    NetDeviceContainer p2pDevices_R1_R2 = pointToPoint_Between_R1_R2.Install(router);; 



    /* Router R1 is acting as an AP serving four WiFi devices W1 to W4.*/

    NodeContainer wifiNodes; // Creating Wifi Nodes
    wifiNodes.Create(4);
    
    NodeContainer R1_AP = router.Get(R1); // Setiing R1 as AP
    
    YansWifiPhyHelper PHY;
    PHY.SetChannel(YansWifiChannelHelper::Default().Create());

    WifiHelper WIFI; // Configuring MAC layer and Installing AP and Station devices
    WifiMacHelper MAC;
    MAC.SetType("ns3::ApWifiMac" , "Ssid", SsidValue(Ssid("Question-2")));
    NetDeviceContainer APDevice  = WIFI.Install(PHY, MAC, R1_AP);
    MAC.SetType("ns3::StaWifiMac", "Ssid", SsidValue(Ssid("Question-2")), "ActiveProbing", BooleanValue(false));
    NetDeviceContainer STADevice = WIFI.Install(PHY, MAC, wifiNodes);

    MobilityHelper mobility;
    mobility.SetMobilityModel("ns3::ConstantPositionMobilityModel");
    mobility.Install(R1_AP);
    mobility.SetMobilityModel("ns3::RandomWalk2dMobilityModel","Bounds", RectangleValue(Rectangle(-50, 50, -50, 50)));
    mobility.Install(wifiNodes);
    


    /* Computer C1 is also connected to R1 using a Wired Connection.*/

    NodeContainer C1;
    C1.Add(router.Get(R1));
    C1.Create(1);  

    CsmaHelper CSMA_Between_R1_C1;
    CSMA_Between_R1_C1.SetChannelAttribute("DataRate", StringValue("100Mbps"));
    CSMA_Between_R1_C1.SetChannelAttribute("Delay", TimeValue(NanoSeconds(2000)));

    NetDeviceContainer CSMA_Device_R1_C1 = CSMA_Between_R1_C1.Install(C1);



    /* Computer C2 and C3, connected to R2 via an Ethernet network.*/

    NodeContainer nodes_C2_C3;
    nodes_C2_C3.Add(router.Get(R2));
    nodes_C2_C3.Create(2);

    CsmaHelper C2_C3;
    C2_C3.SetChannelAttribute("DataRate", StringValue("100Mbps"));
    C2_C3.SetChannelAttribute("Delay", TimeValue(NanoSeconds(2000)));

    NetDeviceContainer CSMA_Devices_C2_C3 = C2_C3.Install(nodes_C2_C3);

    

    /* Installing Internet Stack on all the devices*/

    InternetStackHelper stack;
    stack.Install(wifiNodes);
    stack.Install(R1_AP);
    stack.Install(C1);
    stack.Install(nodes_C2_C3);
    
    
    
    /* Assigning IP addresses to Devices*/

    Ipv4AddressHelper address;

    address.SetBase("169.1.1.0", "255.255.255.0");
    address.Assign(p2pDevices_R1_R2);

    address.SetBase("169.1.2.0", "255.255.255.0");
    
    Ipv4InterfaceContainer STAInterface = address.Assign(STADevice);
    address.Assign(APDevice);

    address.SetBase("169.1.3.0", "255.255.255.0");
    Ipv4InterfaceContainer C1_Interface = address.Assign(CSMA_Device_R1_C1);

    address.SetBase("169.1.4.0", "255.255.255.0");
    Ipv4InterfaceContainer C2_C3_Ethernet = address.Assign(CSMA_Devices_C2_C3);
    


    /* Installing and running TCP Application on nodes C1, C3 and W4.*/

    Address serverAddress_C1(InetSocketAddress(C1_Interface.GetAddress(1), 69));
    PacketSinkHelper Server_C1("ns3::TcpSocketFactory", InetSocketAddress(Ipv4Address::GetAny(), 69));
    ApplicationContainer serverApp_C1 = Server_C1.Install(C1.Get(1));
    serverApp_C1.Start(Seconds(1));
    serverApp_C1.Stop(Seconds(10));

    Ptr<MyApp> clientApp_C3 = CreateObject<MyApp>();
    clientApp_C3       -> Setup(Socket::CreateSocket(nodes_C2_C3.Get(2), TcpSocketFactory::GetTypeId()), serverAddress_C1, 2048, 100, DataRate("100Mbps"));
    nodes_C2_C3.Get(2) -> AddApplication(clientApp_C3);
    clientApp_C3       -> SetStartTime(Seconds(2));
    clientApp_C3       -> SetStopTime(Seconds(100));

    Ptr<MyApp> clientApp_W4 = CreateObject<MyApp>();
    clientApp_W4       -> Setup(Socket::CreateSocket(wifiNodes.Get(3), TcpSocketFactory::GetTypeId()), serverAddress_C1, 2048, 100, DataRate("100Mbps"));
    wifiNodes.Get(3)   -> AddApplication(clientApp_W4);
    clientApp_W4       -> SetStartTime(Seconds(2));
    clientApp_W4       -> SetStopTime(Seconds(100));


    Ipv4GlobalRoutingHelper::PopulateRoutingTables();
    Simulator::Stop(Seconds(100));

    PHY.SetPcapDataLinkType(WifiPhyHelper::DLT_IEEE802_11_RADIO);
    PHY.EnablePcap("W4_TCP", STADevice.Get(3), true);
    C2_C3.EnablePcap("C3_TCP", CSMA_Devices_C2_C3.Get(2), true);
    CSMA_Between_R1_C1.EnablePcap("C1_TCP", CSMA_Device_R1_C1.Get(1), true);
    

    Simulator::Run();
    Simulator::Destroy();
    return 0;
}