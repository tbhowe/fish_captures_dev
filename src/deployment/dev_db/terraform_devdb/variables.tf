variable "subscription_id" {
  description = "Azure Subscription ID"
}

variable "client_id" {
  description = "Azure Client ID"
}

variable "client_secret" {
  description = "Azure Client Secret"
}

variable "tenant_id" {
  description = "Azure Tenant ID"
}

variable "location" {
  description = "Location for all resources"
  default     = "UK South"
}

variable "postgres_admin_username" {
  description = "The administrator username for the PostgreSQL server"
  default = "fishcap_admin"
}

variable "postgres_admin_password" {
  description = "The administrator password for the PostgreSQL server"
  default = "peouerH00s3"
  
}
