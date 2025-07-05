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


	Troubleshooting

Manual Install (with EC2 - Key Pair)
sudo yum update -y
sudo yum install -y ruby wget
cd /home/ec2-user
wget https://aws-codedeploy-eu-west-1.s3.eu-west-1.amazonaws.com/latest/install
chmod +x ./install
sudo ./install auto
sudo systemctl enable codedeploy-agent
sudo systemctl start codedeploy-agent
 

  
   


1. source /home/ec2-user/app/venv/bin/activate
cd /home/ec2-user/app
uvicorn api_service.main:app --host 127.0.0.1 --port 8000

CHECK if service running

ps aux | grep uvicorn 



NOTES:
DynamoDB does not support float and using Decimal instead for unit_price and total_amount
Auto Scaling is not enabled for Self healing, and will not pull the latest code.  Pipeline has to be run to ge the code on teh isntance
AWS Quota limit has to be increased on EC2 for the number for vCPUs in new accounts. Default is 16 vCPU and needs to be increased to 64 vCPU


For IBM
https://cloud.ibm.com/registration?target=/db2-wh&uucid=0d24d74b852ef96a&utm_content=DABWW
Select the AWS option, choose the starting configuration, then apply the promo code DB2W1K to receive USD 1,000 of free credits to use toward the service.

Apache JMeter - EC2
1. Launch EC2 instance and use existing networking components
	a Name: Apache JMeter
	a Instane Type: m6i.xlarge
	a Create a new EC2 Key Pair 
	a VPC: liverpool-vpc
    a Subnet: liverpool-public-nat-AZ-a
1. a Auto-Assign public IP: Enable
1. Security Group: SecurigtyGroup-SGBastion-xxxxx
1. Storage: 100 GB gp3

Apache JMeter - Setup
- Ensure Java 8+ is installed: https://javadl.oracle.com/webapps/download/AutoDL?xd_co_f=YzVhYzVlYjUtOTQ5Ni00NzI5LWI3ODAtZmRiYzJkY2Y2MThl&BundleId=252044_8a1589aa0fe24566b4337beee47c2d29
- Download https://dlcdn.apache.org//jmeter/binaries/apache-jmeter-5.6.3.zip
- Extact the .zip file
- navigate to the bin folder and run jmeter.bat