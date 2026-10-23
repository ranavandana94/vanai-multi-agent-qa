
from playwright.sync_api import Page


def test_playwright_browser(page: Page):
    response = page.goto(
        "https://example.com",
        wait_until="domcontentloaded"
    )

    print("\nStatus:", response.status if response else None)
    print("URL:", page.url)
    print("Title:", page.title())
    print("HTML:", page.content()[:2000])
    print("Body text:", page.locator("body").inner_text()[:1000])

    assert page.title() == "Example Domain"
