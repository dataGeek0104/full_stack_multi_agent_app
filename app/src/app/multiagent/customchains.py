from typing import Optional

from .llm import LLMFactory

from langchain_core.output_parsers import StrOutputParser  # type: ignore[import-not-found]  # isort: skip
from langchain_core.prompts import ChatPromptTemplate  # type: ignore[import-not-found]  # isort: skip


class SimpleLLMChain:
    def __init__(
        self,
        model_provider: str,
        sys_prompt: str,
        model: Optional[str] = None,
        api_key: Optional[str] = None,
    ):
        self.llm = LLMFactory.get_model(
            model_provider=model_provider, model=model, api_key=api_key
        )
        self.prompt = ChatPromptTemplate.from_messages(
            [
                ("system", sys_prompt),
                ("human", "{question}"),
            ]
        )
        self.output_parser = StrOutputParser()
        self.runnable = self.prompt | self.llm | self.output_parser

    def invoke(self, question: str) -> str:
        return self.runnable.invoke({"question": question})
