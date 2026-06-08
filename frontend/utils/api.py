from __future__ import annotations

import httpx
import streamlit as st

BASE_URL = "http://localhost:8000"


def _headers() -> dict:
    token = st.session_state.get("token")
    if token:
        return {"Authorization": f"Bearer {token}"}
    return {}


# Auth

def login(username: str, password: str) -> tuple:
    r = httpx.post(
        f"{BASE_URL}/auth/login",
        data={"username": username, "password": password},
    )
    return r.json(), r.status_code


def register(username: str, password: str) -> tuple:
    r = httpx.post(
        f"{BASE_URL}/auth/register",
        json={"username": username, "password": password},
    )
    return r.json(), r.status_code


# Games

def get_games(q=None, platform=None, status=None) -> list:
    params = {}
    if q:
        params["q"] = q
    if platform:
        params["platform"] = platform
    if status:
        params["status"] = status
    r = httpx.get(f"{BASE_URL}/games/", headers=_headers(), params=params)
    if r.status_code == 200:
        return r.json()
    return []


def get_game(game_id: int):
    r = httpx.get(f"{BASE_URL}/games/{game_id}", headers=_headers())
    if r.status_code == 200:
        return r.json()
    return None


def create_game(data: dict) -> tuple:
    r = httpx.post(f"{BASE_URL}/games/", headers=_headers(), json=data)
    return r.json(), r.status_code


def update_game(game_id: int, data: dict) -> tuple:
    r = httpx.put(f"{BASE_URL}/games/{game_id}", headers=_headers(), json=data)
    return r.json(), r.status_code


def delete_game(game_id: int) -> int:
    r = httpx.delete(f"{BASE_URL}/games/{game_id}", headers=_headers())
    return r.status_code


def get_stats() -> dict:
    r = httpx.get(f"{BASE_URL}/games/stats/summary", headers=_headers())
    if r.status_code == 200:
        return r.json()
    return {}
