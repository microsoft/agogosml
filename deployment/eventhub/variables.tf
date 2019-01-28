variable prefix {
  default = "az"
}

variable resource_group_name {
  default = "agogos-rg"
}

variable location {
  default = "East US"
}

variable namespace {
  default = "agogosmleh"
}

variable sku {
  default = "Standard"
}

variable throughput_units {
  default = 1
}

variable eh_name_input {
  default = "agogosml-eh-output"
}

variable eh_name_output {
  default = "agogosml-eh-input"
}

variable eh_partition__count {
  default = 2
}

variable eh_retention {
  default = 1
}

variable kafka_enabled {
  default = "false"
}
