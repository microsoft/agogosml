local cloudVendorAzure = import 'manifest-cloudvendor-azure.libsonnet';

{
    "name": std.extVar('PROJECT_NAME'),
    "cloud": {
        "vendor": std.extVar('CLOUD_VENDOR'),
        "subscriptionId": "MISSING",
        "otherProperties": if std.extVar('CLOUD_VENDOR') == 'azure' then cloudVendorAzure else {}
    }
}
