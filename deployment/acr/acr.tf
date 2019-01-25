resource "azurerm_resource_group" "rg" {
  name     = "${var.prefix}_${var.resource_group_name}"
  location = "East US"
}

resource "azurerm_container_registry" "acr" {
  name                     = "${var.acr_name}"
  resource_group_name      = "${azurerm_resource_group.rg.name}"
  location                 = "${azurerm_resource_group.rg.location}"
  sku                      = "${var.sku}"
  admin_enabled            = "${var.admin_enabled}"
  georeplication_locations = ["East US2", "West Europe"]
}