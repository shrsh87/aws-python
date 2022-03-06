"""An AWS Python Pulumi program"""

import json
import pulumi
import pulumi_aws as aws


"""
Demo 1: Create s3 one bucket.
"""

# # Create an AWS resource (S3 Bucket)
# bucket = s3.Bucket('my-bucket')


"""
Demo 2: Create s3 three buckets.
"""
# buckets = []
# for i in range(3):
#     bucket = aws.s3.Bucket(f"my-bucket-{i}")
#     buckets.append(bucket.id)

# # Export the name of the bucket
# pulumi.export('bucket_name', buckets)

"""
Demo 3: Create a bucket and expose a website index document
"""

# Create a bucket and expose a website index document
site_bucket = aws.s3.Bucket("s3-website-bucket", website=aws.s3.BucketWebsiteArgs(index_document="index.html"))
index_content = """
<html>
    <head><title>Hello S3</title><meta charset="UTF-8"></head>
    <body>
        <p>Hello, world!</p>
        <p>Made with love with <a href="https://pulumi.com">Pulumi</a></p>
    </body>
</html>
"""

# Write our index.html into the site bucket
aws.s3.BucketObject("index",
                bucket=site_bucket.id,  # reference to the s3.Bucket object
                content=index_content,
                key="index.html",  # set the key of the object
                content_type="text/html; charset=utf-8")  # set the MIME type of the file

# Set the access policy for the bucket so all objects are readable
aws.s3.BucketPolicy("bucket-policy", bucket=site_bucket.id, policy=site_bucket.id.apply(lambda id: json.dumps({
    "Version": "2012-10-17",
    "Statement": {
        "Effect": "Allow",
        "Principal": "*",
        "Action": ["s3:GetObject"],
        # Policy refers to bucket explicitly
        "Resource": [f"arn:aws:s3:::{id}/*"]
    },
})))

# Export the website URL
pulumi.export("website_url", site_bucket.website_endpoint)