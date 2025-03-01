import json
from datetime import datetime
from typing import Optional

import typer
from typing_extensions import Annotated

from readwise import get_document_by_id, get_documents, save_document

app = typer.Typer()


@app.command()
def list(
    location: Annotated[Optional[str], typer.Option("--location", "-l")] = None,
    category: Annotated[Optional[str], typer.Option("--category", "-c")] = None,
    upaded_after: Annotated[Optional[datetime], typer.Option("--updated-after", "-u")] = None,
    n: Annotated[Optional[int], typer.Option("--number", "-n")] = None,
) -> None:
    """List documents.

    Params:
        location (Optional[str]): The document's location, could be one of: new, later, shortlist, archive, feed
        category (Optional[str]): The document's category, could be one of: article, email, rss, highlight, note, pdf,
            epub, tweet, video
        upaded_after (Optional[datetime]): Filter documents updated after a certain date.
        n (Optional[int]): Limits the number of documents to a maximum (100 by default).

    Usage:
        $ readwise list new
    """
    documents = get_documents(location, category, upaded_after)[:n]
    fields_to_include = {"title", "id", "category", "author", "source", "created_at", "updated_at", "reading_progress"}
    print(json.dumps([d.dict(include=fields_to_include) for d in documents], indent=2))


@app.command()
def get(id: str) -> None:
    """Get a single document from its ID.

    Usage:
        $ readwise get <document_id>
    """
    doc = get_document_by_id(id)
    if doc:
        print(doc.json(indent=2))
    else:
        print(f"No document with ID {id!r} could be found.")


@app.command()
def save(url: str) -> None:
    """Save a document to Reader.

    Params:
        url (str): URL to the document from where it will be scraped by Readwise.

    Usage:
        $ readwise save "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
    """
    document_already_exists, document_info = save_document(url)
    if document_already_exists:
        print(f"This document has already been saved earlier with ID {document_info.id!r}.")
    else:
        print(f"Saved new document {document_info.id!r}.")
