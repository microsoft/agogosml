resource azurerm_resource_group k8s {
    name     = "${var.prefix}-${var.resource_group_name}"
    location = "${var.location}"
}

resource azurerm_network_security_group k8s {
  name                = "${var.prefix}-${var.nsg_name}"
  location            = "${azurerm_resource_group.k8s.location}"
  resource_group_name = "${azurerm_resource_group.k8s.name}"
}

resource azurerm_virtual_network k8s {
  name                = "${var.prefix}-${var.vnet_name}"
  location            = "${azurerm_resource_group.k8s.location}"
  resource_group_name = "${azurerm_resource_group.k8s.name}"
  address_space       = ["${var.address_space}"]
}

resource azurerm_subnet k8s {
  name                      = "${var.prefix}-${var.subnet_name}"
  resource_group_name       = "${azurerm_resource_group.k8s.name}"
  network_security_group_id = "${azurerm_network_security_group.k8s.id}"
  address_prefix            = "${var.address_prefix}"
  virtual_network_name      = "${azurerm_virtual_network.k8s.name}"
}

resource azurerm_log_analytics_workspace k8s {
  name                = "${var.prefix}-${var.log_solution_name}"
  location            = "${azurerm_resource_group.k8s.location}"
  resource_group_name = "${azurerm_resource_group.k8s.name}"
  sku                 = "${var.log_solution_sku}"
}

resource azurerm_log_analytics_solution k8s {
  solution_name         = "${var.log_analytics_name}"
  location              = "${azurerm_resource_group.k8s.location}"
  resource_group_name   = "${azurerm_resource_group.k8s.name}"
  workspace_resource_id = "${azurerm_log_analytics_workspace.k8s.id}"
  workspace_name        = "${azurerm_log_analytics_workspace.k8s.name}"

  plan {
    publisher = "Microsoft"
    product   = "OMSGallery/ContainerInsights"
  }
}


resource azurerm_kubernetes_cluster k8s {
    name                = "${var.prefix}-${var.cluster_name}"
    location            = "${azurerm_resource_group.k8s.location}"
    resource_group_name = "${azurerm_resource_group.k8s.name}"
    dns_prefix          = "${var.prefix}-${var.dns_sub_prefix}"

    linux_profile {
        admin_username = "ubuntu"

        ssh_key {
            key_data = "${file("${var.ssh_public_key}")}"
        }
    }

    agent_pool_profile {
        name            = "default"
        count           = "${var.agent_count}"
        vm_size         = "${var.agent_size}"
        os_type         = "Linux"
        os_disk_size_gb = "${var.agent_disk_size_gb}"

        # Required for advanced networking
        vnet_subnet_id = "${azurerm_subnet.k8s.id}"
    }

    service_principal {
        client_id     = "${var.client_id}"
        client_secret = "${var.client_secret}"
    }

    addon_profile {
        oms_agent {
            enabled                    = true
            log_analytics_workspace_id = "${azurerm_log_analytics_workspace.k8s.id}"
        }
    }

    network_profile {
        network_plugin = "${var.network_plugin}"
    }

    tags {
        Environment = "Development"
    }
}