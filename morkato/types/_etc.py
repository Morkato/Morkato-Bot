from __future__ import annotations

from typing import (
  TYPE_CHECKING,
  TypeVar
)

if TYPE_CHECKING:
  from ..bot import MorkatoBotBase, MorkatoBot, BotApp
  from ..context import AppBotContext, MorkatoContext

  BotAppT = TypeVar('BotAppT', bound='BotApp')
  MorkatoBotT = TypeVar('MorkatoBotT', bound='MorkatoBotBase')

  MorkatoContextT = TypeVar('MorkatoContextT', bound='MorkatoContext')
  AppBotContextT = TypeVar('AppBotContextT', bound='AppBotContext')

  Context = MorkatoContext[MorkatoBot]
else:
  BotAppT = TypeVar('BotAppT')
  MorkatoBotT = TypeVar('MorkatoBotT')

  MorkatoContextT = TypeVar('MorkatoContextT')
  AppBotContextT = TypeVar('AppBotContextT')

  Context = TypeVar('Context')