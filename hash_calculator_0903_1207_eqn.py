# 代码生成时间: 2025-09-03 12:07:28
# hash_calculator.py
# This script provides a simple hash calculator service using the Falcon framework.

import falcon
import hashlib
import base64
from falcon import API, Request, Response

class HashCalculator:
    def on_get(self, req, resp):
        """
        Handle GET requests and return the hash of the input string.
        """
        input_string = req.get_param("input", default="")
        hash_type = req.get_param("type", default="sha256")

        try:
            if not input_string:
                raise ValueError("Input string is required.")

            hash_object = getattr(hashlib, hash_type)()
            hash_object.update(input_string.encode("utf-8"))
            hash_digest = hash_object.hexdigest()

            resp.media = {"input": input_string, "hash": hash_digest}
            resp.status = falcon.HTTP_200

        except AttributeError:
            resp.media = {"error": f"Unsupported hash type: {hash_type}"}
            resp.status = falcon.HTTP_400
        except ValueError as e:
            resp.media = {"error": str(e)}
            resp.status = falcon.HTTP_400
        except Exception as e:
            resp.media = {"error": f"An unexpected error occurred: {str(e)}"}
            resp.status = falcon.HTTP_500

api = API()
api.add_route("/hash", HashCalculator())

if __name__ == "__main__":
    # Start the server to listen on 0.0.0.0:8000
    api.run(debug=True, host="0.0.0.0", port=8000)