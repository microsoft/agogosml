resource azurerm_resource_group eh {
  name     = "${var.prefix}-${var.resource_group_name}"
  location = "${var.location}"
}

resource "azurerm_eventhub_namespace" eh {
  name                = "${var.namespace}"
  location            = "${azurerm_resource_group.eh.location}"
  resource_group_name = "${azurerm_resource_group.eh.name}"
  sku                 = "${var.sku}"
  capacity            = "${var.throughput_units}"
}

resource "azurerm_eventhub" eh {
  name                = "${var.eh_name}"
  namespace_name      = "${azurerm_eventhub_namespace.eh.name}"
  resource_group_name = "${azurerm_resource_group.eh.name}"
  partition_count     = "${var.eh_partition__count}"
  message_retention   = "${var.eh_retention}"
}

resource "azurerm_eventhub_authorization_rule" rule1 {
  name                = "send_rule"
  namespace_name      = "${azurerm_eventhub_namespace.eh.name}"
  eventhub_name       = "${azurerm_eventhub.eh.name}"
  resource_group_name = "${azurerm_resource_group.eh.name}"
  listen              = false
  send                = true
  manage              = false
}

resource "azurerm_eventhub_authorization_rule" rule2 {
  name                = "eph_rule"
  namespace_name      = "${azurerm_eventhub_namespace.eh.name}"
  eventhub_name       = "${azurerm_eventhub.eh.name}"
  resource_group_name = "${azurerm_resource_group.eh.name}"
  listen              = true
  send                = true
  manage              = true
}
