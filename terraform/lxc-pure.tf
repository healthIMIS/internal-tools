terraform {
	required_providers {
		proxmox = {
			source = "Telmate/proxmox"
			version = "2.7.4"
		}
	}
}

provider "proxmox" {
	pm_api_url = "https://<API_HERE>:8006/api2/json"
	pm_api_token_id = "<TOKEN_ID_HERE>"
	pm_api_token_secret = "<TOKEN_SECRET_HERE>"
	pm_tls_insecure = true
}

resource "proxmox_lxc" "basic" {
	target_node  = "pve"
	hostname     = "<HOSTNAME_HERE>"
	ostemplate   = "local:vztmpl/debian-11-standard_11.0-1_amd64.tar.xz"
	password     = "<PASSWORD_HERE>"
	unprivileged = true
	cores = 2
	memory = 1024
	swap = 0

	// Terraform will crash without rootfs defined
	rootfs {
		storage = "<STORAGE_NAME_HERE>"
		size    = "20G"
	}

	network {
		name   = "eth0"
		bridge = "vmbr0"
		ip     = "dhcp"
	}
}
