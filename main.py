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

def scan_boarding_pass(image_path):
    img = cv2.imread(image_path)
    result = read_barcode(img)

    if not result:
        return {"error": "No barcode found"}

    barcode_data = result.text

    try:
        boarding_pass = bcbp.decode(barcode_data)
        str_boarding_pass = str(boarding_pass)

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

    print(json.dumps(result, indent=2, sort_keys=True, ensure_ascii=False))
