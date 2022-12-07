import time
import typing as tp

import requests


class Session:
    def __init__(
        self,
        base_url: str,
        timeout: float = 5.0,
        max_retries: int = 3,
        backoff_factor: float = 0.3,
    ) -> None:
        self.base_url = base_url
        self.timeout = timeout
        self.max_retries = max_retries
        self.backoff_factor = backoff_factor

    def get(self, url: str, *args: tp.Any, **kwargs: tp.Any) -> requests.Response:
        return self.check(url, requests.get)

    def post(self, url: str, *args: tp.Any, **kwargs: tp.Any) -> requests.Response:
        return self.check(url, requests.post)

    def check(self, url: str, method):
        count = 0
        while True:
            try:
                response = method(f"{self.base_url}/{url}", timeout=self.timeout)
                response.raise_for_status()
                return response
            except requests.exceptions.HTTPError:
                if self.max_retries == 1:
                    raise requests.exceptions.HTTPError

                if count == self.max_retries:
                    raise requests.exceptions.RetryError
                sleep = round((self.backoff_factor * (2**count)))
                time.sleep(sleep)
                count += 1
            except requests.exceptions.ConnectionError:
                raise requests.exceptions.ConnectionError

            except requests.exceptions.ReadTimeout:
                raise requests.exceptions.ReadTimeout
