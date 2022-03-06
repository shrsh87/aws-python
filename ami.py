import pulumi
import pulumi_aws as aws


ami = aws.ec2.get_ami(
    filters = [
        aws.ec2.GetAmiFilterArgs(
            name="name",
            values=["amzn2*"],
        )
    ],
    most_recent=True,
    owners=["amazon"])

pulumi.export("ami", ami)