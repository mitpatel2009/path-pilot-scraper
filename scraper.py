import requests

BASE44_API_URL = "https://api.base44.com"  # confirm if your docs show same
BASE44_API_KEY = os.getenv("BASE44_API_KEY")

def push_to_base44(data):
    print("📡 Pushing to Base44...")

    headers = {
        "api_key": BASE44_API_KEY,
        "Content-Type": "application/json"
    }

    created = 0

    for comp in data:
        payload = {
            "title": comp["title"],
            "url": comp["url"],
            "is_scraped": True
        }

        res = requests.post(
            f"{BASE44_API_URL}/entities/Competition",
            json=payload,
            headers=headers
        )

        print("→", comp["title"])
        print("   status:", res.status_code)
        print("   response:", res.text)

        if res.status_code in [200, 201]:
            created += 1

    print(f"✅ Created: {created}/{len(data)}")
    return created
