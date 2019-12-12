import hashlib
import os
import json
from pathlib import Path

class Metadata:

    cwd = Path(os.getcwd())

    def save(self, filename, json_content):
        filename_hash = hashlib.sha1(filename.encode()).hexdigest()
        with open(os.path.join(cwd, '.au', filename)) as metadata:
            metadata.write(json.dumps(json_content))


    def get_metadata(self, filename):
        filename_hash = hashlib.sha1(filename.encode()).hexdigest()
        # find the file inside .au and return it


