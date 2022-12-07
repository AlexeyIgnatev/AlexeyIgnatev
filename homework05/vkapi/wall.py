import textwrap
import time
import typing as tp
from string import Template

import pandas as pd
import requests
from pandas import json_normalize
from vkapi import config, session
from vkapi.exceptions import APIError
from math import ceil

domainVK = config.VK_CONFIG["domain"]
access_token = config.VK_CONFIG["access_token"]
v = config.VK_CONFIG["version"]


def get_posts_2500(
    owner_id: str = "",
    domain: str = "",
    offset: int = 0,
    count: int = 10,
    max_count: int = 2500,
    filter: str = "owner",
    extended: int = 0,
    fields: tp.Optional[tp.List[str]] = None,
) -> tp.Dict[str, tp.Any]:
    code = """return API.wall.get({
                '"owner_id": "owner_id"',
                '"domain": "domain"',
                '"offset": offset',
                '"count": "1"',
                '"filter": "filter"',
                '"extended": extended',
                '"fields": "fields"',
                '"v": "v"'
                });"""
    post = requests.post(
        url=f"{domainVK}/execute",
        data={"code": code, "access_token": f"{access_token}", "v": f"{v}"},
    )
    return post.json()["response"]["items"]


def get_wall_execute(
    owner_id: str = "",
    domain: str = "",
    offset: int = 0,
    count: int = 10,
    max_count: int = 2500,
    filter: str = "owner",
    extended: int = 0,
    fields: tp.Optional[tp.List[str]] = None,
    progress=None,
) -> pd.DataFrame:
    offset_count = ceil(count / max_count)
    response: tp.List[str] = []
    for i in range(offset_count):
        posts = get_posts_2500(
            owner_id, domain, i * 2500, max_count, max_count, filter, extended, fields
        )
        response += posts
        time.sleep(0.68)
    return json_normalize(response)

