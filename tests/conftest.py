import os
import tempfile

os.environ["DATA_DIR"] = tempfile.mkdtemp(prefix="autoprint-tests-")
os.environ["ADMIN_USERNAME"] = ""
os.environ["ADMIN_PASSWORD"] = ""

