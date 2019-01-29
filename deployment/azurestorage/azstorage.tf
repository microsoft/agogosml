resource azurerm_resource_group rg {
  name     = "${var.prefix}_${var.resource_group_name}"
  location = "${var.location}"
}

resource "azurerm_storage_account" "storage_account" {
  name                     = "${var.storage_account_name}"
  resource_group_name      = "${azurerm_resource_group.rg.name}"
  location                 = "${var.location}"
  account_tier             = "${var.account_tier}"
  account_replication_type = "${var.account_replication_type}"
}

resource "azurerm_storage_container" "cont-input" {
  name                  = "${var.storage_container_name_input}"
  resource_group_name   = "${azurerm_resource_group.rg.name}"
  storage_account_name  = "${azurerm_storage_account.storage_account.name}"
  container_access_type = "private"
}

resource "azurerm_storage_container" "cont-output" {
  name                  = "${var.storage_container_name_output}"
  resource_group_name   = "${azurerm_resource_group.rg.name}"
  storage_account_name  = "${azurerm_storage_account.storage_account.name}"
  container_access_type = "private"
}