# Web Scraping Ethics and Legality Guidelines

This document outlines important ethical and legal considerations when engaging in web scraping. It is crucial to understand and adhere to these principles to avoid legal issues, IP blocking, or causing harm to website owners.

## 1. Respect `robots.txt`

The `robots.txt` file is a standard that websites use to communicate with web crawlers and scrapers. It tells bots which parts of the site they are allowed to access and which parts are forbidden.

* **Always check:** Before scraping any website, visit `https://[website-domain]/robots.txt` (e.g., `https://example.com/robots.txt`).
* **Adhere to rules:** If `robots.txt` disallows scraping a certain path, **do not scrape it**. This is a direct request from the website owner.

## 2. Review Terms of Service (ToS)

Many websites include clauses in their Terms of Service that explicitly prohibit web scraping, data mining, or automated access.

* **Read the fine print:** If a website's ToS explicitly forbids scraping, then scraping that site is a breach of contract and could lead to legal action (e.g., Cease and Desist letters, lawsuits).
* **Implied consent:** Absence of a specific prohibition does not automatically grant permission.

## 3. Be Polite: Rate Limiting and Delays

Overwhelming a website's server with too many requests in a short period can be interpreted as a Denial-of-Service (DoS) attack, impacting the site's performance for legitimate users.

* **Introduce Delays:** Use `time.sleep()` between requests or pages to mimic human browsing behavior. A delay of 2-5 seconds is a common starting point, but adjust based on the site's load.
* **Avoid Concurrent Requests:** Unless you know what you are doing and have explicit permission, avoid sending multiple requests simultaneously.
* **Monitor Server Load:** If you notice slower response times or errors, reduce your request rate.

## 4. Identify Yourself (User-Agent)

When making requests, include a descriptive `User-Agent` header that identifies your scraper. This allows website administrators to contact you if there are issues.

* **Example:** `Mozilla/5.0 (compatible; MyCustomScraper/1.0; mailto:your_email@example.com)`
* **Avoid generic agents:** Do not impersonate common browsers or Googlebot unless your scraper genuinely behaves like them and respects their rules.

## 5. Do Not Impersonate or Hide (Ethically)

While some advanced anti-bot measures might necessitate techniques like rotating IP addresses or using headless browsers, prioritize ethical considerations:

* **Transparency:** If possible, be transparent about your scraping activities.
* **Avoid malicious intent:** Do not use scraped data for illegal activities, spam, or competitive disadvantage where it violates the ToS.

## 6. Data Usage and Copyright

* **Copyright:** Scraped content is often copyrighted. You generally cannot republish, distribute, or monetize scraped data without explicit permission from the copyright holder.
* **Fair Use:** Understand your local "fair use" (or similar) doctrines, but these are often narrow and context-dependent.
* **Personal Use:** Scraping for personal, non-commercial use (e.g., research, personal archive) is generally less risky but still subject to ToS.

## 7. Legal Precedents and Risks

The legal landscape for web scraping is evolving and varies by country. Notable cases exist where scraping has been deemed illegal, particularly when it involves:

* Breaching ToS / contract.
* Trespass to chattels (unauthorized access to computer systems causing harm).
* Copyright infringement.
* Data privacy violations (e.g., scraping personal identifiable information (PII) without consent).

**In summary, always act responsibly, respectfully, and legally. When in doubt, seek explicit permission from the website owner.**

## 8. How this project applies these rules

| Rule | Where in the code |
| :-- | :-- |
| Check `robots.txt` before scraping | `is_allowed_by_robots()` in `src/utils.py`, called at the start of `ScraperAgent.run()` (`respect_robots_txt` in the config) |
| Rate limiting | `delay_between_pages` in the config (default 2 seconds) and `max_pages` as a hard limit |
| Don't hammer a failing server | `retry()` waits between attempts and doubles the delay each time, then gives up after `max_retries` |
| Safe practice target | The example config uses `books.toscrape.com`, a site built for scraping practice |
| No personal data | Only product name, price, URL and image URL are collected |
