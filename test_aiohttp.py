import aiohttp
import json
import asyncio

from pydantic import BaseModel

class ResponseModel(BaseModel):
    Name: str

async def call(url):

    url = f"http://127.0.0.1:8999/{url}"

    print("Calling URL:", url)
    try:
        async with aiohttp.ClientSession() as session:

            async with session.get(url=url) as response:
                print(f"No exception, status: {response.status}")
                response_json = await response.json()
                print(f"Response: {json.dumps(response_json, indent=2)}")
                ResponseModel.model_validate(response_json)
    except Exception as e:
        print(f"\033[91mError during response handling: {e}\033[0m")

    print()


async def main():

    await call("")

    await call("model_not_valid")

    await call("malformed_json")

    await call("raise_exception")


if __name__ == "__main__":
    asyncio.run(main())
