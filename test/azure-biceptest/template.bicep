@description('address prefix')
param vnetAddressPrefix string = '10.0.0.0/16'

@description('Subnet prefix')
param subnetPrefix string = '10.0.0.0/24'

@description('Location for all resources.')
param location string = resourceGroup().location

@description('Test int param.')
param testInt int = 30

@description('Test object param')
param testObj object = {'Foo': 'Bar'}

@description('Test array param')
param testArr array = ['Foo', 'Bar']

@description('Test bool param')
param testBool bool = false

var virtualNetworkName_var = 'NdtTestVNet'
var subnetName = 'NdtTestBackendSubnet'
var loadBalancerName_var = 'NdtTestLoadBalancer'
var nicName_var = 'NdtTestNIC1'
var lbsku = 'Standard'
var subnetRef = resourceId('Microsoft.Network/virtualNetworks/subnets', virtualNetworkName_var, subnetName)
var lbrulename = 'NdtTestHTTPRule'
var lbprobename = 'NdtTestHealthProbe'

resource virtualNetworkName 'Microsoft.Network/virtualNetworks@2020-05-01' = {
  name: virtualNetworkName_var
  location: location
  properties: {
    addressSpace: {
      addressPrefixes: [
        vnetAddressPrefix
      ]
    }
    subnets: [
      {
        name: subnetName
        properties: {
          addressPrefix: subnetPrefix
        }
      }
    ]
  }
}

resource nicName 'Microsoft.Network/networkInterfaces@2020-05-01' = {
  name: nicName_var
  location: location
  properties: {
    ipConfigurations: [
      {
        name: 'ipconfig1'
        properties: {
          privateIPAllocationMethod: 'Dynamic'
          subnet: {
            id: subnetRef
          }
          loadBalancerBackendAddressPools: [
            {
              id: resourceId('Microsoft.Network/loadBalancers/backendAddressPools', loadBalancerName_var, 'loadBalancerBackEnd')
            }
          ]
        }
      }
    ]
  }
  dependsOn: [
    loadBalancerName
  ]
}

resource loadBalancerName 'Microsoft.Network/loadBalancers@2020-05-01' = {
  name: loadBalancerName_var
  location: location
  sku: {
    name: lbsku
  }
  properties: {
    frontendIPConfigurations: [
      {
        name: 'loadBalancerFrontEnd'
        properties: {
          subnet: {
            id: subnetRef
          }
        }
      }
    ]
    backendAddressPools: [
      {
        name: 'loadBalancerBackEnd'
      }
    ]
    loadBalancingRules: [
      {
        properties: {
          frontendIPConfiguration: {
            id: resourceId('Microsoft.Network/loadBalancers/frontendIpConfigurations', loadBalancerName_var, 'loadBalancerFrontEnd')
          }
          backendAddressPool: {
            id: resourceId('Microsoft.Network/loadBalancers/backendAddressPools', loadBalancerName_var, 'loadBalancerBackEnd')
          }
          probe: {
            id: resourceId('Microsoft.Network/loadBalancers/probes', loadBalancerName_var, lbprobename)
          }
          protocol: 'Tcp'
          frontendPort: 80
          backendPort: 80
          enableTcpReset: true
          disableOutboundSnat: true
          idleTimeoutInMinutes: 15
        }
        name: lbrulename
      }
    ]
    probes: [
      {
        properties: {
          protocol: 'Tcp'
          port: 80
          intervalInSeconds: 15
          numberOfProbes: 2
        }
        name: lbprobename
      }
    ]
  }
  dependsOn: [
    virtualNetworkName
  ]
}
