# AWS Database Performance – Infrastructure as Code

Theodor Harmse — University of Liverpool — Database Performance

## Table of Contents
- [Overview](#overview)
- [Prerequisites](#prerequisites)
- [Repository Layout](#repository-layout)
- [Deployment Order (Ireland / eu-west-1)](#deployment-order-ireland--eu-west-1)
  - [1. Networking & Security](#1.-networking-security)
  - [2. Database Setup](#2.-database-setup)
  - [3. API Layer](#3.-api-layer)
  - [4. CI/CD Pipeline](#4.-cicd-pipeline)
- [Post-Deployment: Apache JMeter](#post-deployment-apache-jmeter)
- [Operations & Troubleshooting](#operations--troubleshooting)
- [Notes & Quotas](#notes--quotas)

## Overview

This repository provisions a complete environment in **AWS eu-west-1 (Ireland)** to benchmark multiple database engines using an API layer and **Apache JMeter**. All infrastructure is defined in **AWS CloudFormation** and must be deployed **in the order below** using the **default parameters** unless you have a specific reason to override.

> **Why stack names matter:** Several templates export values and other templates **import** those values via `!ImportValue`. To avoid editing parameters, **use the exact stack names recommended for each template** (e.g., `Networking`, `DB-Subnet-Group`).

## Prerequisites

### Local workstation
- **Visual Studio Community Edition**
- **AWS CLI** – [Install the AWS CLI](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html)
- Configure the CLI (only needed for validations inside Visual Studio):
  ```bash
  aws configure
  # Region: eu-west-1
  # Access key & secret: (your IAM user)
  ```
- **(Optional) Lint CloudFormation**
  ```bash
  pip install cfn-lint
  ```
- **Clone this repository** : `https://github.com/THarmse/AWSDatabasePerformance.git`

### AWS account (Ireland)
- **Region:** `eu-west-1`
- **Quotas to request early:**
  - EC2 **vCPU limit**: increase to **64 vCPUs** for the m-class, r-class and t-class (On Demand).
  - **SSM Parameter Store** `GetParameter` API: raise to **300** requests/sec.
- **IBM Db2 SE** (if performance testing is done here): ensure an **active AWS Marketplace subscription** before deploying the Db2 template.
- **GitHub connection** (for CI/CD): create a **CodeStar Connections** link to GitHub in **eu-west-1** and note the **Connection ARN**.
- **EC2 key pair** (optional): create one in **eu-west-1** if you plan to SSH to instances.

## Repository Layout

```text
cloudformation/1. Networking and Security Groups/1. Networking.yaml
cloudformation/1. Networking and Security Groups/2. VPC Endpoints.yaml
cloudformation/1. Networking and Security Groups/3. Database Subnet Group.yaml
cloudformation/1. Networking and Security Groups/4. Private Hosted Zone.yaml
cloudformation/1. Networking and Security Groups/5. Security Groups and Ports.yaml
cloudformation/2. Database Setup/Aurora MySQL/1. RDS Aurora MySQL Cluster.yaml
cloudformation/2. Database Setup/Aurora PostgreSQL/1. RDS Aurora PostgreSQL Cluster.yaml
cloudformation/2. Database Setup/DynamoDB/1. DynamoDB Table.yaml
cloudformation/2. Database Setup/IBM DB2/1. RDS IBM DB2 SE.yaml
cloudformation/2. Database Setup/Maria DB/1. RDS MariaDB Instance.yaml
cloudformation/2. Database Setup/MS SQL Server/1. RDS MS SQL Server SE.yaml
cloudformation/2. Database Setup/MySQL/1. RDS MySQL Instance.yaml
cloudformation/2. Database Setup/Oracle DB/1. RDS Oracle SE.yaml
cloudformation/2. Database Setup/PostgreSQL/1. RDS PostgreSQL Instance.yaml
cloudformation/3. API/1. NLB, Target Group, API EC2.yaml
cloudformation/4. CICD Pipeline/1. CICD Pipeline.yaml
```

## Deployment Order (Ireland / eu-west-1)

Deploy **exactly** in this order. Use the **recommended stack names** so cross‑stack imports work without editing parameters.

### 1. Networking & Security

#### 🔒 Networking (VPC, Subnets, Route Tables, NAT, Flow Logs)

- **Template:** `cloudformation/1. Networking and Security Groups/1. Networking.yaml`
- **Recommended stack name:** `Networking`
- **Summary:** Creates foundational VPC and subnets across tiers with route tables, NAT gateways, and VPC Flow Logs.

**Deploy (using the AWS Console)**

1. Sign in to the **AWS Management Console**.
2. Open **CloudFormation (Ireland)**: https://eu-west-1.console.aws.amazon.com/cloudformation/home?region=eu-west-1
3. Click **Create stack** and select **With new resources (standard)**.
4. Under **Prerequisite - Prepare template**, make sure **Template is ready** (choose an existing template) is selected.
5. Under **Specify template**, select **Upload a template file**.
6. Click **Choose file**.
7. Browse to and select the CloudFormation template **(.yaml)** from this repository.
8. Click **Next**, then enter a **Stack name**. If this README lists a **Recommended stack name** for the template, use it **exactly** as shown.
9. Ensure all required **Parameters** are filled out (defaults are provided where applicable).
10. Click **Next**, review, acknowledge any required capabilities (e.g., **IAM**), and choose **Create stack** to deploy.


**Parameters**

| Parameter | Type | Default | Allowed Values | Description |
| --- | --- | --- | --- | --- |
| EnvironmentName | String | liverpool |  | Environment Name (e.g., dev, staging, prod, liverpool) in lowercase only |
| VPCCIDR | String | 10.0.0.0/16 |  | CIDR block for the VPC |
| PublicSubnet1CIDR | String | 10.0.1.0/24 |  | CIDR block for Public Subnet 1 (AZ a) |
| PublicSubnet2CIDR | String | 10.0.2.0/24 |  | CIDR block for Public Subnet 2 (AZ b) |
| PublicSubnet3CIDR | String | 10.0.3.0/24 |  | CIDR block for Public Subnet 3 (AZ a) |
| PublicSubnet4CIDR | String | 10.0.4.0/24 |  | CIDR block for Public Subnet 4 (AZ b) |
| PrivateSubnet1CIDR | String | 10.0.5.0/24 |  | CIDR block for Private Subnet 1 (AZ a) |
| PrivateSubnet2CIDR | String | 10.0.6.0/24 |  | CIDR block for Private Subnet 2 (AZ b) |
| PrivateSubnet3CIDR | String | 10.0.7.0/24 |  | CIDR block for Private Subnet 3 (AZ a) |
| PrivateSubnet4CIDR | String | 10.0.8.0/24 |  | CIDR block for Private Subnet 4 (AZ b) |
| PrivateSubnet5CIDR | String | 10.0.9.0/24 |  | CIDR block for Private Subnet 5 (AZ a) |
| PrivateSubnet6CIDR | String | 10.0.10.0/24 |  | CIDR block for Private Subnet 6 (AZ b) |
| PublicTier1Name | String | nat |  | Name of the Public Tier (NAT) |
| PublicTier2Name | String | elb |  | Name of the Public Tier (ELB) |
| PrivateTier1Name | String | web |  | Name of the Private Tier 1 (Web Tier) |
| PrivateTier2Name | String | app |  | Name of the Private Tier 2 (App Tier) |
| PrivateTier3Name | String | data |  | Name of the Private Tier 3 (Data Tier) |
| NumberOfNATGateways | Number | 2 | 0, 1, 2 | Number of NAT Gateways to create |

**Outputs & export names**

| Output key | Export name | Description |
| --- | --- | --- |
| VPCId | ${AWS::StackName}-VPCId | The ID of the VPC |
| PublicSubnet1Id | ${AWS::StackName}-PublicSubnet1Id | The ID of Tier 1 Public Subnet A in AZ A (Public Tier) |
| PublicSubnet2Id | ${AWS::StackName}-PublicSubnet2Id | The ID of Tier 1 Public Subnet B in AZ B (Public Tier) |
| PublicSubnet3Id | ${AWS::StackName}-PublicSubnet3Id | The ID of Tier 2 Public Subnet A in AZ A (Public Tier) |
| PublicSubnet4Id | ${AWS::StackName}-PublicSubnet4Id | The ID of Tier 2 Public Subnet B in AZ B (Public Tier) |
| PrivateSubnet1Id | ${AWS::StackName}-PrivateSubnet1Id | The ID of Tier 1 Private Subnet A in AZ A (Web Tier) |
| PrivateSubnet2Id | ${AWS::StackName}-PrivateSubnet2Id | The ID of Tier 1 Private Subnet B in AZ B (Web Tier) |
| PrivateSubnet3Id | ${AWS::StackName}-PrivateSubnet3Id | The ID of Tier 2 Private Subnet A in AZ A (App Tier) |
| PrivateSubnet4Id | ${AWS::StackName}-PrivateSubnet4Id | The ID of Tier 2 Private Subnet B in AZ B (App Tier) |
| PrivateSubnet5Id | ${AWS::StackName}-PrivateSubnet5Id | The ID of Tier 3 Private Subnet A in AZ A (DB Tier) |
| PrivateSubnet6Id | ${AWS::StackName}-PrivateSubnet6Id | The ID of Tier 3 Private Subnet B in AZ B (DB Tier) |
| PrivateRouteTable1Id | ${AWS::StackName}-PrivateRouteTable1Id | The ID of Private Route Table 1 (Web Tier) |
| PrivateRouteTable2Id | ${AWS::StackName}-PrivateRouteTable2Id | The ID of Private Route Table 2 (Web Tier) |
| PrivateRouteTable3Id | ${AWS::StackName}-PrivateRouteTable3Id | The ID of Private Route Table 3 (App Tier) |
| PrivateRouteTable4Id | ${AWS::StackName}-PrivateRouteTable4Id | The ID of Private Route Table 4 (App Tier) |
| PrivateRouteTable5Id | ${AWS::StackName}-PrivateRouteTable5Id | The ID of Private Route Table 5 (DB Tier) |
| PrivateRouteTable6Id | ${AWS::StackName}-PrivateRouteTable6Id | The ID of Private Route Table 6 (DB Tier) |
| PublicRouteTable1Id | ${AWS::StackName}-PublicRouteTable1Id | The ID of Public Route Table 1 (Public Tier) |
| PublicRouteTable2Id | ${AWS::StackName}-PublicRouteTable2Id | The ID of Public Route Table 2 (Public Tier) |
| VPCFlowLogsBucket | ${AWS::StackName}-VPCFlowLogsBucket | The S3 Bucket Name for storing VPC Flow Logs |


#### VPC Endpoints (S3 & DynamoDB)

- **Template:** `cloudformation/1. Networking and Security Groups/2. VPC Endpoints.yaml`
- **Recommended stack name:** `VPC-Endpoints`
- **Summary:** Creates Gateway VPC Endpoints for S3 and DynamoDB and associates them to private route tables.

**Deploy (using the AWS Console)**

1. Sign in to the **AWS Management Console**.
2. Open **CloudFormation (Ireland)**: https://eu-west-1.console.aws.amazon.com/cloudformation/home?region=eu-west-1
3. Click **Create stack** and select **With new resources (standard)**.
4. Under **Prerequisite - Prepare template**, make sure **Template is ready** (choose an existing template) is selected.
5. Under **Specify template**, select **Upload a template file**.
6. Click **Choose file**.
7. Browse to and select the CloudFormation template **(.yaml)** from this repository.
8. Click **Next**, then enter a **Stack name**. If this README lists a **Recommended stack name** for the template, use it **exactly** as shown.
9. Ensure all required **Parameters** are filled out (defaults are provided where applicable).
10. Click **Next**, review, acknowledge any required capabilities (e.g., **IAM**), and choose **Create stack** to deploy.


**Parameters**

| Parameter | Type | Default | Allowed Values | Description |
| --- | --- | --- | --- | --- |
| Region | String | eu-west-1 | eu-west-1, eu-central-1, us-east-1, us-east-2, us-west-1, us-west-2 | AWS Region for deployment |

**Outputs & export names**

| Output key | Export name | Description |
| --- | --- | --- |
| DynamoDBVPCEndpointId | Networking-DynamoDBVPCEndpointId | ID of the created DynamoDB VPC Endpoint |
| S3VPCEndpointId | Networking-S3VPCEndpointId | ID of the created S3 VPC Endpoint |

**Imports used by this template**

- `Networking-PrivateRouteTable1Id`
- `Networking-PrivateRouteTable2Id`
- `Networking-PrivateRouteTable3Id`
- `Networking-PrivateRouteTable4Id`
- `Networking-PrivateRouteTable5Id`
- `Networking-PrivateRouteTable6Id`
- `Networking-VPCId`


#### Database Subnet Group

- **Template:** `cloudformation/1. Networking and Security Groups/3. Database Subnet Group.yaml`
- **Recommended stack name:** `DB-Subnet-Group`
- **Summary:** Creates the RDS Subnet Group from DB-tier subnets (private).

**Deploy (using the AWS Console)**

1. Sign in to the **AWS Management Console**.
2. Open **CloudFormation (Ireland)**: https://eu-west-1.console.aws.amazon.com/cloudformation/home?region=eu-west-1
3. Click **Create stack** and select **With new resources (standard)**.
4. Under **Prerequisite - Prepare template**, make sure **Template is ready** (choose an existing template) is selected.
5. Under **Specify template**, select **Upload a template file**.
6. Click **Choose file**.
7. Browse to and select the CloudFormation template **(.yaml)** from this repository.
8. Click **Next**, then enter a **Stack name**. If this README lists a **Recommended stack name** for the template, use it **exactly** as shown.
9. Ensure all required **Parameters** are filled out (defaults are provided where applicable).
10. Click **Next**, review, acknowledge any required capabilities (e.g., **IAM**), and choose **Create stack** to deploy.

**Parameters**

| Parameter | Type | Default | Allowed Values | Description |
| --- | --- | --- | --- | --- |
| NetworkingStackName | String | Networking |  | Name of the stack that created the networking infrastructure (used to import subnet IDs) |

**Outputs & export names**

| Output key | Export name | Description |
| --- | --- | --- |
| RDSSubnetGroup | ${AWS::StackName}-RDSSubnetGroupName | RDS Subnet Group Name |

**Imports used by this template**

- `!Sub "${NetworkingStackName}-PrivateSubnet5Id"`
- `!Sub "${NetworkingStackName}-PrivateSubnet6Id"`


#### Private Hosted Zone (Route 53)

- **Template:** `cloudformation/1. Networking and Security Groups/4. Private Hosted Zone.yaml`
- **Recommended stack name:** `Private-Hosted-Zone`
- **Summary:** Creates a Route 53 Private Hosted Zone associated to the VPC.

**Deploy (using the AWS Console)**

1. Sign in to the **AWS Management Console**.
2. Open **CloudFormation (Ireland)**: https://eu-west-1.console.aws.amazon.com/cloudformation/home?region=eu-west-1
3. Click **Create stack** and select **With new resources (standard)**.
4. Under **Prerequisite - Prepare template**, make sure **Template is ready** (choose an existing template) is selected.
5. Under **Specify template**, select **Upload a template file**.
6. Click **Choose file**.
7. Browse to and select the CloudFormation template **(.yaml)** from this repository.
8. Click **Next**, then enter a **Stack name**. If this README lists a **Recommended stack name** for the template, use it **exactly** as shown.
9. Ensure all required **Parameters** are filled out (defaults are provided where applicable).
10. Click **Next**, review, acknowledge any required capabilities (e.g., **IAM**), and choose **Create stack** to deploy.

**Parameters**

| Parameter | Type | Default | Allowed Values | Description |
| --- | --- | --- | --- | --- |
| DomainName | String | liverpool.com |  | The domain name for the private hosted zone |

**Outputs & export names**

| Output key | Export name | Description |
| --- | --- | --- |
| HostedZoneId | PrivateHostedZoneId | The ID of the created Private Hosted Zone |

**Imports used by this template**

- `Networking-VPCId`


#### Security Groups and Ports

- **Template:** `cloudformation/1. Networking and Security Groups/5. Security Groups and Ports.yaml`
- **Recommended stack name:** `SecurityGroup`
- **Summary:** Defines security groups for Bastion, ELB/NLB, Web, App, and RDS tiers.

**Deploy (using the AWS Console)**

1. Sign in to the **AWS Management Console**.
2. Open **CloudFormation (Ireland)**: https://eu-west-1.console.aws.amazon.com/cloudformation/home?region=eu-west-1
3. Click **Create stack** and select **With new resources (standard)**.
4. Under **Prerequisite - Prepare template**, make sure **Template is ready** (choose an existing template) is selected.
5. Under **Specify template**, select **Upload a template file**.
6. Click **Choose file**.
7. Browse to and select the CloudFormation template **(.yaml)** from this repository.
8. Click **Next**, then enter a **Stack name**. If this README lists a **Recommended stack name** for the template, use it **exactly** as shown.
9. Ensure all required **Parameters** are filled out (defaults are provided where applicable).
10. Click **Next**, review, acknowledge any required capabilities (e.g., **IAM**), and choose **Create stack** to deploy.

**Parameters**

| Parameter | Type | Default | Allowed Values | Description |
| --- | --- | --- | --- | --- |
| ELBPortHTTP | Number | 80 |  | HTTP port for ELB |
| ELBPortHTTPS | Number | 443 |  | HTTPS port for ELB |
| ELBSource | String | 0.0.0.0/0 |  | Source CIDR for ELB ingress |
| WebTierPortHTTP | Number | 80 |  | HTTP port for web tier |
| WebTierPortHTTPS | Number | 443 |  | HTTPS port for web tier |
| AppTierPortHTTP | Number | 80 |  | HTTP port for app tier |
| AppTierPortHTTPS | Number | 443 |  | HTTPS port for app tier |
| RDSPortMSSQL | Number | 1433 |  | Microsoft SQL Server port |
| RDSPortOracle | Number | 1521 |  | Oracle port |
| RDSPortMySQL | Number | 3306 |  | MySQL/MariaDB/Aurora MySQL port |
| RDSPortPostgreSQL | Number | 5432 |  | PostgreSQL/Aurora PostgreSQL port |
| RDSPortDB2 | Number | 50000 |  | IBM DB2 port |

**Outputs & export names**

| Output key | Export name | Description |
| --- | --- | --- |
| BastionSGId | SecurityGroup-BastionSGId | ID of the bastion security group |
| ELBSGId | SecurityGroup-ELBSGId | ID of the ELB security group |
| WebTierSGId | SecurityGroup-WebTierSGId | ID of the web tier security group |
| AppTierSGId | SecurityGroup-AppTierSGId | ID of the app tier security group |
| RDSSGId | SecurityGroup-RDSSGId | ID of the RDS security group |

**Imports used by this template**

- `Networking-VPCId`


---

### 2. Database Setup

#### RDS Aurora MySQL Cluster

- **Template:** `cloudformation/2. Database Setup/Aurora MySQL/1. RDS Aurora MySQL Cluster.yaml`
- **Recommended stack name:** `RDS-Aurora-MySQL`
- **Summary:** Creates Aurora MySQL cluster and instance with private DNS.

**Deploy (using the AWS Console)**

1. Sign in to the **AWS Management Console**.
2. Open **CloudFormation (Ireland)**: https://eu-west-1.console.aws.amazon.com/cloudformation/home?region=eu-west-1
3. Click **Create stack** and select **With new resources (standard)**.
4. Under **Prerequisite - Prepare template**, make sure **Template is ready** (choose an existing template) is selected.
5. Under **Specify template**, select **Upload a template file**.
6. Click **Choose file**.
7. Browse to and select the CloudFormation template **(.yaml)** from this repository.
8. Click **Next**, then enter a **Stack name**. If this README lists a **Recommended stack name** for the template, use it **exactly** as shown.
9. Ensure all required **Parameters** are filled out (defaults are provided where applicable).
10. Click **Next**, review, acknowledge any required capabilities (e.g., **IAM**), and choose **Create stack** to deploy.

**Parameters**

| Parameter | Type | Default | Allowed Values | Description |
| --- | --- | --- | --- | --- |
| HostedZoneDomainName | String | liverpool.com |  | Base domain for the private hosted zone |
| Region | String | eu-west-1 | eu-west-1, eu-central-1, us-east-1, us-east-2, us-west-1, us-west-2 | AWS Region for deployment |
| DBClusterIdentifier | String | liv-aurora-mysql-cluster |  | The name for the Aurora DB cluster |
| DBInstanceIdentifier | String | liv-aurora-mysql-instance |  | The name for the Aurora DB instance |
| DBInstanceClass | String | db.r6i.large | db.r6i.large, db.t3.medium, db.m6i.large, db.r6i.xlarge, db.m6i.xlarge | Aurora instance class |
| DBName | String | performance_db |  | Initial database name |
| DBUsername | String | adminuser |  | Master username |
| DBPassword | String | Password123! |  | Master user password |
| PreferredAvailabilityZone | String | eu-west-1a |  | Preferred Availability Zone for the Aurora instance |

**Outputs & export names**

| Output key | Export name | Description |
| --- | --- | --- |
| AuroraClusterEndpoint | Aurora-MySQL-ClusterEndpoint | The endpoint of the Aurora cluster |
| AuroraClusterId | Aurora-MySQL-ClusterId | The ID of the Aurora cluster |
| AuroraInstanceId | Aurora-MySQL-InstanceId | The ID of the Aurora instance |
| AuroraMySQLRecordName |  | DNS name for Aurora MySQL in Private Hosted Zone |
| ParameterStoreCredentialPath |  | SSM Parameter Store path for JSON credentials |

**Imports used by this template**

- `DB-Subnet-Group-RDSSubnetGroupName`
- `PrivateHostedZoneId`
- `SecurityGroup-RDSSGId`


#### RDS Aurora PostgreSQL Cluster

- **Template:** `cloudformation/2. Database Setup/Aurora PostgreSQL/1. RDS Aurora PostgreSQL Cluster.yaml`
- **Recommended stack name:** `RDS-Aurora-PostgreSQL`
- **Summary:** Creates Aurora PostgreSQL cluster and instance with private DNS.

**Deploy (using the AWS Console)**

1. Sign in to the **AWS Management Console**.
2. Open **CloudFormation (Ireland)**: https://eu-west-1.console.aws.amazon.com/cloudformation/home?region=eu-west-1
3. Click **Create stack** and select **With new resources (standard)**.
4. Under **Prerequisite - Prepare template**, make sure **Template is ready** (choose an existing template) is selected.
5. Under **Specify template**, select **Upload a template file**.
6. Click **Choose file**.
7. Browse to and select the CloudFormation template **(.yaml)** from this repository.
8. Click **Next**, then enter a **Stack name**. If this README lists a **Recommended stack name** for the template, use it **exactly** as shown.
9. Ensure all required **Parameters** are filled out (defaults are provided where applicable).
10. Click **Next**, review, acknowledge any required capabilities (e.g., **IAM**), and choose **Create stack** to deploy.

**Parameters**

| Parameter | Type | Default | Allowed Values | Description |
| --- | --- | --- | --- | --- |
| HostedZoneDomainName | String | liverpool.com |  | Base domain for the private hosted zone |
| Region | String | eu-west-1 | eu-west-1, eu-central-1, us-east-1, us-east-2, us-west-1, us-west-2 | AWS Region for deployment |
| DBClusterIdentifier | String | liv-aurora-postgres-cluster |  | The name for the Aurora DB cluster |
| DBInstanceIdentifier | String | liv-aurora-postgres-instance |  | The name for the Aurora DB instance |
| DBInstanceClass | String | db.r6i.large | db.r6i.large, db.t3.medium, db.m6i.large, db.r6i.xlarge, db.m6i.xlarge | Aurora instance class |
| DBName | String | performance_db |  | Initial database name |
| DBUsername | String | adminuser |  | Master username |
| DBPassword | String | Password123! |  | Master user password |
| PreferredAvailabilityZone | String | eu-west-1a |  | Preferred Availability Zone for the Aurora instance |

**Outputs & export names**

| Output key | Export name | Description |
| --- | --- | --- |
| AuroraClusterEndpoint | Aurora-PostgreSQL-ClusterEndpoint | The endpoint of the Aurora PostgreSQL cluster |
| AuroraClusterId | Aurora-PostgreSQL-ClusterId | The ID of the Aurora PostgreSQL cluster |
| AuroraInstanceId | Aurora-PostgreSQL-InstanceId | The ID of the Aurora PostgreSQL instance |
| AuroraPostgreSQLRecordName |  | DNS name for Aurora PostgreSQL in Private Hosted Zone |
| ParameterStoreCredentialPath |  | SSM Parameter Store path for JSON credentials |

**Imports used by this template**

- `DB-Subnet-Group-RDSSubnetGroupName`
- `PrivateHostedZoneId`
- `SecurityGroup-RDSSGId`


#### DynamoDB Table

- **Template:** `cloudformation/2. Database Setup/DynamoDB/1. DynamoDB Table.yaml`
- **Recommended stack name:** `DynamoDB-Table`
- **Summary:** Creates a DynamoDB table for transactions.

**Deploy (using the AWS Console)**

1. Sign in to the **AWS Management Console**.
2. Open **CloudFormation (Ireland)**: https://eu-west-1.console.aws.amazon.com/cloudformation/home?region=eu-west-1
3. Click **Create stack** and select **With new resources (standard)**.
4. Under **Prerequisite - Prepare template**, make sure **Template is ready** (choose an existing template) is selected.
5. Under **Specify template**, select **Upload a template file**.
6. Click **Choose file**.
7. Browse to and select the CloudFormation template **(.yaml)** from this repository.
8. Click **Next**, then enter a **Stack name**. If this README lists a **Recommended stack name** for the template, use it **exactly** as shown.
9. Ensure all required **Parameters** are filled out (defaults are provided where applicable).
10. Click **Next**, review, acknowledge any required capabilities (e.g., **IAM**), and choose **Create stack** to deploy.
 
**Parameters**

| Parameter | Type | Default | Allowed Values | Description |
| --- | --- | --- | --- | --- |
| Region | String | eu-west-1 | eu-west-1, eu-central-1, us-east-1, us-east-2, us-west-1, us-west-2 | AWS Region for deployment |
| HostedZoneDomainName | String | liverpool.com |  | Base domain for the private hosted zone |
| TableName | String | transaction_records |  | DynamoDB table name |

**Outputs & export names**

| Output key | Export name | Description |
| --- | --- | --- |
| DynamoDBTableName |  | Name of the DynamoDB table |
| ParameterStoreCredentialPath |  | SSM Parameter Store path for JSON credentials |


#### RDS IBM Db2 Standard Edition

- **Template:** `cloudformation/2. Database Setup/IBM DB2/1. RDS IBM DB2 SE.yaml`
- **Recommended stack name:** `RDS-IBM-DB2-SE`
- **Summary:** Creates IBM Db2 (SE) RDS instance with private DNS. Requires AWS Marketplace subscription.

**Deploy (using the AWS Console)**

1. Sign in to the **AWS Management Console**.
2. Open **CloudFormation (Ireland)**: https://eu-west-1.console.aws.amazon.com/cloudformation/home?region=eu-west-1
3. Click **Create stack** and select **With new resources (standard)**.
4. Under **Prerequisite - Prepare template**, make sure **Template is ready** (choose an existing template) is selected.
5. Under **Specify template**, select **Upload a template file**.
6. Click **Choose file**.
7. Browse to and select the CloudFormation template **(.yaml)** from this repository.
8. Click **Next**, then enter a **Stack name**. If this README lists a **Recommended stack name** for the template, use it **exactly** as shown.
9. Ensure all required **Parameters** are filled out (defaults are provided where applicable).
10. Click **Next**, review, acknowledge any required capabilities (e.g., **IAM**), and choose **Create stack** to deploy.

 
**Parameters**

| Parameter | Type | Default | Allowed Values | Description |
| --- | --- | --- | --- | --- |
| HostedZoneDomainName | String | liverpool.com |  | Base domain for the private hosted zone |
| Region | String | eu-west-1 | eu-west-1, eu-central-1, us-east-1, us-east-2, us-west-1, us-west-2 | AWS Region for deployment |
| DBInstanceIdentifier | String | liv-rds-DB2 |  | The name for the RDS DB instance |
| DBInstanceClass | String | db.r6i.large | db.r6i.large, db.m6i.large, db.r6i.xlarge, db.m6i.xlarge | RDS instance class |
| DBName | String | perf_db |  | Initial database name |
| DBUsername | String | adminuser |  | Master username |
| DBPassword | String | Password123! |  | Master user password |
| AllocatedStorage | Number | 20 |  | Allocated storage (GB) |
| PreferredAvailabilityZone | String | eu-west-1a |  | Preferred Availability Zone for the RDS instance |

**Outputs & export names**

| Output key | Export name | Description |
| --- | --- | --- |
| RDSInstanceEndpoint | RDS-IBMDB2-Endpoint | The endpoint address of the IBM DB2 RDS instance |
| RDSInstanceId | RDS-IBMDB2-InstanceId | The ID of the IBM DB2 RDS instance |
| IBMDB2RecordName |  | DNS name for IBM DB2 in Private Hosted Zone |
| ParameterStoreCredentialPath |  | SSM Parameter Store path for JSON credentials |

**Imports used by this template**

- `DB-Subnet-Group-RDSSubnetGroupName`
- `PrivateHostedZoneId`
- `SecurityGroup-RDSSGId`

#### RDS MariaDB Instance

- **Template:** `cloudformation/2. Database Setup/Maria DB/1. RDS MariaDB Instance.yaml`
- **Recommended stack name:** `RDS-MariaDB`
- **Summary:** Creates Amazon RDS for MariaDB with private DNS.

**Deploy (using the AWS Console)**

1. Sign in to the **AWS Management Console**.
2. Open **CloudFormation (Ireland)**: https://eu-west-1.console.aws.amazon.com/cloudformation/home?region=eu-west-1
3. Click **Create stack** and select **With new resources (standard)**.
4. Under **Prerequisite - Prepare template**, make sure **Template is ready** (choose an existing template) is selected.
5. Under **Specify template**, select **Upload a template file**.
6. Click **Choose file**.
7. Browse to and select the CloudFormation template **(.yaml)** from this repository.
8. Click **Next**, then enter a **Stack name**. If this README lists a **Recommended stack name** for the template, use it **exactly** as shown.
9. Ensure all required **Parameters** are filled out (defaults are provided where applicable).
10. Click **Next**, review, acknowledge any required capabilities (e.g., **IAM**), and choose **Create stack** to deploy.


**Parameters**

| Parameter | Type | Default | Allowed Values | Description |
| --- | --- | --- | --- | --- |
| HostedZoneDomainName | String | liverpool.com |  | Base domain for the private hosted zone |
| Region | String | eu-west-1 | eu-west-1, eu-central-1, us-east-1, us-east-2, us-west-1, us-west-2 | AWS Region for deployment |
| DBInstanceIdentifier | String | liv-rds-MariaDB |  | The name for the RDS DB instance |
| DBInstanceClass | String | db.r6i.large | db.r6i.large, db.t3.medium, db.m6i.large, db.r6i.xlarge, db.m6i.xlarge | RDS instance class |
| DBName | String | performance_db |  | Initial database name |
| DBUsername | String | adminuser |  | Master username |
| DBPassword | String | Password123! |  | Master user password |
| AllocatedStorage | Number | 20 |  | Allocated storage (GB) |
| PreferredAvailabilityZone | String | eu-west-1a |  | Preferred Availability Zone for the RDS instance |

**Outputs & export names**

| Output key | Export name | Description |
| --- | --- | --- |
| RDSInstanceEndpoint | RDS-MariaDB-Endpoint | The endpoint address of the MariaDB RDS instance |
| RDSInstanceId | RDS-MariaDB-InstanceId | The ID of the MariaDB RDS instance |
| MariaDBRecordName |  | DNS name for MariaDB in Private Hosted Zone |
| ParameterStoreCredentialPath |  | SSM Parameter Store path for JSON credentials |

**Imports used by this template**

- `DB-Subnet-Group-RDSSubnetGroupName`
- `PrivateHostedZoneId`
- `SecurityGroup-RDSSGId`


#### RDS Microsoft SQL Server SE Instance

- **Template:** `cloudformation/2. Database Setup/MS SQL Server/1. RDS MS SQL Server SE.yaml`
- **Recommended stack name:** `RDS-MSSQL-SE`
- **Summary:** Creates Amazon RDS for SQL Server (Standard Edition) with private DNS.

**Deploy (using the AWS Console)**

1. Sign in to the **AWS Management Console**.
2. Open **CloudFormation (Ireland)**: https://eu-west-1.console.aws.amazon.com/cloudformation/home?region=eu-west-1
3. Click **Create stack** and select **With new resources (standard)**.
4. Under **Prerequisite - Prepare template**, make sure **Template is ready** (choose an existing template) is selected.
5. Under **Specify template**, select **Upload a template file**.
6. Click **Choose file**.
7. Browse to and select the CloudFormation template **(.yaml)** from this repository.
8. Click **Next**, then enter a **Stack name**. If this README lists a **Recommended stack name** for the template, use it **exactly** as shown.
9. Ensure all required **Parameters** are filled out (defaults are provided where applicable).
10. Click **Next**, review, acknowledge any required capabilities (e.g., **IAM**), and choose **Create stack** to deploy.
 
**Parameters**

| Parameter | Type | Default | Allowed Values | Description |
| --- | --- | --- | --- | --- |
| HostedZoneDomainName | String | liverpool.com |  | Base domain for the private hosted zone |
| Region | String | eu-west-1 | eu-west-1, eu-central-1, us-east-1, us-east-2, us-west-1, us-west-2 | AWS Region for deployment |
| DBInstanceIdentifier | String | liv-rds-SQLServer |  | The name for the RDS DB instance |
| DBInstanceClass | String | db.r6i.large | db.r6i.large, db.m6i.large, db.r6i.xlarge, db.m6i.xlarge | RDS instance class |
| DBName | String | performance_db |  | Initial database name |
| DBEdition | String | Standard | Standard | SQL Server Edition |
| DBUsername | String | adminuser |  | Master username |
| DBPassword | String | Password123! |  | Master user password |
| AllocatedStorage | Number | 20 |  | Allocated storage (GB) |
| PreferredAvailabilityZone | String | eu-west-1a |  | Preferred Availability Zone for the RDS instance |

**Outputs & export names**

| Output key | Export name | Description |
| --- | --- | --- |
| RDSInstanceEndpoint | RDS-SQLServer-Endpoint | The endpoint address of the SQL Server RDS instance |
| RDSInstanceId | RDS-SQLServer-InstanceId | The ID of the SQL Server RDS instance |
| SQLServerRecordName |  | DNS name for SQL Server in Private Hosted Zone |
| ParameterStoreCredentialPath |  | SSM Parameter Store path for JSON credentials |

**Imports used by this template**

- `DB-Subnet-Group-RDSSubnetGroupName`
- `PrivateHostedZoneId`
- `SecurityGroup-RDSSGId`


#### RDS MySQL Instance

- **Template:** `cloudformation/2. Database Setup/MySQL/1. RDS MySQL Instance.yaml`
- **Recommended stack name:** `RDS-MySQL`
- **Summary:** Creates Amazon RDS for MySQL with private DNS.

**Deploy (using the AWS Console)**

1. Sign in to the **AWS Management Console**.
2. Open **CloudFormation (Ireland)**: https://eu-west-1.console.aws.amazon.com/cloudformation/home?region=eu-west-1
3. Click **Create stack** and select **With new resources (standard)**.
4. Under **Prerequisite - Prepare template**, make sure **Template is ready** (choose an existing template) is selected.
5. Under **Specify template**, select **Upload a template file**.
6. Click **Choose file**.
7. Browse to and select the CloudFormation template **(.yaml)** from this repository.
8. Click **Next**, then enter a **Stack name**. If this README lists a **Recommended stack name** for the template, use it **exactly** as shown.
9. Ensure all required **Parameters** are filled out (defaults are provided where applicable).
10. Click **Next**, review, acknowledge any required capabilities (e.g., **IAM**), and choose **Create stack** to deploy.

**Parameters**

| Parameter | Type | Default | Allowed Values | Description |
| --- | --- | --- | --- | --- |
| HostedZoneDomainName | String | liverpool.com |  | Base domain for the private hosted zone |
| Region | String | eu-west-1 | eu-west-1, eu-central-1, us-east-1, us-east-2, us-west-1, us-west-2 | AWS Region for deployment |
| DBInstanceIdentifier | String | liv-rds-MySQL |  | The name for the RDS DB instance |
| DBInstanceClass | String | db.r6i.large | db.r6i.large, db.t3.medium, db.m6i.large, db.r6i.xlarge, db.m6i.xlarge | RDS instance class |
| DBName | String | performance_db |  | Initial database name |
| DBUsername | String | adminuser |  | Master username |
| DBPassword | String | Password123! |  | Master user password |
| AllocatedStorage | Number | 20 |  | Allocated storage (GB) |
| PreferredAvailabilityZone | String | eu-west-1a |  | Preferred Availability Zone for the RDS instance |

**Outputs & export names**

| Output key | Export name | Description |
| --- | --- | --- |
| RDSInstanceEndpoint | RDS-MySQL-Endpoint | The endpoint address of the RDS instance |
| RDSInstanceId | RDS-MySQL-InstanceId | The ID of the RDS instance |
| MySQLRecordName |  | DNS name for MySQL in Private Hosted Zone |
| ParameterStoreCredentialPath |  | SSM Parameter Store path for JSON credentials |

**Imports used by this template**

- `DB-Subnet-Group-RDSSubnetGroupName`
- `PrivateHostedZoneId`
- `SecurityGroup-RDSSGId`



#### RDS Oracle Standard Edition Instance

- **Template:** `cloudformation/2. Database Setup/Oracle DB/1. RDS Oracle SE.yaml`
- **Recommended stack name:** `RDS-Oracle-SE`
- **Summary:** Creates Amazon RDS for Oracle (SE) with private DNS.

**Deploy (using the AWS Console)**

1. Sign in to the **AWS Management Console**.
2. Open **CloudFormation (Ireland)**: https://eu-west-1.console.aws.amazon.com/cloudformation/home?region=eu-west-1
3. Click **Create stack** and select **With new resources (standard)**.
4. Under **Prerequisite - Prepare template**, make sure **Template is ready** (choose an existing template) is selected.
5. Under **Specify template**, select **Upload a template file**.
6. Click **Choose file**.
7. Browse to and select the CloudFormation template **(.yaml)** from this repository.
8. Click **Next**, then enter a **Stack name**. If this README lists a **Recommended stack name** for the template, use it **exactly** as shown.
9. Ensure all required **Parameters** are filled out (defaults are provided where applicable).
10. Click **Next**, review, acknowledge any required capabilities (e.g., **IAM**), and choose **Create stack** to deploy.

**Parameters**

| Parameter | Type | Default | Allowed Values | Description |
| --- | --- | --- | --- | --- |
| HostedZoneDomainName | String | liverpool.com |  | Base domain for the private hosted zone |
| Region | String | eu-west-1 | eu-west-1, eu-central-1, us-east-1, us-east-2, us-west-1, us-west-2 | AWS Region for deployment |
| DBInstanceIdentifier | String | liv-rds-Oracle |  | The name for the RDS DB instance |
| DBInstanceClass | String | db.r6i.large | db.r6i.large, db.m6i.large, db.r6i.xlarge, db.m6i.xlarge | RDS instance class |
| DBName | String | ORCL |  | Initial database name |
| DBUsername | String | adminuser |  | Master username |
| DBPassword | String | Password123! |  | Master user password |
| AllocatedStorage | Number | 20 |  | Allocated storage (GB) |
| PreferredAvailabilityZone | String | eu-west-1a |  | Preferred Availability Zone for the RDS instance |

**Outputs & export names**

| Output key | Export name | Description |
| --- | --- | --- |
| RDSInstanceEndpoint | RDS-Oracle-Endpoint | The endpoint address of the Oracle RDS instance |
| RDSInstanceId | RDS-Oracle-InstanceId | The ID of the Oracle RDS instance |
| OracleRecordName |  | DNS name for Oracle in Private Hosted Zone |
| ParameterStoreCredentialPath |  | SSM Parameter Store path for JSON credentials |

**Imports used by this template**

- `DB-Subnet-Group-RDSSubnetGroupName`
- `PrivateHostedZoneId`
- `SecurityGroup-RDSSGId`


#### RDS PostgreSQL Instance

- **Template:** `cloudformation/2. Database Setup/PostgreSQL/1. RDS PostgreSQL Instance.yaml`
- **Recommended stack name:** `RDS-PostgreSQL`
- **Summary:** Creates Amazon RDS for PostgreSQL with private DNS.

**Deploy (using the AWS Console)**

1. Sign in to the **AWS Management Console**.
2. Open **CloudFormation (Ireland)**: https://eu-west-1.console.aws.amazon.com/cloudformation/home?region=eu-west-1
3. Click **Create stack** and select **With new resources (standard)**.
4. Under **Prerequisite - Prepare template**, make sure **Template is ready** (choose an existing template) is selected.
5. Under **Specify template**, select **Upload a template file**.
6. Click **Choose file**.
7. Browse to and select the CloudFormation template **(.yaml)** from this repository.
8. Click **Next**, then enter a **Stack name**. If this README lists a **Recommended stack name** for the template, use it **exactly** as shown.
9. Ensure all required **Parameters** are filled out (defaults are provided where applicable).
10. Click **Next**, review, acknowledge any required capabilities (e.g., **IAM**), and choose **Create stack** to deploy.

**Parameters**

| Parameter | Type | Default | Allowed Values | Description |
| --- | --- | --- | --- | --- |
| HostedZoneDomainName | String | liverpool.com |  | Base domain for the private hosted zone |
| Region | String | eu-west-1 | eu-west-1, eu-central-1, us-east-1, us-east-2, us-west-1, us-west-2 | AWS Region for deployment |
| DBInstanceIdentifier | String | liv-rds-PostgreSQLa |  | The name for the RDS DB instance |
| DBInstanceClass | String | db.r6i.large | db.r6i.large, db.t3.medium, db.m6i.large, db.r6i.xlarge, db.m6i.xlarge | RDS instance class |
| DBName | String | performance_db |  | Initial database name |
| DBUsername | String | adminuser |  | Master username |
| DBPassword | String | Password123! |  | Master user password |
| AllocatedStorage | Number | 20 |  | Allocated storage (GB) |
| PreferredAvailabilityZone | String | eu-west-1a |  | Preferred Availability Zone for the RDS instance |

**Outputs & export names**

| Output key | Export name | Description |
| --- | --- | --- |
| RDSInstanceEndpoint | RDS-PostgreSQL-Endpoint | The endpoint address of the PostgreSQL RDS instance |
| RDSInstanceId | RDS-PostgreSQL-InstanceId | The ID of the PostgreSQL RDS instance |
| PostgreSQLRecordName |  | DNS name for PostgreSQL in Private Hosted Zone |
| ParameterStoreCredentialPath |  | SSM Parameter Store path for JSON credentials |

**Imports used by this template**

- `DB-Subnet-Group-RDSSubnetGroupName`
- `PrivateHostedZoneId`
- `SecurityGroup-RDSSGId`



---

### 3. API Layer

#### NLB, Target Group, API EC2 (ASG)

- **Template:** `cloudformation/3. API/1. NLB, Target Group, API EC2.yaml`
- **Recommended stack name:** `API`
- **Summary:** Creates NLB, Target Group, Launch Template + Auto Scaling Group, and private DNS record.

**Deploy (using the AWS Console)**

1. Sign in to the **AWS Management Console**.
2. Open **CloudFormation (Ireland)**: https://eu-west-1.console.aws.amazon.com/cloudformation/home?region=eu-west-1
3. Click **Create stack** and select **With new resources (standard)**.
4. Under **Prerequisite - Prepare template**, make sure **Template is ready** (choose an existing template) is selected.
5. Under **Specify template**, select **Upload a template file**.
6. Click **Choose file**.
7. Browse to and select the CloudFormation template **(.yaml)** from this repository.
8. Click **Next**, then enter a **Stack name**. If this README lists a **Recommended stack name** for the template, use it **exactly** as shown.
9. Ensure all required **Parameters** are filled out (defaults are provided where applicable).
10. Click **Next**, review, acknowledge any required capabilities (e.g., **IAM**), and choose **Create stack** to deploy.

**Parameters**

| Parameter | Type | Default | Allowed Values | Description |
| --- | --- | --- | --- | --- |
| NamePrefix | String | API |  | Prefix for naming resources |
| NLBScheme | String | internet-facing | internet-facing, internal | NLB Scheme (internet-facing or internal) |
| HostedZoneDomainName | String | liverpool.com |  | Base domain for the private hosted zone |
| EC2InstanceType | String | m6i.xlarge | t3.medium, t3.large, t3.xlarge, t3.2xlarge, m6i.large, m6i.xlarge, m6i.2xlarge, m6i.4xlarge | EC2 Instance type |
| EC2AmiId | AWS::EC2::Image::Id | ami-0fab1b527ffa9b942 |  | AMI ID for EC2 instances |
| TargetGroupPort | Number | 80 |  | Port for Target Group registration |
| HealthCheckPath | String | / |  | Retained for compatibility but unused in NLB TCP health checks |
| EC2VolumeSize | Number | 40 |  | EC2 root EBS volume size (GB) |
| MinSize | Number | 10 |  | Minimum number of EC2 instances in Auto Scaling Group |
| MaxSize | Number | 10 |  | Maximum number of EC2 instances in Auto Scaling Group |
| DesiredCapacity | Number | 10 |  | Desired number of EC2 instances in Auto Scaling Group |
| ScaleCpuThreshold | Number | 80 |  | Target average CPU utilization (%) to trigger scale-out/in |

**Outputs & export names**

| Output key | Export name | Description |
| --- | --- | --- |
| NLBDNSName | api-app-nlb-dnsname | DNS name of the Network Load Balancer |
| TargetGroupArn | api-app-targetgroup-arn | ARN of the Target Group |
| LaunchTemplateId | api-app-tier-launchtemplateid | ID of the Launch Template |
| AutoScalingGroupName | api-app-tier-autoscalinggroupname | Name of the Auto Scaling Group |
| NLBRecordName |  | DNS name in Private Hosted Zone |

**Imports used by this template**

- `Networking-PrivateSubnet3Id`
- `Networking-PrivateSubnet4Id`
- `Networking-PublicSubnet3Id`
- `Networking-PublicSubnet4Id`
- `Networking-VPCId`
- `PrivateHostedZoneId`
- `SecurityGroup-AppTierSGId`
- `SecurityGroup-ELBSGId`


---

### 4. CI/CD Pipeline

#### CI/CD Pipeline (CodePipeline, CodeBuild, CodeDeploy)

- **Template:** `cloudformation/4. CICD Pipeline/1. CICD Pipeline.yaml`
- **Recommended stack name:** `cicd`
- **Summary:** Builds and deploys API to EC2 via CodeDeploy using tag-based targeting.
- **Pre-Requisite:** Navigate to CodePipeline (Ireland) and create a connection to the GitHub Code Repository. Keep the ARN ready for deployment
**Deploy (using the AWS Console)**

1. Sign in to the **AWS Management Console**.
2. Open **CloudFormation (Ireland)**: https://eu-west-1.console.aws.amazon.com/cloudformation/home?region=eu-west-1
3. Click **Create stack** and select **With new resources (standard)**.
4. Under **Prerequisite - Prepare template**, make sure **Template is ready** (choose an existing template) is selected.
5. Under **Specify template**, select **Upload a template file**.
6. Click **Choose file**.
7. Browse to and select the CloudFormation template **(.yaml)** from this repository.
8. Click **Next**, then enter a **Stack name**. If this README lists a **Recommended stack name** for the template, use it **exactly** as shown.
9. Ensure all required **Parameters** are filled out (defaults are provided where applicable).
10. Click **Next**, review, acknowledge any required capabilities (e.g., **IAM**), and choose **Create stack** to deploy.

**Parameters**

| Parameter | Type | Default | Allowed Values | Description |
| --- | --- | --- | --- | --- |
| AppName | String | apiservice |  | Name of the application (used for naming resources, must be lowercase) |
| GitHubOwner | String | {PASTE / INSERT GITHUB OWNER}} |  | GitHub user or organization owning the repository (public) |
| GitHubRepo | String | AWSDatabasePerformance |  | GitHub repository name (public) |
| GitHubBranch | String | main |  | Branch to watch for changes |
| GitHubConnectionArn | String | | {PASTE/ INSERT ARN HERE} | ARN of the AWS CodeStar Connection to GitHub (must be in AVAILABLE state) |
| EC2TagKey | String | CodeDeployRole |  | EC2 instance tag key to target |
| EC2TagValue | String | AppServer |  | EC2 instance tag value to target |

**Outputs & export names**

| Output key | Export name | Description |
| --- | --- | --- |
| PipelineName | apiservice-pipeline-name | Name of the CodePipeline |
| CodeDeployApplicationName | apiservice-codedeploy-application-name | Name of the CodeDeploy Application |
| DeploymentGroupName | apiservice-deployment-group-name | Name of the CodeDeploy Deployment Group |
| ArtifactBucketName | apiservice-artifact-bucket-name | S3 bucket used for storing pipeline artifacts |


---

## Post-Deployment: Apache JMeter

You can run the performance tests locally (Windows) or from a dedicated EC2 host.

### Option A — Run on Windows (local)
- Test plans: `performance_tests\jmeter\test plans`
- **Run all tests:** `performance_tests\jmeter\batch files\1_RUN ALL Tests.bat`
- **Open all reports:** `performance_tests\jmeter\batch files\2_OPEN ALL Reports.bat`
- Reports & artifacts: `performance_tests\jmeter\results\<engine>\*`

### Option B — Run on an EC2 host (recommended for consistency)
1. **Launch EC2** in the existing VPC:
   - Name: **Apache JMeter**
   - Instance type: **m6i.xlarge**
   - Key pair: create or select an existing key
   - VPC: **liverpool-vpc** (from the `Networking` stack)
   - Subnet: **liverpool-public-nat-AZ-a**
   - Auto‑assign public IP: **Enabled**
   - Security Group: **SecurigtyGroup-SGBastion-xxxxx** (from the SecurityGroup stack)
   - Storage: **100 GB gp3**
2. **Install Java (8+)** and **Apache JMeter 5.6.3**:
   - Download JDK 8+ from your preferred distribution.
   - Download JMeter 5.6.3: https://dlcdn.apache.org/jmeter/binaries/apache-jmeter-5.6.3.zip
   - Extract the zip and run from the `bin/` folder:
     ```bash
     ./jmeter.bat   # on Windows
     ./jmeter       # on Linux/macOS
     ```
3. **Pull test plans** from this repo onto the host and execute the batch files as in Option A.

## Operations & Troubleshooting

### CodeDeploy agent (if the API EC2 is not getting new builds)
```bash
sudo yum update -y
sudo yum install -y ruby wget
cd /home/ec2-user
wget https://aws-codedeploy-eu-west-1.s3.eu-west-1.amazonaws.com/latest/install
chmod +x ./install
sudo ./install auto
sudo systemctl enable codedeploy-agent
sudo systemctl start codedeploy-agent
```

### Manually run the API service (sanity check via SSH to EC2)
```bash
source /home/ec2-user/app/venv/bin/activate
cd /home/ec2-user/app
uvicorn api_service.main:app --host 127.0.0.1 --port 8000
```
**Verify/stop the process**
```bash
ps aux | grep uvicorn
sudo netstat -tulnp | grep 8000
sudo kill <PID>
```

## Notes & Quotas

- **Deployments & code updates:** EC2 instances are managed by an **Auto Scaling Group** (self‑healing). **Code updates** are delivered by the **CI/CD pipeline** (CodeDeploy) and are **not** fetched automatically unless a deployment is triggered.
- **Quotas:** New accounts often have **16 vCPU** regional limits; request an increase to **64 vCPU** for planned testing.
- **Cross‑stack dependencies:**
  - `Networking` → exports `${AWS::StackName}-*` (e.g., `Networking-VPCId`, `Networking-PrivateSubnet3Id`).
  - `DB-Subnet-Group` → exports `${AWS::StackName}-RDSSubnetGroupName` (imported as `DB-Subnet-Group-RDSSubnetGroupName`).
  - `Private-Hosted-Zone` → exports `PrivateHostedZoneId`.
  - `SecurityGroup` → exports fixed names like `SecurityGroup-ELBSGId`, `SecurityGroup-RDSSGId`.