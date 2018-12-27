# Retrieve storage credentials
storage_account = dbutils.secrets.get(scope="storage_scope", key="storage_account")  # noqa: F821
storage_key = dbutils.secrets.get(scope="storage_scope", key="storage_key")  # noqa: F821
storage_container = "databricks"

# Mount
dbutils.fs.mount(  # noqa: F821
  source="wasbs://databricks@" + storage_account + ".blob.core.windows.net",
  mount_point="/mnt/blob_storage/",
  extra_configs={"fs.azure.account.key." + storage_account + ".blob.core.windows.net": storage_key})

# Refresh mounts
dbutils.fs.refreshMounts()  # noqa: F821
