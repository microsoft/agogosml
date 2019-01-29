output "eventhub_namespace_name" {
  value = "${azurerm_eventhub_namespace.eh.name}"
}

output "eventhub_name_output" {
  value = "${azurerm_eventhub.eh_output.name}"
}
output "eventhub_name_input" {
  value = "${azurerm_eventhub.eh_input.name}"
}


output "eventhub_send_rule_name_input" {
  value = "${azurerm_eventhub_authorization_rule.rule1_input.name}"
}

output "eventhub_send_rule_key_input" {
  value = "${azurerm_eventhub_authorization_rule.rule1_input.primary_key}"
}

output "eventhub_eph_rule_name_input" {
  value = "${azurerm_eventhub_authorization_rule.rule2_input.name}"
}

output "eventhub_eph_rule_key_input" {
  value = "${azurerm_eventhub_authorization_rule.rule2_input.primary_key}"
}

output "eventhub_send_rule_name_output" {
  value = "${azurerm_eventhub_authorization_rule.rule1_output.name}"
}

output "eventhub_send_rule_key_output" {
  value = "${azurerm_eventhub_authorization_rule.rule1_output.primary_key}"
}

output "eventhub_eph_rule_name_output" {
  value = "${azurerm_eventhub_authorization_rule.rule2_output.name}"
}

output "eventhub_eph_rule_key_output" {
  value = "${azurerm_eventhub_authorization_rule.rule2_output.primary_key}"
}
