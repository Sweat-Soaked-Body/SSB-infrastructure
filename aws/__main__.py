import pulumi_aws as aws

vpc = aws.ec2.get_vpc(default=True)

instance = aws.ec2.Instance(
    'ssb',
    ami='ami-040c33c6a51fd5d96',
    instance_type='t2.micro',
    associate_public_ip_address=True,
    tags={
        'Name': 'ssb',
    }
)

rds_security_group = aws.ec2.SecurityGroup(
    'rds-sg',
    vpc_id=vpc.id,
    ingress=[
        aws.ec2.SecurityGroupIngressArgs(
            from_port=5432,
            to_port=5432,
            protocol='tcp',
            cidr_blocks=['0.0.0.0/0'],
        ),
    ],
    egress=[
        aws.ec2.SecurityGroupEgressArgs(
            from_port=0,
            to_port=0,
            protocol='-1',
            cidr_blocks=['0.0.0.0/0'],
        ),
    ],
)

rds = aws.rds.Instance(
    'ssb',
    instance_class='db.t4g.micro',
    engine='postgres',
    engine_version='16.3',
    allocated_storage=20,
    db_name='ssb',
    username='ssb',
    password='ssbssbssbssb',
    skip_final_snapshot=True,
    publicly_accessible=True,
    vpc_security_group_ids=[rds_security_group.id],
    tags={
        'Name': 'ssb-rds',
    }
)