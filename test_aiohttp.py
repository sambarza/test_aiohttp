import aiohttp
import asyncio

from pydantic import BaseModel
from dataclasses import dataclass, field

import traceback

def set_color(status: str) -> str:
    if status == "OK":
        print("\033[92m")  # Green
    else:
        print("\033[91m")  # Red


def reset_color() -> str:
    print("\033[0m")  # Reset to default color


class ResponseModel(BaseModel):
    MyName: str


@dataclass
class Body:
    initialization = ""
    confirmation = ""

    def __str__(self):
        return f"Initialization: [{self.initialization}], Confirmation: [{self.confirmation}]"


@dataclass
class ProcessInfo:

    url = ""
    request_body: Body = field(default_factory=Body)
    response_body: Body = field(default_factory=Body)
    initialization_response = None
    confirmation_response = None
    error: str = ""
    status = ""
    the_name = ""


def log_start(url, scenario):
    print("\033[96m")  # blue
    print("---------------------------------------------")
    print(f"{scenario}")
    print("---------------------------------------------")
    print("\033[3m" + f"{url}" + "\033[0m")  # Italic
    reset_color()


def save_result(process_info: ProcessInfo):
    set_color(process_info.status)

    print(f"Process result:")
    print(f"Status:         \t {process_info.status}")
    print(f"Url:            \t {process_info.url}")
    print(f"Request body:   \t {process_info.request_body}")
    print(f"Response body:  \t {process_info.response_body}")
    print(f"The name:       \t {process_info.the_name}")
    print()
    print(f"Error:")
    print()
    print(f"{process_info.error}")
    print()

    reset_color()


async def initialization(url, process_info: ProcessInfo):

    process_info.request_body.initialization = {"amount": 100, "currency": "EUR"}

    async with aiohttp.ClientSession() as session:
        async with session.get(url=url) as process_info.response:

            if process_info.response.status != 200:
                process_info.error = f"HTTP status {process_info.response.status} Response: {process_info.response.reason}"
                raise Exception(process_info.error)

            process_info.response_body.initialization = (
                await process_info.response.text()
            )

            process_info.initialization_response = ResponseModel.model_validate(
                await process_info.response.json()
            )

            process_info.the_name = process_info.initialization_response.MyName


async def confirm_payment(url, process_info: ProcessInfo):

    process_info.request_body.confirmation = {"dummy": "data"}

    # do something with the initialization payment, the id is here -> process_info.the_name

    process_info.response_body.confirmation = {"result": "confirmed"}


async def set_lock():
    pass


async def remove_lock():

    # THIS METHOD CANNOT RAISE EXCEPTIONS, ALL THE EXCEPTIONS MUST BE HANDLED INSIDE
    # why? because it is called inside a finally block, the payment has been already sent
    pass


async def do_job(url) -> ProcessInfo:

    process_info = ProcessInfo()

    process_info.url = url
    process_info.status = "ERROR"

    try:
        await set_lock()
        await initialization(url, process_info)
        await confirm_payment(url, process_info)

        process_info.status = "OK"

    except Exception as e:

        if process_info.error == "":
            process_info.error = str(e)

        process_info.error = traceback.format_exc(limit=5, chain=False)

    finally:
        await remove_lock()

    return process_info


async def create_payment(url, scenario) -> None:

    log_start(url, scenario)

    process_info = await do_job(url)

    save_result(process_info)


async def main():

    url = f"http://127.0.0.1:8999/"

    await create_payment(f"{url}", "Must finish without errors")

    await create_payment(
        f"{url}model_not_valid",
        "Call returned 200 but returned json model is not valid",
    )

    await create_payment(
        f"{url}malformed_json", "Call returned 200 but returned json is malformed"
    )

    await create_payment(f"{url}raise_exception", "Call returned http error 500")

    await create_payment(f"{url}wrong_path", "Call to wrong path, returned http 400")

    await create_payment(f"http://127.0.0.1:9000", "Call to wrong port")


if __name__ == "__main__":
    asyncio.run(main())
