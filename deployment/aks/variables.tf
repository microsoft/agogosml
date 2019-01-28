variable prefix {
    default = "az"
}

variable resource_group_name {
    default = "agogosml-k8s-rg"
}

variable location {
    default = "East US"
}

variable ssh_public_key {
    default = "~/.ssh/id_rsa.pub"
}

variable dns_sub_prefix {
    default = "k8stest"
}

variable cluster_name {
    default = "k8stest"
}

variable storage_account_name {
    default = "k8-agogosml"
}
