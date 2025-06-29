# AWS Database Performance
Theodor Harmse - University of Liverpool - Infrastructure as Code: Database Performance Project

Setup:
1. Install Visual Studio Community Edition
1. Install the AWS CLI https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html
1. Run AWS Configure and specify the region as eu-west-1 and supply the access key and secret key (only for validations in visual studio)
1. Run pip install cfn-lint


Deployments
1. Networking.yaml  (Stack Name:  Networking)

2. Database Subnet Group.yaml  (Stack name: DB-Subnet-Group)

3. Security Groups and Ports.yaml (Stack name: SecurityGroups)

4. RDS MySQL Instance

When doing IBM, activate Marketplace Pay-as-you-use license first


5. ALB

6. CICD Pipeline  
   a  Create clone of Public repo
   b. Create GitHub connection in AWS (ireland region)
   c. Create Cloudformation stack with lowercase name ONLY ie. cicd 
	a 