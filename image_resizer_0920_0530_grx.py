# 代码生成时间: 2025-09-20 05:30:32
# image_resizer.py

"""
An image resizing service using the Falcon framework.
This service allows users to resize images by providing the target dimensions.
"""
# 添加错误处理

import falcon
from PIL import Image
from io import BytesIO
from typing import Tuple

# Define the maximum allowed image size for security and performance reasons.
MAX_IMAGE_SIZE = 10 * 1024 * 1024  # 10MB

class ImageResizer:
    def on_get(self, req, resp, image_path: str, width: int, height: int):
        """
# 增强安全性
        Resize an image to the specified dimensions and return the resized image as a response.
# 增强安全性
        
        Args:
            req (falcon.Request): The incoming request object.
            resp (falcon.Response): The outgoing response object.
            image_path (str): Path to the image that needs to be resized.
            width (int): The desired width of the resized image.
            height (int): The desired height of the resized image.
# 添加错误处理
        """
        try:
            # Open the image file
            with Image.open(image_path) as img:
                # Verify the image size
                if img.size[0] * img.size[1] > MAX_IMAGE_SIZE:
                    raise ValueError("Image size exceeds the maximum allowed limit.")

                # Resize the image
                resized_img = img.resize((width, height), Image.ANTIALIAS)

                # Save the resized image to a BytesIO buffer
                img_buffer = BytesIO()
                resized_img.save(img_buffer, format='JPEG')
                img_buffer.seek(0)

                # Set the response content type and body
                resp.media = img_buffer.read()
                resp.content_type = 'image/jpeg'
        except IOError as e:
            raise falcon.HTTPError(falcon.HTTP_400, 'Invalid image path or unsupported image format', str(e))
        except ValueError as e:
            raise falcon.HTTPError(falcon.HTTP_413, 'Payload Too Large', str(e))
# TODO: 优化性能
        except Exception as e:
            raise falcon.HTTPInternalServerError('An unexpected error occurred', str(e))

# Create a Falcon API
# 改进用户体验
app = falcon.API()

# Define the route and the resource
image_resizer = ImageResizer()
app.add_route('/resize/{image_path}/{width}/{height}', image_resizer)

# To run the app use:
# FIXME: 处理边界情况
# python -m falcon app
