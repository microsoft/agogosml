# Retrieve storage credentials
storage_account = dbutils.secrets.get(scope = "storage_scope", key = "storage_account")
storage_key = dbutils.secrets.get(scope = "storage_scope", key = "storage_key")
storage_container = "databricks"

# Mount
dbutils.fs.mount(
  source = "wasbs://databricks@" + storage_account + ".blob.core.windows.net",
  mount_point = "/mnt/blob_storage/", 
  extra_configs = {"fs.azure.account.key." + storage_account + ".blob.core.windows.net": storage_key})

# Refresh mounts
dbutils.fs.refreshMounts()
