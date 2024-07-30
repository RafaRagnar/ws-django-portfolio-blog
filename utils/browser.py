from time import sleep
from selenium import webdriver


def make_chrome_browser(headless=False):
    """Creates a new Chrome browser instance, optionally in headless mode.

    Args:
        headless (bool, optional): Whether to run the browser in headless mode.
        Defaults to False.

    Returns:
        webdriver.Chrome: The newly created Chrome browser instance.
    """
    options = webdriver.EdgeOptions()
    if headless:
        # Use --headless=new for latest versions
        options.add_argument("--headless=new")

    driver = webdriver.Edge(options=options)
    return driver


if __name__ == "__main__":
    # Set headless to True for headless mode
    browser = make_chrome_browser(headless=False)
    browser.get("http://www.udemy.com/")
    # Add your browser interactions here (e.g., find elements, interact with
    # the page)
    sleep(50)  # Wait for 5 seconds to see the page
    # ... your code to interact with the browser ...

    browser.quit()
