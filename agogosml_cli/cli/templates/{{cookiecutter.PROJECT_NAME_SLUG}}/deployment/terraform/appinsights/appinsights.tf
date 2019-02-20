resource azurerm_resource_group rg {
  name     = "${var.prefix}_${var.resource_group_name}"
  location = "${var.location}"
}

resource "azurerm_application_insights" appinsights {
  name                = "${var.appinsights_name}"
  location            = "${var.location}"
  resource_group_name = "${azurerm_resource_group.rg.name}"
  application_type    = "Other"
}
