import os
import requests
from bs4 import BeautifulSoup

BASE44_API_KEY = os.environ.get("BASE44_API_KEY")

BASE44_URL = "https://api.base44.com/v1/entities/Competition"

HEADERS = {
    "Authorization": f"Bearer {BASE44_API_KEY}",
    "Content-Type": "application/json"
}

SOURCE_URL = "https://www.studentcompetitions.com/competitions"


def scrape():
    print("Fetching website...")

    res = requests.get(
        SOURCE_URL,
        headers={"User-Agent": "Mozilla/5.0"}
    )

    soup = BeautifulSoup(res.text, "html.parser")

    competitions = []

    # find all links that look like competition pages
    for a in soup.find_all("a", href=True):
        href = a["href"]
        title = a.get_text(strip=True)

        if "/competition" in href and title and len(title) > 5:
            full_url = (
                href if href.startswith("http")
                else "https://www.studentcompetitions.com" + href
            )

            competitions.append({
                "title": title,
                "url": full_url,
                "description": "",
                "skills": ["Unknown"],
                "difficulty": "Beginner",
                "is_scraped": True
            })

    # remove duplicates
    seen = set()
    unique = []

    for c in competitions:
        if c["url"] not in seen:
            unique.append(c)
            seen.add(c["url"])

    print(f"Found {len(unique)} competitions")
    return unique


def push_to_base44(data):
    if not BASE44_API_KEY:
        raise Exception("Missing BASE44_API_KEY")

    for item in data:
        r = requests.post(BASE44_URL, json=item, headers=HEADERS)
        print("Sent:", r.status_code, r.text)


if __name__ == "__main__":
    data = scrape()
    push_to_base44(data)
    print("DONE")
