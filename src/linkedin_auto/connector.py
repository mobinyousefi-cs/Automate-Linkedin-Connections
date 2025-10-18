#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
=========================================================================================================
Project: LinkedIn Connections Automator
File: connector.py
Author: Mobin Yousefi (GitHub: https://github.com/mobinyousefi-cs)
Created: 2025-10-18
Updated: 2025-10-18
License: MIT License (see LICENSE file for details)
=========================================================================================================

Description:
Core automation flows: login, send connection requests by profile URLs, or from search results.
Selectors may change; consider them starting points.
"""
from __future__ import annotations

import sys
from typing import Iterable, Optional

from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException, NoSuchElementException

from .utils import human_delay, safe_click, wait_for, exists


LOGIN_URL = "https://www.linkedin.com/login"
SEARCH_URL = "https://www.linkedin.com/search/results/people/?keywords={query}"


def login(driver: WebDriver, email: str, password: str, human_min: float, human_max: float) -> None:
    driver.get(LOGIN_URL)
    human_delay(human_min, human_max)

    # Email field
    if not safe_click(driver, By.ID, "username", timeout=20):
        raise RuntimeError("Could not focus username field")
    driver.find_element(By.ID, "username").send_keys(email)
    human_delay(human_min, human_max)

    # Password field
    if not exists(driver, By.ID, "password", timeout=20):
        raise RuntimeError("Could not find password field")
    driver.find_element(By.ID, "password").send_keys(password)
    human_delay(human_min, human_max)

    # Submit
    driver.find_element(By.ID, "password").send_keys(Keys.RETURN)
    human_delay(human_min, human_max * 2)

    # Heuristic: presence of Me menu indicates logged-in
    if not exists(driver, By.ID, "global-nav", timeout=20):
        raise RuntimeError("Login likely failed. Check credentials or 2FA requirements.")


def add_note_if_present(driver: WebDriver, note: str, human_min: float, human_max: float) -> None:
    # Note dialog may appear after clicking Connect
    try:
        # Try "Add a note" button inside modal
        if safe_click(driver, By.XPATH, "//button[contains(., 'Add a note')]", timeout=3):
            human_delay(human_min, human_max)
            textarea = driver.find_element(By.XPATH, "//textarea[@name='message']")
            textarea.clear()
            textarea.send_keys(note[:280])  # LinkedIn note limit
            human_delay(human_min, human_max)
            # Send
            safe_click(driver, By.XPATH, "//button[contains(., 'Send') and not(@disabled)]", timeout=5)
            return
        # Some UIs open note directly
        if exists(driver, By.XPATH, "//textarea[@name='message']", timeout=2):
            textarea = driver.find_element(By.XPATH, "//textarea[@name='message']")
            textarea.send_keys(note[:280])
            human_delay(human_min, human_max)
            safe_click(driver, By.XPATH, "//button[contains(., 'Send') and not(@disabled)]", timeout=5)
    except NoSuchElementException:
        pass  # Ignore if note UI not available


def connect_on_profile(driver: WebDriver, profile_url: str, *, note: Optional[str],
                       dry_run: bool, human_min: float, human_max: float) -> bool:
    driver.get(profile_url)
    human_delay(human_min, human_max)

    if dry_run:
        return True  # No-op for safety

    # Try primary "Connect" button on profile header
    clicked = safe_click(driver, By.XPATH, "//button[contains(., 'Connect')]", timeout=6)
    if not clicked:
        # Sometimes behind overflow (More button)
        if safe_click(driver, By.XPATH, "//button[contains(., 'More')]", timeout=5):
            human_delay(human_min, human_max)
            clicked = safe_click(driver, By.XPATH, "//div[@role='menu']//span[contains(., 'Connect')]/..", timeout=5)

    if not clicked:
        # Already connected or button not found
        return False

    human_delay(human_min, human_max)

    if note:
        add_note_if_present(driver, note, human_min, human_max)
    else:
        # Confirm without note
        safe_click(driver, By.XPATH, "//button[contains(., 'Send') and not(@disabled)]", timeout=5)

    human_delay(human_min, human_max)
    return True


def search_and_connect(driver: WebDriver, query: str, *, per_page_limit: int, pages: int,
                       note_template: Optional[str], dry_run: bool,
                       human_min: float, human_max: float) -> int:
    total_sent = 0
    for page in range(1, pages + 1):
        url = SEARCH_URL.format(query=query) + f"&page={page}"
        driver.get(url)
        human_delay(human_min, human_max)

        # Grab result cards
        cards = driver.find_elements(
            By.XPATH,
            "//div[contains(@class,'reusable-search__result-container')]"
        )
        sent_this_page = 0
        for card in cards:
            if sent_this_page >= per_page_limit:
                break
            # Prefer a visible 'Connect' button in the card
            btns = card.find_elements(By.XPATH, ".//button[.//span[contains(., 'Connect')]]")
            if not btns:
                continue
            if dry_run:
                sent_this_page += 1
                total_sent += 1
                continue
            try:
                btns[0].click()
                human_delay(human_min, human_max)
                if note_template:
                    add_note_if_present(driver, note_template, human_min, human_max)
                else:
                    safe_click(driver, By.XPATH, "//button[contains(., 'Send') and not(@disabled)]", timeout=5)
                human_delay(human_min, human_max)
                sent_this_page += 1
                total_sent += 1
            except Exception:
                continue

        # Small scroll to mimic human behavior between pages
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight * 0.5);")
        human_delay(human_min, human_max)
    return total_sent
