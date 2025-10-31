"""Config migrations for versions older than 0.7.1 to 0.7.1."""

from logzero import logger

TO_VERSION = "0.7.1"


def migrate_ip_mode(config_dict):
    """Migrate old host_ipv6 and host_ipv4_fallback settings to host_ip_mode."""
    if "ssh" not in config_dict or not isinstance(config_dict["ssh"], dict):
        return config_dict

    ssh_config = config_dict["ssh"]

    # Check if migration has already been performed
    if "host_ip_mode" in ssh_config:
        # Remove old settings if they still exist
        ssh_config.pop("host_ipv6", None)
        ssh_config.pop("host_ipv4_fallback", None)
        return config_dict

    # Get old settings
    ipv6 = ssh_config.pop("host_ipv6", False)
    ipv4_fallback = ssh_config.pop("host_ipv4_fallback", True)

    # Translate to new ip_mode setting
    if ipv6 and ipv4_fallback:
        ip_mode = "auto"
    elif ipv6 and not ipv4_fallback:
        ip_mode = "v6"
    else:
        ip_mode = "v4"

    logger.debug(f"Migrating SSH IP settings: ipv6={ipv6}, ipv4_fallback={ipv4_fallback} -> ip_mode={ip_mode}")
    ssh_config["host_ip_mode"] = ip_mode

    return config_dict


def run_migrations(config_dict):
    """Run all migrations."""
    logger.info(f"Running config migrations for {TO_VERSION}.")
    config_dict = migrate_ip_mode(config_dict)
    config_dict["_version"] = TO_VERSION
    return config_dict
