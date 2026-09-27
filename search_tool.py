import requests
from typing import Type

from langchain_core.tools import BaseTool
from pydantic import BaseModel, Field


# Input format for the search tool
class SearchInput(BaseModel):
    query: str = Field(
        description="The search query to execute"
    )


# Search Tool
class SearchTool(BaseTool):
    name: str = "search"

    description: str = (
        "Search for current information on the internet. "
        "Use this when you need recent or specific information about a topic."
    )

    args_schema: Type[BaseModel] = SearchInput

    def _run(self, query: str) -> str:
        try:
            # DuckDuckGo Instant Answer API
            url = "https://api.duckduckgo.com/"

            params = {
                "q": query,
                "format": "json",
                "no_html": "1",
                "skip_disambig": "1"
            }

            # Send request
            response = requests.get(
                url,
                params=params,
                timeout=10
            )

            # Check for HTTP errors
            response.raise_for_status()

            # Convert response to JSON
            data = response.json()

            # Get main answer
            abstract = data.get("AbstractText")

            if abstract:
                return abstract

            # Try related topics if no abstract is available
            related_topics = data.get("RelatedTopics", [])

            results = []

            for topic in related_topics[:5]:
                if isinstance(topic, dict):
                    text = topic.get("Text")

                    if text:
                        results.append(text)

            if results:
                return "\n\n".join(results)

            return "No useful search result found."

        except requests.exceptions.Timeout:
            return "Search failed: request timed out."

        except requests.exceptions.RequestException as e:
            return f"Search failed: {str(e)}"

        except Exception as e:
            return f"Unexpected search error: {str(e)}"