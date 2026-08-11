"""
ai/groq_client.py

Groq LLM Client

Creates and manages a singleton ChatGroq instance.

Responsibilities
----------------
- Validate configuration
- Create ChatGroq client
- Reuse the same client
- Hide provider-specific implementation

Author: Raman Tiwari
Project: SAP AI Test Copilot
"""

from threading import Lock

from langchain_groq import ChatGroq

from ai.config import AIConfig


class GroqClient:
    """
    Singleton wrapper around ChatGroq.
    """

    _instance = None
    _lock = Lock()

    @classmethod
    def get_llm(cls) -> ChatGroq:
        """
        Returns a singleton ChatGroq instance.
        """

        if cls._instance is None:

            with cls._lock:

                if cls._instance is None:

                    AIConfig.validate()

                    cls._instance = ChatGroq(

                        api_key=AIConfig.GROQ_API_KEY,

                        model=AIConfig.MODEL_NAME,

                        temperature=AIConfig.TEMPERATURE,

                        max_tokens=AIConfig.MAX_TOKENS,

                        timeout=AIConfig.TIMEOUT,

                        max_retries=AIConfig.MAX_RETRIES

                    )

        return cls._instance


def get_llm() -> ChatGroq:
    """
    Convenience function.

    Example
    -------
    llm = get_llm()
    """

    return GroqClient.get_llm()