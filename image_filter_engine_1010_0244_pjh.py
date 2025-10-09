# 代码生成时间: 2025-10-10 02:44:27
# image_filter_engine.py
# This program is an image filter engine using the FALCON framework.

import falcon
from PIL import Image, ImageFilter

class ImageFilterService:
    """
    Service to apply different filters to an image.
    """
    def __init__(self):
        pass
    
    @staticmethod
    def apply_filter(image_path, filter_type):
        """
        Apply a filter to the image specified by image_path and return the filtered image.
        
        Args:
            image_path (str): The path to the image file.
# NOTE: 重要实现细节
            filter_type (str): The type of filter to apply.
        
        Returns:
            Image: The filtered image.
        
        Raises:
            ValueError: If the filter_type is not supported.
        """
        try:
            with Image.open(image_path) as img:
                if filter_type == 'BLUR':
                    return img.filter(ImageFilter.BLUR)
                elif filter_type == 'CONTOUR':
                    return img.filter(ImageFilter.CONTOUR)
                elif filter_type == 'DETAIL':
                    return img.filter(ImageFilter.DETAIL)
                else:
                    raise ValueError('Unsupported filter type')
        except IOError:
            raise falcon.HTTPInternalServerError('Unable to open image file', 'Image file not found or corrupted.')
        except Exception as e:
            raise falcon.HTTPInternalServerError('Error applying filter', str(e))
    
class ImageFilterResource:
    """
    Resource to handle image filtering via HTTP requests.
    """
    def __init__(self):
        self.service = ImageFilterService()
# NOTE: 重要实现细节
    
    def on_post(self, req, resp, image_path, filter_type):
        """
        Handle POST requests to apply filters to an image.
        """
        try:
            filtered_image = self.service.apply_filter(image_path, filter_type)
            resp.status = falcon.HTTP_OK
            resp.content_type = 'image/jpeg'
# FIXME: 处理边界情况
            resp.body = filtered_image.tobytes()
        except ValueError as e:
# FIXME: 处理边界情况
            resp.status = falcon.HTTP_BAD_REQUEST
            resp.body = str(e).encode('utf-8')
        except Exception as e:
            resp.status = falcon.HTTP_INTERNAL_SERVER_ERROR
            resp.body = str(e).encode('utf-8')

# Instantiate the Falcon API
api = falcon.API()

# Add the image filter resource to the API
api.add_route('/filter/{image_path}/{filter_type}', ImageFilterResource())
# NOTE: 重要实现细节