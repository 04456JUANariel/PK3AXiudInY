# 代码生成时间: 2025-08-13 11:32:08
import os
import re
from falcon import Falcon, Request, Response

# Batch File Renamer API
class BatchFileRenamer:
    def __init__(self, directory):
        self.directory = directory

    def rename_files(self, prefix, suffix):
        """Renames files in the specified directory with the given prefix and suffix.

        Args:
            prefix (str): The new base name for the files.
            suffix (str): The new extension for the files.

        Returns:
            list: A list of tuples containing the old and new file names.
        """
        old_new_files = []
        for filename in os.listdir(self.directory):
            old_file = os.path.join(self.directory, filename)
            if os.path.isfile(old_file):
                new_filename = f"{prefix}_{filename}{suffix}"
                new_file = os.path.join(self.directory, new_filename)
                try:
                    os.rename(old_file, new_file)
                    old_new_files.append((old_file, new_file))
                except OSError as e:
                    print(f"Error renaming file {old_file} to {new_file}: {e}")
        return old_new_files

# Falcon API setup
api = Falcon()

# Define the route for renaming files
@api.route('/rename', methods=['POST'])
class RenameFileResource:
    def on_post(self, req, resp):
        # Get the directory and renaming parameters from the request
        try:
            body = req.media or {}
            directory = body.get('directory')
            prefix = body.get('prefix')
            suffix = body.get('suffix')

            if not all([directory, prefix, suffix]):
                raise ValueError('Missing required parameters in the request.')

            # Instantiate the renamer and perform the operation
            renamer = BatchFileRenamer(directory)
            results = renamer.rename_files(prefix, suffix)

            # Return the results as a JSON response
            resp.media = {'results': results}
            resp.status = falcon.HTTP_200
        except ValueError as e:
            resp.media = {'error': str(e)}
            resp.status = falcon.HTTP_400
        except Exception as e:
            resp.media = {'error': 'An unexpected error occurred.'}
            resp.status = falcon.HTTP_500

if __name__ == '__main__':
    # Start the Falcon API on port 8000
    from wsgiref.simple_server import make_server
    httpd = make_server('localhost', 8000, api)
    print("Serving on port 8000...
")
    httpd.serve_forever()