# /// script
# requires-python = ">=3.13"
# dependencies = [
#     "zxing-cpp",
#   "opencv-python",
# ]
# ///
import cv2
import json
from zxingcpp import read_barcode
import bcbp
import sys

class BCBPEncoder(json.JSONEncoder):
    def default(self, obj):
        if hasattr(obj, '__dict__'):
            return obj.__dict__
        return str(obj)

def scan_boarding_pass(image_path):
    # Read the image
    img = cv2.imread(image_path)
    # Decode barcode using zxing-cpp
    result = read_barcode(img)

    if not result:
        return {"error": "No barcode found"}

    # Extract data
    barcode_data = result.text

    # Parse boarding pass data
    try:
        boarding_pass = bcbp.decode(barcode_data)
        str_boarding_pass = str(boarding_pass)

        # Try to parse as JSON if it's a JSON string
        try:
            decoded_json = json.loads(str_boarding_pass)
            return {"raw_data": barcode_data, "decoded": decoded_json}
        except json.JSONDecodeError:
            # If not valid JSON, return as string
            return {"raw_data": barcode_data, "decoded": str_boarding_pass}
    except Exception as e:
        return {"error": f"Failed to parse: {str(e)}", "raw_data": barcode_data}

if __name__ == "__main__":
    result = scan_boarding_pass(sys.argv[1])

    formatted_json = json.dumps(result, indent=2, sort_keys=True, ensure_ascii=False)
    print(formatted_json)
