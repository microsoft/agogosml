variable nsg_name {
    description = "Network security group name"
    default = "1-nsg"
}

variable vnet_name {
    description = "virtual network name"
    default = "1-vnet"
}

variable subnet_name {
    default = "1-subnet"
}

variable address_space {
  default = "10.1.0.0/16"
}

variable address_prefix {
  default = "10.1.0.0/24"
}

variable network_plugin {
  default = "azure"
}
