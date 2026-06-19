import os

print("Fetching website...")

# Read API key properly
BASE44_API_KEY = os.getenv("BASE44_API_KEY")

if not BASE44_API_KEY:
    print("❌ ERROR: Missing BASE44_API_KEY")
    exit(1)

print("✅ API key loaded successfully")

# -----------------------------
# Your scraping logic here
# -----------------------------

def push_to_base44(data):
    # Example safe check (DO NOT raise blindly anymore)
    if not BASE44_API_KEY:
        print("❌ Missing API key inside function")
        return

    print("📡 Pushing data to Base44...")

    # TODO: your actual Base44 SDK / request logic here
    # Example placeholder:
    # response = requests.post(...)

    print("✅ Data pushed successfully")


# Example flow
data = [
    {"title": "Sample Competition"}
]

print("📦 SCRAPED COMPETITIONS:")
for i, comp in enumerate(data):
    print(f"{i+1}. {comp['title']} - {comp.get('url', 'no url')}")
push_to_base44(data)
