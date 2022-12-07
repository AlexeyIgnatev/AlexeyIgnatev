import dataclasses
import time
import typing as tp
from math import ceil

import requests
from vkapi import config, session
from vkapi.config import VK_CONFIG
from vkapi.exceptions import APIError

QueryParams = tp.Optional[tp.Dict[str, tp.Union[str, int]]]


@dataclasses.dataclass(frozen=True)
class FriendsResponse:
    count: int
    items: tp.List[tp.Dict[str, tp.Any]]


def get_friends(
    user_id: int, count: int = 5000, offset: int = 0, fields: tp.Optional[tp.List[str]] = None
) -> FriendsResponse:
    response = session.get(
        "friends.get",
        user_id=user_id,
        count=count,
        offset=offset,
        fields=fields,
        access_token=VK_CONFIG["access_token"],
        v=VK_CONFIG["version"],
    ).json()["response"]
    return FriendsResponse(count=response["count"], items=response["items"])


class MutualFriends(tp.TypedDict):
    id: int
    common_friends: tp.List[int]
    common_count: int


def get_mutual(
    source_uid: tp.Optional[int] = None,
    target_uid: tp.Optional[int] = None,
    target_uids: tp.Optional[tp.List[int]] = None,
    order: str = "",
    count: tp.Optional[int] = None,
    offset: int = 0,
    progress=None,
) -> tp.List[MutualFriends]:

    mutual_friends = []
    if target_uids is None:
        c = 1
    else:
        c = ceil((len(target_uids) / 100))

    for i in range(c):
        get = requests.get(
            VK_CONFIG["domain"] + "/friends.getMutual",
            params={
                "access_token": VK_CONFIG["access_token"],
                "source_uid": source_uid,
                "target_uid": target_uid,
                "target_uids": target_uids,
                "order": order,
                "count": count,
                "offset": i * 100,
                "v": VK_CONFIG["version"],
            },
        )
        response = get.json()["response"]
        mutual_friends += response

        time.sleep(0.34)

    return mutual_friends
