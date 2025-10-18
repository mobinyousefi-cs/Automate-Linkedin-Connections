#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
=========================================================================================================
Project: LinkedIn Connections Automator
File: utils.py
Author: Mobin Yousefi (GitHub: https://github.com/mobinyousefi-cs)
Created: 2025-10-18
Updated: 2025-10-18
License: MIT License (see LICENSE file for details)
=========================================================================================================

Description:
Utility helpers for logging, safe element interactions, and human-like delays.
"""
from __future__ import annotations

import random
import time
from typing import Callable, Optional

from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC  # type: ignore
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException, WebDriverException


def human_delay(min_s: float = 1.0, max_s: float = 2.5) -> None:
    """Sleep a pseudo-random duration to mimic human behavior."""
    duration = random.uniform(min_s, max_s)
    time.sleep(duration)


def wait_for(driver: WebDriver, condition: Callable, timeout: float = 20.0):
    return WebDriverWait(driver, timeout).until(condition)


def safe_click(driver: WebDriver, by: By, value: str, timeout: float = 15.0) -> bool:
    try:
        elem = wait_for(driver, EC.element_to_be_clickable((by, value)), timeout)
        elem.click()
        return True
    except (TimeoutException, WebDriverException):
        return False


def exists(driver: WebDriver, by: By, value: str, timeout: float = 5.0) -> bool:
    try:
        wait_for(driver, EC.presence_of_element_located((by, value)), timeout)
        return True
    except TimeoutException:
        return False
