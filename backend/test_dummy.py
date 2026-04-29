import asyncio
from openai import AsyncOpenAI

async def test():
    client = AsyncOpenAI(
        base_url="https://integrate.api.nvidia.com/v1",
        api_key="dummy-key"
    )
    
    try:
        resp = await client.chat.completions.create(
            model="meta/llama-3.1-70b-instruct",
            messages=[{"role": "user", "content": "Hello, output JSON please."}],
            response_format={"type": "json_object"}
        )
        print("Success:", resp.choices[0].message.content)
    except Exception as e:
        print(f"Error type: {type(e).__name__}")
        print(f"Error msg: {e}")

asyncio.run(test())
