BUCKET_NAMING_MSG = """
* Bucket names must be unique across all existing bucket names in Amazon S3.
* Bucket names must comply with DNS naming conventions.
* Bucket names must be at least 3 and no more than 63 characters long.
* Bucket names must not contain uppercase characters or underscores.
* Bucket names must start with a lowercase letter or number.
* Bucket names must be a series of one or more labels. Adjacent labels are separated
by a single period (.). Bucket names can contain lowercase letters, numbers, and
hyphens. Each label must start and end with a lowercase letter or a number.
* Bucket names must not be formatted as an IP address (for example, 192.168.5.4).
* When you use virtual hosted–style buckets with Secure Sockets Layer (SSL), the SSL
wildcard certificate only matches buckets that don't contain periods. To work around
this, use HTTP or write your own certificate verification logic. We recommend that
you do not use periods (".") in bucket names when using virtual hosted–style buckets.
"""

# https://github.com/Miserlou/Zappa/issues/1688
def is_valid_bucket_name(name):
    """
    Checks if an S3 bucket name is valid according to https://docs.aws.amazon.com/AmazonS3/latest/dev/BucketRestrictions.html#bucketnamingrules
    """
    # Bucket names must be at least 3 and no more than 63 characters long.
    if len(name) < 3 or len(name) > 63:
        return False
    # Bucket names must not contain uppercase characters or underscores.
    if any(x.isupper() for x in name):
        return False
    if "_" in name:
        return False
    # Bucket names must start with a lowercase letter or number.
    if not (name[0].islower() or name[0].isdigit()):
        return False
    # Bucket names must be a series of one or more labels. Adjacent labels are separated by a single period (.).
    for label in name.split("."):
        # Each label must start and end with a lowercase letter or a number.
        if len(label) < 1:
            return False
        if not (label[0].islower() or label[0].isdigit()):
            return False
        if not (label[-1].islower() or label[-1].isdigit()):
            return False
    # Bucket names must not be formatted as an IP address (for example, 192.168.5.4).
    looks_like_IP = True
    for label in name.split("."):
        if not label.isdigit():
            looks_like_IP = False
            break
    if looks_like_IP:
        return False

    return True

