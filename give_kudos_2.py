import asyncio
import os
from playwright.async_api import async_playwright, expect

# --- Configuration ---
# In a CI environment like GitHub Actions, secrets are passed as environment variables.
# We retrieve them using os.environ.get()
EMAIL = os.environ.get("MY_EMAIL")
PASSWORD = os.environ.get("MY_PASSWORD")

# Define a hypothetical secure testing URL
BASE_URL = "https://www.strava.com/login"


async def run(playwright):
    """
    Executes the automated login process using the provided credentials.
    """
    if not EMAIL or not PASSWORD:
        print("ERROR: Credentials (MY_EMAIL and MY_PASSWORD) not found in environment variables.")
        return

    browser = await playwright.chromium.launch(headless=True)
    page = await browser.new_page()

    try:
        print(f"1. Navigating to {BASE_URL}")
        # Always wait for the page to load completely
        await page.goto(BASE_URL, wait_until="domcontentloaded")
    
                # Playwright ensures the element is ready before typing (auto-waiting).
        # Using role and label is the most robust way to locate input fields.
        await page.get_by_label("Email Address").fill(EMAIL)
        
        # Explicitly wait for the main form container to be visible
      #  await page.wait_for_selector('form#login-form-container', state='visible', timeout=10000)
       # print("   Page loaded successfully.")

        # --- Handle the 'Use Password' Option (Simulating Strava's UI requirement) ---
      #  print("2. Checking for 'Use Password Option'...")
        
        # Use a flexible locator that waits for the element to be available in the DOM.
        # This simulates a click required before accessing the email/password fields.
        password_option_button = page.get_by_role("button", name="Use Password Option")
        
        # Use try/except to handle cases where the button might not exist (e.g., if it's the default view)
        if await password_option_button.is_visible():
            print("   'Use Password Option' found and clicking...")
            await password_option_button.click()
            # Wait for the email field to become visible after the click
            await page.get_by_label("Email Address").wait_for(state="visible")
        else:
            print("   Password option not needed (assuming email/pass fields are already visible).")


        # --- Input Credentials ---
        print("3. Entering credentials...")
        
)
        await page.get_by_label("Password").fill(PASSWORD)

        # Ensure the Sign In button is ready before clicking
        sign_in_button = page.get_by_role("button", name="Sign In")
        await sign_in_button.wait_for(state="enabled")
        
        print("4. Clicking Sign In...")
        await sign_in_button.click()

        # --- Verification ---
        # Wait for navigation to the dashboard or a welcome message.
        # Replace 'Dashboard' with an actual unique element/text on the success page.
        print("5. Verifying successful login...")
        await page.wait_for_url("**/dashboard")
        
        # Final check using expect (Playwright's assertion library)
        welcome_message = page.get_by_text("Welcome, Athlete!")
        await expect(welcome_message).to_be_visible()

        print("SUCCESS: Login test passed! Dashboard reached and element found.")

    except Exception as e:
        # In a real CI environment, this will cause the workflow step to fail.
        print(f"FAILURE: An error occurred during the login process: {e}")
        # Capture a screenshot on failure for debugging purposes
        await page.screenshot(path="login_failure_screenshot.png")
        raise e
    finally:
        await browser.close()


async def main():
    """Entry point for the script."""
    async with async_playwright() as playwright:
        await run(playwright)

if __name__ == "__main__":
    asyncio.run(main())
