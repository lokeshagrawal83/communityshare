import tinys3

from community_share import config


def save_file_to_s3(src_filename, dst_filename):
    conn = tinys3.Connection(config.S3_USERNAME, config.S3_KEY, tls=True)

    conn.upload(
        dst_filename,
        src_filename,
        config.S3_BUCKETNAME,
        expires=3600  # cache-expiry = 1 hour
    )
