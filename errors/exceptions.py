class ImageRecoError(Exception):
    pass


class ItemNotFoundError(ImageRecoError):
    pass


class ItemExistsError(ImageRecoError):
    pass