import datetime as dt
import statistics
import typing as tp

from vkapi.friends import get_friends


def age_predict(user_id: int) -> tp.Optional[float]:
    year = dt.datetime.now().year
    friends_response = get_friends(user_id).items
    friends_age = []
    for friend in friends_response:
        try:
            friends_age.append(year - int(friend["bdate"][5:]))
        except:
            pass

    return statistics.median(friends_age) if friends_age else None
