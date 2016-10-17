class BadRequest(Exception):
    pass


class FileTypeNotImplemented(BadRequest):
    pass


class FileTypeNotPermitted(BadRequest):
    pass
