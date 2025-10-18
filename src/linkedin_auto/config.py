#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
=========================================================================================================
Project: LinkedIn Connections Automator
File: config.py
Author: Mobin Yousefi (GitHub: https://github.com/mobinyousefi-cs)
Created: 2025-10-18
Updated: 2025-10-18
License: MIT License (see LICENSE file for details)
=========================================================================================================

Description:
Configuration loader for environment variables and defaults. Supports .env files.
"""
from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Optional

from dotenv import load_dotenv


@dataclass(frozen=True)
class Settings:
    email: str
    password: str
    headless: bool
    profile_dir: Optional[str]
    dry_run: bool
    implicit_wait: float
    page_load_timeout: float
    max_connects_per_page: int
    human_delay_min: float
    human_delay_max: float
    note_template: Optional[str]


def load_settings() -> Settings:
    load_dotenv(override=False)

    def _bool(name: str, default: bool) -> bool:
        v = os.getenv(name, str(default)).strip().lower()
        return v in {"1", "true", "yes", "y", "on"}

    def _float(name: str, default: float) -> float:
        try:
            return float(os.getenv(name, str(default)))
        except ValueError:
            return default

    email = os.getenv("LI_EMAIL", "").strip()
    password = os.getenv("LI_PASSWORD", "").strip()

    return Settings(
        email=email,
        password=password,
        headless=_bool("LI_HEADLESS", True),
        profile_dir=os.getenv("LI_PROFILE_DIR") or None,
        dry_run=_bool("LI_DRY_RUN", True),
        implicit_wait=_float("LI_IMPLICIT_WAIT", 1.0),
        page_load_timeout=_float("LI_PAGE_LOAD_TIMEOUT", 45.0),
        max_connects_per_page=int(os.getenv("LI_MAX_CONNECTS_PER_PAGE", "10")),
        human_delay_min=_float("LI_HUMAN_DELAY_MIN", 1.0),
        human_delay_max=_float("LI_HUMAN_DELAY_MAX", 2.75),
        note_template=os.getenv("LI_NOTE_TEMPLATE") or None,
    )
