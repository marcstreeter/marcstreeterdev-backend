import time
import asyncio
from openai import AsyncOpenAI
from anthropic import AsyncAnthropic
from .schemas import LLMRequest, MultiTestResponse, ProviderResult, ProviderStatus
from core.settings import settings


async def _call_openai(prompt: str, timeout: int) -> ProviderResult:
    """Call OpenAI API"""
    if not settings.openai_api_key:
        return ProviderResult(
            provider="openai",
            status=ProviderStatus.NO_CONFIG,
            prompt=prompt,
            output=""
        )
    t0 = time.perf_counter()
    try:
        client = AsyncOpenAI(api_key=settings.openai_api_key)
        response = await client.chat.completions.create(
            model=settings.openai_model,
            messages=[{"role": "user", "content": prompt}],
            timeout=timeout
        )
        elapsed = time.perf_counter() - t0
        return ProviderResult(
            provider="openai",
            elapsed=elapsed,
            output=str(response),
            prompt=prompt,
            status=ProviderStatus.OK
        )
    except Exception as e:
        elapsed = time.perf_counter() - t0
        return ProviderResult(
            provider="openai",
            elapsed=elapsed,
            output=str(e),
            prompt=prompt,
            status=ProviderStatus.FAILED
        )


async def _call_anthropic(prompt: str, timeout: int) -> ProviderResult:
    """Call Anthropic API"""
    if not settings.anthropic_api_key:
        return ProviderResult(
            provider="anthropic",
            status=ProviderStatus.NO_CONFIG,
            prompt=prompt,
            output=""
        )
    t0 = time.perf_counter()
    try:
        client = AsyncAnthropic(api_key=settings.anthropic_api_key)
        response = await client.messages.create(
            model=settings.anthropic_model,
            max_tokens=256,
            messages=[{"role": "user", "content": prompt}],
            timeout=timeout
        )
        elapsed = time.perf_counter() - t0
        return ProviderResult(
            provider="anthropic",
            elapsed=elapsed,
            output=str(response),
            prompt=prompt,
            status=ProviderStatus.OK
        )
    except Exception as e:
        elapsed = time.perf_counter() - t0
        return ProviderResult(
            provider="anthropic",
            elapsed=elapsed,
            output=str(e),
            prompt=prompt,
            status=ProviderStatus.FAILED
        )


async def _call_google(prompt: str, timeout: int) -> ProviderResult:
    """Call Google Gemini API"""
    if not settings.google_api_key:
        return ProviderResult(
            provider="google",
            status=ProviderStatus.NO_CONFIG,
            prompt=prompt,
            output=""
        )
    t0 = time.perf_counter()
    try:
        client = AsyncOpenAI(
            api_key=settings.google_api_key,
            base_url=settings.google_api_url
        )
        response = await client.chat.completions.create(
            model="gemini-pro",
            messages=[{"role": "user", "content": prompt}],
            timeout=timeout
        )
        elapsed = time.perf_counter() - t0
        return ProviderResult(
            provider="google",
            elapsed=elapsed,
            output=str(response),
            prompt=prompt,
            status=ProviderStatus.OK
        )
    except Exception as e:
        elapsed = time.perf_counter() - t0
        return ProviderResult(
            provider="google",
            elapsed=elapsed,
            output=str(e),
            prompt=prompt,
            status=ProviderStatus.FAILED
        )


async def _call_deepseek(prompt: str, timeout: int) -> ProviderResult:
    """Call DeepSeek API"""
    if not settings.deepseek_api_key:
        return ProviderResult(
            provider="deepseek",
            status=ProviderStatus.NO_CONFIG,
            prompt=prompt,
            output=""
        )
    t0 = time.perf_counter()
    try:
        client = AsyncOpenAI(
            api_key=settings.deepseek_api_key,
            base_url=settings.deepseek_api_url
        )
        response = await client.chat.completions.create(
            model=settings.deepseek_model,
            messages=[{"role": "user", "content": prompt}],
            timeout=timeout
        )
        elapsed = time.perf_counter() - t0
        return ProviderResult(
            provider="deepseek",
            elapsed=elapsed,
            output=str(response),
            prompt=prompt,
            status=ProviderStatus.OK
        )
    except Exception as e:
        elapsed = time.perf_counter() - t0
        return ProviderResult(
            provider="deepseek",
            elapsed=elapsed,
            output=str(e),
            prompt=prompt,
            status=ProviderStatus.FAILED
        )


async def _call_groq(prompt: str, timeout: int) -> ProviderResult:
    """Call Groq API"""
    if not settings.groq_api_key:
        return ProviderResult(
            provider="groq",
            status=ProviderStatus.NO_CONFIG,
            prompt=prompt,
            output=""
        )
    t0 = time.perf_counter()
    try:
        client = AsyncOpenAI(
            api_key=settings.groq_api_key,
            base_url="https://api.groq.com/openai/v1"
        )
        response = await client.chat.completions.create(
            model="llama3-8b-8192",
            messages=[{"role": "user", "content": prompt}],
            timeout=timeout
        )
        elapsed = time.perf_counter() - t0
        return ProviderResult(
            provider="groq",
            elapsed=elapsed,
            output=str(response),
            prompt=prompt,
            status=ProviderStatus.OK
        )
    except Exception as e:
        elapsed = time.perf_counter() - t0
        return ProviderResult(
            provider="groq",
            elapsed=elapsed,
            output=str(e),
            prompt=prompt,
            status=ProviderStatus.FAILED
        )


async def run_llm_test(req: LLMRequest) -> MultiTestResponse:
    """Run LLM multi-provider test"""
    prompt = req.prompt or "give me the name of the main villain's cat in the show the smurfs"
    timeout = settings.llm_timeout

    # Define provider functions
    provider_functions = [
        _call_openai,
        _call_anthropic,
        _call_google,
        _call_deepseek,
        _call_groq
    ]
    
    # Create coroutines for all providers
    coros = [func(prompt, timeout) for func in provider_functions]
    
    try:
        responses = await asyncio.wait_for(asyncio.gather(*coros), timeout=timeout)
    except asyncio.TimeoutError:
        responses = []
        provider_names = ["openai", "anthropic", "google", "deepseek", "groq"]
        for provider_name in provider_names:
            responses.append(ProviderResult(
                provider=provider_name,
                elapsed=timeout,
                output="Timed out after 30s",
                prompt=prompt,
                status=ProviderStatus.TIMEOUT
            ))
    
    return MultiTestResponse(results=responses)
