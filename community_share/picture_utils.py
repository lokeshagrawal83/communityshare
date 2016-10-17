import hashlib
import imghdr

from community_share.s3_connection import save_file_to_s3

allowable_types = ['gif', 'jpeg', 'png']


def get_image_type(image_data):
    return imghdr.what('ignored', h=image_data)


def image_to_user_filename(image_data, user_id):
    image_type = get_image_type(image_data)

    return 'user_{0:d}_{1}.{2}'.format(
        user_id,
        hashlib.sha1(image_data).hexdigest(),
        image_type if image_type is not 'jpeg' else 'jpg',
    )


def is_allowable_image(image_data):
    # _not_ extensions, but types from imghdr
    # if unrecognized, type will be None
    return get_image_type(image_data) in allowable_types


def store_image(src_filename, dst_filename):
    try:
        save_file_to_s3(src_filename, dst_filename)
    except:
        return
