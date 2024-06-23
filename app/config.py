from enum import Enum

import chromadb

THRESHOLD: float = 0.3


class ChromaCredentials(Enum):
    HOST: str = '192.168.0.100'
    PORT: int = 8090
    SSL: bool = False
    SETTINGS = chromadb.Settings()
