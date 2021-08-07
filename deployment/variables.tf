variable "branch" {
  description = "Current github branch. Used for build and deploy artifact naming"
}

variable "application" {
  description = "Name of application being deployed"
  default = "titancraft"
}