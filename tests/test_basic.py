#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
=========================================================================================================
Project: LinkedIn Connections Automator
File: test_basic.py
Author: Mobin Yousefi (GitHub: https://github.com/mobinyousefi-cs)
Created: 2025-10-18
Updated: 2025-10-18
License: MIT License (see LICENSE file for details)
=========================================================================================================

Description:
Basic offline unit tests (no network, no webdriver). CI-safe.
"""
from linkedin_auto.config import load_settings
from linkedin_auto.utils import human_delay


def test_config_defaults_envless(monkeypatch):
    # Ensure no envs to test defaults
    monkeypatch.delenv("LI_EMAIL", raising=False)
    monkeypatch.delenv("LI_PASSWORD", raising=False)
    s = load_settings()
    assert s.headless is True
    assert s.dry_run is True
    assert s.max_connects_per_page >= 1
    assert s.human_delay_min < s.human_delay_max


def test_human_delay_runs_quickly(monkeypatch):
    # Make delay tiny to keep tests instant
    human_delay(0.0, 0.0)
    assert True
