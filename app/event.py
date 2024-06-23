from contextlib import asynccontextmanager

import chromadb
from fastapi import FastAPI
from langchain_community.embeddings import HuggingFaceBgeEmbeddings
from langchain_experimental.text_splitter import SemanticChunker

import config
from global_vars import GlobalVars


@asynccontextmanager
async def lifespan_event(app: FastAPI):
    GlobalVars.chroma_client = chromadb.HttpClient(
        host=config.ChromaCredentials.HOST.value,
        port=config.ChromaCredentials.PORT.value,
        ssl=config.ChromaCredentials.SSL.value,
        settings=config.ChromaCredentials.SETTINGS.value)

    GlobalVars.embedding_func = HuggingFaceBgeEmbeddings(
        model_name='BAAI/bge-base-en-v1.5',
        model_kwargs={'device': 'cuda'},
        encode_kwargs={'normalize_embeddings': True})

    GlobalVars.text_splitter = SemanticChunker(GlobalVars.embedding_func, breakpoint_threshold_type="percentile")

    yield

    pass
