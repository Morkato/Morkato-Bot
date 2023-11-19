from datetime import datetime
from dataclasses import dataclass

from .abc import (
  Snowflake as ObjectSnowflake,

  WORKER,
  BITS,
  SEQUENCE,
  EPOCH
)

class Snowflake:
  def __init__(self, worker: int = WORKER, bits: int = BITS, seq: int = SEQUENCE, epoch: int = EPOCH) -> None:
    self.worker = worker
    self.bits   = bits
    self.seq    = seq

    self.epoch = epoch if not epoch == -1 else datetime.now().timestamp() * 1000

  def generate(self) -> int:
    timestamp = int((datetime.now().timestamp() * 1000 - self.epoch))

    return (timestamp << (self.bits + self.seq)) | (self.worker << self.seq)

  def created_at(self, obj: ObjectSnowflake) -> datetime:
    timestamp = (obj.id >> (self.bits + self.seq)) + self.epoch

    return datetime.fromtimestamp(timestamp / 1000)

snowflake = Snowflake()

def generate() -> int:
  return snowflake.generate()

def created_at(snow: ObjectSnowflake) -> datetime:
  return snowflake.created_at(snow)

@dataclass
class Object(ObjectSnowflake):
  id: int
