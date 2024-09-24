class AppError(Exception):
  def __init__(self, message: str) -> None:
    self.message = message
class ArtNotFoundError(AppError):
  def __init__(self, art_name: str) -> None:
    super().__init__("A arte (Respiration, Kekkijutsu ou Estilo de Luta): **`%s`** não existe." % art_name)
class AttackNotFoundERROR(AppError):
  pass