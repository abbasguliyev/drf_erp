from django.core.exceptions import ValidationError
from io import BytesIO
from PIL import Image
from django.core.files import File


def file_size(value): # add this to some file where you can import it from
    # limit = 2 * 1024 * 1024
    # if value.size > limit:
    #     raise ValidationError('File too large. Size should not exceed 2 MiB.')
    pass

def compress(image):
    if image != None:
        im = Image.open(image)
        im_io = BytesIO() 
        im.save(im_io, 'JPEG', quality=10) 
        new_image = File(im_io, name=image.name)
        return new_image
