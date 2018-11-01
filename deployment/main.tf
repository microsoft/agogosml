provider "azurerm" {
    version = "~>1.5"
}

terraform {
    backend "azurerm" {
        container_name       = "tfstate"
        key                  = "codelab.microsoft.tfstate"
    }
}