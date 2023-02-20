# Basic CloudFormation Templates
Been learning about CloudFormation Templates recently.

Here's a basic template that creates an EC2 instance in the default VPC.
I'm working on learning more so that I can have a template that creates EC2 instances in a dedicated VPC.
I also want to learn more about AWS SSM.

This was pieced together using samples in [https://github.com/awslabs/aws-cloudformation-templates](https://github.com/awslabs/aws-cloudformation-templates).
Especially [https://github.com/awslabs/aws-cloudformation-templates/blob/master/aws/services/EC2/EC2InstanceWithSecurityGroupSample.yaml](https://github.com/awslabs/aws-cloudformation-templates/blob/master/aws/services/EC2/EC2InstanceWithSecurityGroupSample.yaml).

```yaml
AWSTemplateFormatVersion: "2010-09-09"
Metadata:
  License: Apache-2.0
Description:
  "AWS CloudFormation Sample Template EC2InstanceWithSecurityGroupSample:
  Create an Amazon EC2 instance running the Amazon Linux AMI. The AMI is chosen based
  on the region in which the stack is run. This example creates an EC2 security group
  for the instance to give you SSH access. **WARNING** This template creates an Amazon
  EC2 instance. You will be billed for the AWS resources used if you create a stack
  from this template."
Parameters:
  InstanceName:
    Description: Name of the EC2 Instance
    Type: String
  KeyName:
    Description: Name of an existing EC2 KeyPair to enable SSH access to the instance
    Type: AWS::EC2::KeyPair::KeyName
    ConstraintDescription: must be the name of an existing EC2 KeyPair.
  InstanceType:
    Description: WebServer EC2 instance type
    Type: String
    Default: t3.small
    AllowedValues:
      [
        t2.nano,
        t2.micro,
        t2.small,
        t2.medium,
        t2.large,
        t2.xlarge,
        t2.2xlarge,
        t3.nano,
        t3.micro,
        t3.small,
        t3.medium,
        t3.large,
        t3.xlarge,
        t3.2xlarge,
        m4.large,
        m4.xlarge,
        m4.2xlarge,
        m4.4xlarge,
        m4.10xlarge,
        m5.large,
        m5.xlarge,
        m5.2xlarge,
        m5.4xlarge,
        c5.large,
        c5.xlarge,
        c5.2xlarge,
        c5.4xlarge,
        c5.9xlarge,
        g3.8xlarge,
        r5.large,
        r5.xlarge,
        r5.2xlarge,
        r5.4xlarge,
        r3.12xlarge,
        i3.xlarge,
        i3.2xlarge,
        i3.4xlarge,
        i3.8xlarge,
        d2.xlarge,
        d2.2xlarge,
        d2.4xlarge,
        d2.8xlarge,
      ]
    ConstraintDescription: must be a valid EC2 instance type.
  SSHLocation:
    Description: The IP address range that can be used to SSH to the EC2 instances
    Type: String
    MinLength: 9
    MaxLength: 18
    Default: 0.0.0.0/0
    AllowedPattern: (\d{1,3})\.(\d{1,3})\.(\d{1,3})\.(\d{1,3})/(\d{1,2})
    ConstraintDescription: must be a valid IP CIDR range of the form x.x.x.x/x.
Resources:
  EC2Instance:
    Type: AWS::EC2::Instance
    Properties:
      InstanceType: !Ref "InstanceType"
      SecurityGroups: [!Ref "InstanceSecurityGroup"]
      KeyName: !Ref "KeyName"
      ImageId: !FindInMap
        - awsRegionMap
        - !Ref "AWS::Region"
        - ami
      Tags:
        - Key: Name
          Value: !Ref "InstanceName"
  InstanceSecurityGroup:
    Type: AWS::EC2::SecurityGroup
    Properties:
      GroupDescription: EC2 Instance Security group for ports 22, 80, 443
      SecurityGroupIngress:
        - IpProtocol: tcp
          FromPort: 22
          ToPort: 22
          CidrIp: !Ref "SSHLocation"
        - CidrIp: 0.0.0.0/0
          Description: Allow http access
          FromPort: "80"
          IpProtocol: tcp
          ToPort: "80"
        - CidrIp: 0.0.0.0/0
          Description: Allow https access
          FromPort: "443"
          IpProtocol: tcp
          ToPort: "443"
  IPAddress:
    Type: AWS::EC2::EIP
  IPAssoc:
    Type: AWS::EC2::EIPAssociation
    Properties:
      InstanceId: !Ref "EC2Instance"
      EIP: !Ref "IPAddress"

Outputs:
  InstanceId:
    Description: InstanceId of the newly created EC2 instance
    Value: !Ref "EC2Instance"
  AZ:
    Description: Availability Zone of the newly created EC2 instance
    Value: !GetAtt [EC2Instance, AvailabilityZone]
  PublicDNS:
    Description: Public DNSName of the newly created EC2 instance
    Value: !GetAtt [EC2Instance, PublicDnsName]
  PublicIP:
    Description: Public IP address of the newly created EC2 instance
    Value: !GetAtt [EC2Instance, PublicIp]
  InstanceIPAddress:
    Description: IP address of the newly created EC2 instance
    Value: !Ref "IPAddress"

Mappings:
  awsRegionMap:
    us-east-1:
      ami: ami-08c40ec9ead489470
    us-east-2:
      ami: ami-02f3416038bdb17fb
```