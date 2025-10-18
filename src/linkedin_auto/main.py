#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
=========================================================================================================
Project: LinkedIn Connections Automator
File: main.py
Author: Mobin Yousefi (GitHub: https://github.com/mobinyousefi-cs)
Created: 2025-10-18
Updated: 2025-10-18
License: MIT License (see LICENSE file for details)
=========================================================================================================

Description:
Typer-based CLI for automating limited LinkedIn connection flows.
Usage:
    python -m linkedin_auto --help
Notes:
- Use with caution. May violate LinkedIn ToS. Prefer dry-run first.
"""
from __future__ import annotations

import sys
from pathlib import Path
from typing import Optional

import typer
from rich import print
from rich.console import Console
from rich.table import Table

from .config import load_settings
from .driver import build_chrome
from .connector import login, connect_on_profile, search_and_connect
from . import __version__

app = typer.Typer(add_completion=False, no_args_is_help=True)
console = Console()


@app.command()
def version():
    """Show package version."""
    print(f"[bold cyan]linkedin-auto[/] v{__version__}")


@app.command()
def login_check():
    """
    Attempt to login once (non-intrusive) to verify credentials and setup.
    """
    cfg = load_settings()
    if not cfg.email or not cfg.password:
        typer.echo("Missing LI_EMAIL/LI_PASSWORD in environment or .env")
        raise typer.Exit(code=2)

    driver = build_chrome(headless=cfg.headless, profile_dir=cfg.profile_dir,
                          page_load_timeout=cfg.page_load_timeout, implicit_wait=cfg.implicit_wait)
    try:
        login(driver, cfg.email, cfg.password, cfg.human_delay_min, cfg.human_delay_max)
        print("[green]Login appears successful.[/]")
    finally:
        driver.quit()


@app.command()
def connect_urls(
    file: Path = typer.Option(..., "--file", "-f", exists=True, readable=True, help="Text file with profile URLs (one per line)"),
    note: Optional[str] = typer.Option(None, "--note", "-n", help="Optional note to include (<=280 chars)."),
):
    """
    Send (or simulate) connection requests to the LinkedIn profile URLs in FILE.
    Honors LI_DRY_RUN and rate limits per your environment settings.
    """
    cfg = load_settings()
    urls = [u.strip() for u in file.read_text(encoding="utf-8").splitlines() if u.strip()]

    driver = build_chrome(headless=cfg.headless, profile_dir=cfg.profile_dir,
                          page_load_timeout=cfg.page_load_timeout, implicit_wait=cfg.implicit_wait)
    try:
        login(driver, cfg.email, cfg.password, cfg.human_delay_min, cfg.human_delay_max)
        sent = 0
        for url in urls:
            ok = connect_on_profile(
                driver,
                url,
                note=(note or cfg.note_template),
                dry_run=cfg.dry_run,
                human_min=cfg.human_delay_min,
                human_max=cfg.human_delay_max,
            )
            sent += 1 if ok else 0

        table = Table(title="Connection Summary")
        table.add_column("Mode", justify="left")
        table.add_column("Count", justify="right")
        table.add_row("Dry-run" if cfg.dry_run else "Live", str(sent))
        console.print(table)
    finally:
        driver.quit()


@app.command()
def connect_search(
    query: str = typer.Argument(..., help="People search keywords (e.g., 'Data Scientist Milan')"),
    pages: int = typer.Option(1, "--pages", "-p", min=1, max=10, help="Number of search pages to iterate"),
):
    """
    Send (or simulate) connection requests from LinkedIn search results for QUERY.
    Respects LI_MAX_CONNECTS_PER_PAGE and LI_DRY_RUN.
    """
    cfg = load_settings()
    driver = build_chrome(headless=cfg.headless, profile_dir=cfg.profile_dir,
                          page_load_timeout=cfg.page_load_timeout, implicit_wait=cfg.implicit_wait)
    try:
        login(driver, cfg.email, cfg.password, cfg.human_delay_min, cfg.human_delay_max)
        total = search_and_connect(
            driver,
            query=query,
            per_page_limit=cfg.max_connects_per_page,
            pages=pages,
            note_template=cfg.note_template,
            dry_run=cfg.dry_run,
            human_min=cfg.human_delay_min,
            human_max=cfg.human_delay_max,
        )
        print(f"[bold]{'Dry-run' if cfg.dry_run else 'Live'}[/] total on '{query}': {total}")
    finally:
        driver.quit()


def main():
    app()


if __name__ == "__main__":
    main()
