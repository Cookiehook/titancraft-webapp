terraform {
  required_providers {
    aws = {
      source = "hashicorp/aws"
    }
  }
}

provider "aws" {
  region = "eu-west-2"
}

module "infrastructure" {
  source = "./infrastructure"

  application = var.application
}

module "rds" {
  source = "./rds"

  application = var.application
}

module "app" {
  source = "./app"

  application = var.application
  branch = var.branch
}
