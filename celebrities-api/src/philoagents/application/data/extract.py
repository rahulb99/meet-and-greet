from typing import Generator

from langchain_community.document_loaders import WebBaseLoader, WikipediaLoader
from langchain_core.documents import Document
from tqdm import tqdm

from philoagents.domain.celeb import Celeb, CelebExtract
from philoagents.domain.celeb_factory import CelebFactory


def get_extraction_generator(
    celebs: list[CelebExtract],
) -> Generator[tuple[Celeb, list[Document]], None, None]:
    """Extract documents for a list of celebs, yielding one at a time.

    Args:
        celebs: A list of CelebExtract objects containing celeb information.

    Yields:
        tuple[Celeb, list[Document]]: A tuple containing the celeb object and a list of
            documents extracted for that celeb.
    """

    progress_bar = tqdm(
        celebs,
        desc="Extracting docs",
        unit="celeb",
        bar_format="{desc}: {percentage:3.0f}%|{bar}| {n_fmt}/{total_fmt} [{elapsed}<{remaining}, {rate_fmt}] {postfix}",
        ncols=100,
        position=0,
        leave=True,
    )

    celebs_factory = CelebFactory()
    for celeb_extract in progress_bar:
        celeb = celebs_factory.get_celeb(celeb_extract.id)
        progress_bar.set_postfix_str(f"Celeb: {celeb.name}")

        celeb_docs = extract(celeb, celeb_extract.urls)

        yield (celeb, celeb_docs)


def extract(celeb: Celeb, extract_urls: list[str]) -> list[Document]:
    """Extract documents for a single celeb from all sources and deduplicate them.

    Args:
        celeb: Celeb object containing celeb information.
        extract_urls: List of URLs to extract content from.

    Returns:
        list[Document]: List of deduplicated documents extracted for the celeb.
    """

    docs = []

    docs.extend(extract_wikipedia(celeb))
    docs.extend(extract_brittanica(celeb, extract_urls))

    return docs


def extract_wikipedia(celeb: Celeb) -> list[Document]:
    """Extract documents for a single celeb from Wikipedia.

    Args:
        celeb: Celeb object containing celeb information.

    Returns:
        list[Document]: List of documents extracted from Wikipedia for the celeb.
    """

    loader = WikipediaLoader(
        query=celeb.name,
        lang="en",
        load_max_docs=1,
        doc_content_chars_max=1000000,
    )
    docs = loader.load()

    for doc in docs:
        doc.metadata["celeb_id"] = celeb.id
        doc.metadata["celeb_name"] = celeb.name

    return docs


def extract_brittanica(celeb: Celeb, urls: list[str]) -> list[Document]:
    """Extract documents for a single celeb from Stanford Encyclopedia of Philosophy.

    Args:
        celeb: Celeb object containing celeb information.
        urls: List of URLs to extract content from.

    Returns:
        list[Document]: List of documents extracted from Stanford Encyclopedia for the celeb.
    """

    def extract_paragraphs_and_headers(soup) -> str:
        content = []
        for element in soup.find_all("p.topic-paragraph"):
            content.append(element.get_text())

        return "\n\n".join(content)

    if len(urls) == 0:
        return []

    loader = WebBaseLoader(show_progress=False)
    soups = loader.scrape_all(urls)

    documents = []
    for url, soup in zip(urls, soups):
        text = extract_paragraphs_and_headers(soup)
        metadata = {
            "source": url,
            "celeb_id": celeb.id,
            "celeb_name": celeb.name,
        }

        if title := soup.find("title"):
            metadata["title"] = title.get_text().strip(" \n")

        documents.append(Document(page_content=text, metadata=metadata))

    return documents


if __name__ == "__main__":
    trump = CelebFactory().get_celeb("trump")
    docs = extract_brittanica(
        trump,
        [
            "https://www.britannica.com/biography/Donald-Trump",
            "https://www.britannica.com/biography/Donald-Trump",
        ],
    )
    print(docs)
