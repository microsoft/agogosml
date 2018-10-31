provider "azurerm" {
    version = "~>1.5"
}

terraform {
    backend "azurerm" {
        storage_account_name = "agogosml"
        container_name       = "tfstate"
        key                  = "codelab.microsoft.tfstate"
    }
}