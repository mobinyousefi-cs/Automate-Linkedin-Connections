#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
=========================================================================================================
Project: LinkedIn Connections Automator
File: driver.py
Author: Mobin Yousefi (GitHub: https://github.com/mobinyousefi-cs)
Created: 2025-10-18
Updated: 2025-10-18
License: MIT License (see LICENSE file for details)
=========================================================================================================

Description:
WebDriver factory with sane defaults: headless, user-agent, timeouts, optional Chrome profile.
"""
from __future__ import annotations

import platform
from typing import Optional

from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager


def build_chrome(headless: bool = True, profile_dir: Optional[str] = None,
                 page_load_timeout: float = 45.0, implicit_wait: float = 1.0) -> webdriver.Chrome:
    options = ChromeOptions()
    if headless:
        # Chrome >= 109 uses the new headless mode
        options.add_argument("--headless=new")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1280,900")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--no-sandbox")
    options.add_argument("--lang=en-US")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--disable-extensions")
    options.add_argument("--start-maximized")
    options.add_argument("--user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
                         "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")

    if profile_dir:
        # WARNING: Using a profile on multiple concurrent runs can corrupt it.
        options.add_argument(f"--user-data-dir={profile_dir}")

    # On Windows, avoid console window
    service = ChromeService(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    driver.set_page_load_timeout(page_load_timeout)
    driver.implicitly_wait(implicit_wait)
    return driver
