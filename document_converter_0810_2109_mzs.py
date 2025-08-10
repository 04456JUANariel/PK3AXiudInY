# 代码生成时间: 2025-08-10 21:09:44
# document_converter.py

"""
A document converter application using Falcon framework.
This application allows users to convert documents between
different formats.
"""

import falcon
from falcon import API, media, testing
from falcon.media import JSONHandler
import json
from docx import Document
from docxtpl import DocxTemplate
from docx.shared import Inches
from docx.oxml.ns import qn
from docx.enum.text import WD_ALIGN_PARAGRAPH

# Define an error handler for 400 Bad Request
class ErrorHandler:
    def process_request(self, req, resp):
        pass

    def process_response(self, req, resp, resource):
        if resp.status == falcon.HTTP_400:
            raise falcon.HTTPError(f"{resp.status} Bad Request", "The request was malformed.")

    def process_resource_exception(self, req, resp, resource, exception):
        raise falcon.HTTPError(f"{resp.status} Bad Request", "An error occurred while processing your request.")

class DocumentConverter:
    """
    A resource for converting documents between different formats.
    Currently supports conversion from Word to PDF.
    """

    def on_get(self, req, resp):
        """
        Handles GET requests.
        Returns a list of supported formats.
        """
        resp.media = {"supported_formats": ["docx", "pdf"]}
        resp.status = falcon.HTTP_200

    def on_post(self, req, resp):
        """
        Handles POST requests.
        Expects a JSON payload with the document and the desired format.
        """
        try:
            # Parse the JSON payload
            payload = json.load(req.bounded_stream)
            document = payload.get("document")
            desired_format = payload.get("format")

            # Validate the payload
            if not document or not desired_format:
                raise falcon.HTTPError(falcon.HTTP_400, "Missing required parameters.")

            # Convert the document to the desired format
            if desired_format == "pdf":
                self.convert_to_pdf(document)
            else:
                raise falcon.HTTPError(falcon.HTTP_400, f"Unsupported format: {desired_format}")

            # Return the converted document as a JSON object
            resp.media = {"message": "Document converted successfully."}
            resp.status = falcon.HTTP_200
        except json.JSONDecodeError:
            raise falcon.HTTPError(falcon.HTTP_400, "Invalid JSON payload.")
        except Exception as e:
            raise falcon.HTTPError(falcon.HTTP_500, str(e))

    def convert_to_pdf(self, document):
        """
        Converts a Word document to PDF.
        """
        # Load the Word document
        doc = Document(document)

        # Save the document as PDF
        doc.save(f"{document}.pdf")

# Create an instance of the Falcon API
api = API(middleware=[ErrorHandler()])

# Add the resource to the API
api.add_route("/convert", DocumentConverter())

# Define a test client for testing the API
class TestClient:
    def __init__(self, api):
        self.api = api

    def simulate_request(self, method, path, body=None):
        """
        Simulates a request to the API.
        """
        sim_req = testing.TestRequest(path, method)
        if body:
            sim_req.media = body
        sim_resp = testing.TestResponse()
        self.api(req=sim_req, resp=sim_resp)
        return sim_resp

# Create a test client and simulate a request
client = TestClient(api)
resp = client.simulate_request("POST", "/convert", {"document": "example.docx", "format": "pdf"})
print(resp.media)