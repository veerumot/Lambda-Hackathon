module "IAM" {
    source = "./modules/IAM-Role"
}

module "S3" {
    source = "./modules/S3"
}

module "Lambda" {
    source = "./modules/Lambda"
    lambda_execution_role_arn = module.IAM.ec2_lambda_role_arn
}