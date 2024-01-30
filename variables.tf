variable "client_id" {
  default = "0000-0000-0000-0000"
}

variable "keyvaultname" {
  default = "keyvault"
}

variable "dns_zone_prefix" {
  default = "campus"
}

variable "dhcpd_loadbalancer_ip" {
  default = "10.0.0.250"
}

variable "giturl" {
  default = "https://cnaas:$(GIT_TOKEN)@gitlab.surf.nl/surf-wired/cnaas-templates.git"
}

variable "branch" {
  default = "master"
}