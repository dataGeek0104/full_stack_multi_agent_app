import os
from typing import Optional

from langchain_core.tools import Tool  # type: ignore[import-not-found]  # isort: skip
from langchain_tavily import TavilySearch  # type: ignore[import-not-found]  # isort: skip


class WebSearchTool(Tool):
    def __init__(
        self,
        topic: str,
        api_key: Optional[str] = None,
    ):
        api_key = api_key or os.getenv("TAVILY_API_KEY")
        if not api_key:
            raise ValueError("TAVILY_API_KEY environment variable is not set.")
        search = TavilySearch(
            max_results=1,
            topic=topic,
            # include_answer=False,
            # include_raw_content=False,
            include_images=True,
            include_image_descriptions=True,
            # search_depth="basic",
            # time_range="day",
            # include_domains=None,
            # exclude_domains=None
        )
        super().__init__(
            name="web_search",
            description="Use this tool to search the web using Tavily Search. Provide a query to get results.",
            func=search.invoke,
        )
