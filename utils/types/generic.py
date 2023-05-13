from typing import Literal, Union, Dict, List

JsonObjects = Union[str, int, bool, float, Literal[None], list, dict]
Json = Union[Dict[str, JsonObjects], List[JsonObjects]]

Headers = Dict[
  Literal[
  "host",
  "user-agent",
  "accept",
  "accept-language",
  "accept-encoding",
  "referer",
  "connection",
  "upgrade-insecure-requests",
  "if-modified-since",
  "if-none-match",
  "cache-control",

  "x-access-control",
  "authorization"
], str]

