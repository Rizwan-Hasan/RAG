from io import BytesIO
from typing import List

import uvicorn
from PyPDF2 import PdfReader
from fastapi import FastAPI, UploadFile, File, Form
from langchain_chroma import Chroma
from langchain_core.documents import Document

import config
from event import lifespan_event
from global_vars import GlobalVars

app = FastAPI(title='RAG', lifespan=lifespan_event)


@app.on_event("shutdown")
async def shutdown_event():
    # Assuming chroma_client has a close method to close the connection
    pass


@app.post('/upload-file')
async def upload_file(pdf_files: List[UploadFile] = File(...), collection_name: str = Form(...)):
    for file in pdf_files:
        pdf = PdfReader(BytesIO(await file.read()))
        content = ' '.join(page.extract_text() for page in pdf.pages)
        documents = GlobalVars.text_splitter.split_documents([Document(page_content=content)])

        vector_store = Chroma.from_documents(
            client=GlobalVars.chroma_client,
            client_settings=config.ChromaCredentials.SETTINGS.value,
            documents=documents,
            embedding=GlobalVars.embedding_func,
            collection_name=collection_name,
            collection_metadata={'hnsw:space': 'cosine'}
        )

    return {
        'status': True,
        'message': 'File uploaded successfully'
    }


@app.post('/query')
async def query(question: str = Form(...), collection_name: str = Form(...)):
    collection = Chroma(
        client=GlobalVars.chroma_client,
        client_settings=config.ChromaCredentials.SETTINGS.value,
        embedding_function=GlobalVars.embedding_func,
        collection_name=collection_name,
        create_collection_if_not_exists=False
    )
    docs = collection.similarity_search_with_relevance_scores(
        query=question, k=4,
        score_threshold=config.THRESHOLD
    )

    return {
        'status': True,
        'documents': [dict(content=doc[0].page_content, score=doc[1]) for doc in docs]
    }


@app.delete("/delete")
async def delete(collection_name: str = Form(...)):
    try:
        GlobalVars.chroma_client.delete_collection(collection_name)
        return {
            'status': True,
            'message': 'Collection deleted'
        }
    except Exception as ex:
        return {
            'status': False,
            'message': str(ex)
        }


if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port=8001, loop='asyncio', log_level="info")
