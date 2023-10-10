
from django.core.exceptions import ValidationError
def validate_image(image ):
        # print('^^^^^^^^^6',type(image))
        if image.size >1048576 :
            raise ValidationError(f'Image size must be less than 1 mb , {type(image)}')

        else:
            return image