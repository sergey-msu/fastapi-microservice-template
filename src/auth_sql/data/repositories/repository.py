from utils.logging import LogMixin
from data import repositories


class Repository(LogMixin):
    def __init__(
        self,
        tokens: repositories.TokensRepository,
        # other repos ...
        **kwargs
    ):
        super().__init__(**kwargs)

        self.tokens = tokens
        # other repos ...
