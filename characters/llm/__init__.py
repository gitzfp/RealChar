import os
from functools import cache

from dotenv import load_dotenv
from langchain.chat_models.base import BaseChatModel

from characters.llm.base import LLM


load_dotenv()


def get_llm(model="gpt-3.5-turbo-16k") -> LLM:
    model = os.getenv("LLM_MODEL_USE", model)

    if model.startswith("qwen"):
        from characters.llm.qwen_llm import TongyiLlm

        return TongyiLlm(model=model)

    if model.startswith("gpt"):
        from characters.llm.openai_llm import OpenaiLlm

        return OpenaiLlm(model=model)
    elif model.startswith("claude"):
        from characters.llm.anthropic_llm import AnthropicLlm

        return AnthropicLlm(model=model)
    elif "localhost" in model:
        # Currently use llama2-wrapper to run local llama models
        local_llm_url = os.getenv("LOCAL_LLM_URL", "")
        if local_llm_url:
            from characters.llm.local_llm import LocalLlm

            return LocalLlm(url=local_llm_url)
        else:
            raise ValueError("LOCAL_LLM_URL not set")
    elif "llama" in model:
        # Currently use Anyscale to support llama models
        from characters.llm.anyscale_llm import AnysacleLlm

        return AnysacleLlm(model=model)
    elif "rebyte" in model:
        from characters.llm.rebyte_llm import RebyteLlm

        return RebyteLlm()
    else:
        raise ValueError(f"Invalid llm model: {model}")


def get_chat_model(model="gpt-3.5-turbo-16k") -> BaseChatModel:
    model = os.getenv("LLM_MODEL_USE", model)
    if model.startswith("qwen"):
        # TODO
        from characters.llm.qwen_llm import TongyiLlm

        return TongyiLlm(model=model).chat_tongyi
    if model.startswith("gpt"):
        from characters.llm.openai_llm import OpenaiLlm

        return OpenaiLlm(model=model).chat_open_ai
    elif model.startswith("claude"):
        from characters.llm.anthropic_llm import AnthropicLlm

        return AnthropicLlm(model=model).chat_anthropic
    elif "localhost" in model:
        # Currently use llama2-wrapper to run local llama models
        local_llm_url = os.getenv("LOCAL_LLM_URL", "")
        if local_llm_url:
            from characters.llm.local_llm import LocalLlm

            return LocalLlm(url=local_llm_url).chat_open_ai
        else:
            raise ValueError("LOCAL_LLM_URL not set")
    elif "llama" in model:
        # Currently use Anyscale to support llama models
        from characters.llm.anyscale_llm import AnysacleLlm

        return AnysacleLlm(model=model).chat_open_ai
    elif "rebyte" in model:
        from characters.llm.rebyte_llm import RebyteLlm

        return RebyteLlm().chat_rebyte
    else:
        raise ValueError(f"Invalid llm model: {model}")


@cache
def get_chat_model_from_env() -> BaseChatModel:
    """GPT-4 has the best performance while generating system prompt."""

    if os.getenv("REBYTE_API_KEY"):
        return get_chat_model(model="rebyte")
    elif os.getenv("OPENAI_API_KEY"):
        return get_chat_model(model="gpt-4")
    elif os.getenv("ANTHROPIC_API_KEY"):
        return get_chat_model(model="claude-2")
    elif os.getenv("ANYSCALE_API_KEY"):
        return get_chat_model(model="meta-llama/Llama-2-70b-chat-hf")
    elif os.getenv("LOCAL_LLM_URL"):
        return get_chat_model(model="localhost")
    elif os.getenv("DASHSCOPE_API_KEY"):
        return get_chat_model(model="qwen-max")

    raise ValueError("No llm api key found in env")
