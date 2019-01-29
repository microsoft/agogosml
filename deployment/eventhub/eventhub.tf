resource azurerm_resource_group eh {
  name     = "${var.prefix}_${var.resource_group_name}"
  location = "${var.location}"
}

resource "azurerm_eventhub_namespace" eh {
  name                = "${var.namespace}"
  location            = "${azurerm_resource_group.eh.location}"
  resource_group_name = "${azurerm_resource_group.eh.name}"
  sku                 = "${var.sku}"
  capacity            = "${var.throughput_units}"
  kafka_enabled       = "${var.kafka_enabled}"
}

resource "azurerm_eventhub" eh_input {
  name                = "${var.eh_name_input}"
  namespace_name      = "${azurerm_eventhub_namespace.eh.name}"
  resource_group_name = "${azurerm_resource_group.eh.name}"
  partition_count     = "${var.eh_partition__count}"
  message_retention   = "${var.eh_retention}"
}

resource "azurerm_eventhub" eh_output {
  name                = "${var.eh_name_output}"
  namespace_name      = "${azurerm_eventhub_namespace.eh.name}"
  resource_group_name = "${azurerm_resource_group.eh.name}"
  partition_count     = "${var.eh_partition__count}"
  message_retention   = "${var.eh_retention}"
}

resource "azurerm_eventhub_authorization_rule" rule1_output {
  name                = "send_rule"
  namespace_name      = "${azurerm_eventhub_namespace.eh.name}"
  eventhub_name       = "${azurerm_eventhub.eh_output.name}"
  resource_group_name = "${azurerm_resource_group.eh.name}"
  listen              = false
  send                = true
  manage              = false
}

resource "azurerm_eventhub_authorization_rule" rule2_output {
  name                = "eph_rule"
  namespace_name      = "${azurerm_eventhub_namespace.eh.name}"
  eventhub_name       = "${azurerm_eventhub.eh_output.name}"
  resource_group_name = "${azurerm_resource_group.eh.name}"
  listen              = true
  send                = true
  manage              = true
}

resource "azurerm_eventhub_authorization_rule" rule1_input {
  name                = "send_rule"
  namespace_name      = "${azurerm_eventhub_namespace.eh.name}"
  eventhub_name       = "${azurerm_eventhub.eh_input.name}"
  resource_group_name = "${azurerm_resource_group.eh.name}"
  listen              = false
  send                = true
  manage              = false
}

resource "azurerm_eventhub_authorization_rule" rule2_input {
  name                = "eph_rule"
  namespace_name      = "${azurerm_eventhub_namespace.eh.name}"
  eventhub_name       = "${azurerm_eventhub.eh_input.name}"
  resource_group_name = "${azurerm_resource_group.eh.name}"
  listen              = true
  send                = true
  manage              = true
}
