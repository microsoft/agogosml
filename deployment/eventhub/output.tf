output "eventhub_namespace_name" {
  value = "${azurerm_eventhub_namespace.eh.name}"
}

output "eventhub_name" {
  value = "${azurerm_eventhub.eh.name}"
}

output "eventhub_send_rule_name" {
  value = "${azurerm_eventhub_authorization_rule.rule1.name}"
}

output "eventhub_send_rule_key" {
  value = "${azurerm_eventhub_authorization_rule.rule1.primary_key}"
}

output "eventhub_eph_rule_name" {
  value = "${azurerm_eventhub_authorization_rule.rule2.name}"
}

output "eventhub_eph_rule_key" {
  value = "${azurerm_eventhub_authorization_rule.rule2.primary_key}"
}
