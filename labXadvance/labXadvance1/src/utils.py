"""Helper functions: saving data (JSON/CSV), explicit waits, retries, robots.txt check."""
import csv
import json
import os
import time
from typing import Any, Callable, Dict, List
from urllib import robotparser
from urllib.parse import urljoin, urlparse

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


def save_data_to_json(data: List[Dict[str, Any]], filepath: str):
    """Save a list of dicts to a pretty-printed UTF-8 JSON file."""
    os.makedirs(os.path.dirname(filepath) or ".", exist_ok=True)
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


def save_data_to_csv(data: List[Dict[str, Any]], filepath: str):
    """Save a list of dicts to a CSV file (header taken from the first item)."""
    os.makedirs(os.path.dirname(filepath) or ".", exist_ok=True)
    if not data:
        open(filepath, "w", encoding="utf-8-sig").close()
        return
    with open(filepath, "w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(data[0].keys()))
        writer.writeheader()
        writer.writerows(data)


def wait_for_element(driver, selector: str, timeout: int = 10, by: By = By.CSS_SELECTOR):
    """Explicit wait: block until at least one element matching the selector is present."""
    return WebDriverWait(driver, timeout).until(
        EC.presence_of_element_located((by, selector))
    )


def retry(action: Callable, max_retries: int = 3, delay: float = 2.0, description: str = "action"):
    """
    Run `action()` and retry on any exception (transient network/DOM errors).
    Waits `delay` seconds between attempts, doubling each time (simple backoff).
    Re-raises the last error if all attempts fail.
    """
    last_error = None
    for attempt in range(1, max_retries + 1):
        try:
            return action()
        except Exception as e:  # noqa: BLE001 - we deliberately retry on any transient error
            last_error = e
            print(f"  [Retry] {description} failed (attempt {attempt}/{max_retries}): {type(e).__name__}")
            if attempt < max_retries:
                time.sleep(delay)
                delay *= 2
    raise last_error


def safe_click(driver, element):
    """Scroll the element into view, then click it (falls back to a JS click if intercepted)."""
    driver.execute_script("arguments[0].scrollIntoView(true);", element)
    time.sleep(0.5)
    try:
        element.click()
    except Exception:
        driver.execute_script("arguments[0].click();", element)


def is_allowed_by_robots(url: str, user_agent: str = "*") -> bool:
    """
    Check the site's robots.txt before scraping.
    If robots.txt cannot be read (offline, local file, no file), scraping is allowed with a warning.
    """
    parsed = urlparse(url)
    if parsed.scheme not in ("http", "https"):
        return True
    robots_url = urljoin(f"{parsed.scheme}://{parsed.netloc}", "/robots.txt")
    rp = robotparser.RobotFileParser()
    rp.set_url(robots_url)
    try:
        rp.read()
    except Exception as e:  # noqa: BLE001
        print(f"  [Warning] Could not read {robots_url} ({type(e).__name__}); proceeding carefully.")
        return True
    return rp.can_fetch(user_agent, url)
