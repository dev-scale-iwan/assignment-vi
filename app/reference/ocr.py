import base64
import os
from dotenv import load_dotenv
from mistralai.client import Mistral

print("Loading environment variables...")
load_dotenv()

try:
    api_key = os.environ["MISTRALAI_API_KEY"]
    print(f"API key loaded: {api_key[:10]}...")
except KeyError:
    print("ERROR: MISTRALAI_API_KEY not found in environment variables!")
    print("Please set the MISTRALAI_API_KEY environment variable.")
    exit(1)

print("Initializing Mistral client...")
client = Mistral(api_key=api_key)

def main():
    print("Starting OCR processing...")
    ocr_response = client.ocr.process(
        model="mistral-ocr-latest",
        document={
            "type": "document_url",
            "document_url": "https://arxiv.org/pdf/2201.04234"
        },
        table_format="html", # default is None
        include_image_base64=True
    )

    print(f"Processing {len(ocr_response.pages)} pages...")

    full_content = ""
    image_data = ""

    for page in ocr_response.pages:
        full_content += page.markdown
        for image in page.images:
            image_data += image.image_base64 # data:image/png;base64,.....
            if "," in image_data:
                image_data = image_data.split(",")[1] # Remove the prefix
            with open(image.id, "wb") as f:
                f.write(base64.b64decode(image_data))
        
    with open("output.md", "w", encoding="utf-8") as f:
        f.write(full_content)

    print(f"✓ OCR complete! Output saved to output.md ({len(full_content)} characters)")

if __name__ == "__main__":
    main()