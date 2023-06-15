# import asyncio
# import aiohttp
# from django_setup import *
# from asgiref.sync import sync_to_async
#
# from app.models import Car
#
#
# async def fetch_data(url):
#     async with aiohttp.ClientSession() as session:
#         async with session.get(url) as response:
#             return await response.json()
#
#
# async def save_car_to_database(data):
#     car = await sync_to_async(Vehicle.objects.create)(
#         vehicle_type="Car/Truck" if data[0]["type"] == 3 else "Motorcycle",
#         vehicle_year=data[0]["year"],
#         vehicle_make=data[0]["make"],
#         vehicle_model=data[0]["model"],
#         vehicle_engine=data[0]["engine"],
#     )
#     await sync_to_async(car.save)()
#
#
# async def get_final_endpoint():
#     types_endpoint = "https://shop.advanceautoparts.com/capi/v29/vehicles/types"
#     years_endpoints = {
#         "car/truck": "https://shop.advanceautoparts.com/capi/v29/vehicles/years?type=3",
#         "motorcycle": "https://shop.advanceautoparts.com/capi/v29/vehicles/years?type=6",
#     }
#
#     async with aiohttp.ClientSession() as session:
#         types_response = await session.get(types_endpoint)
#         types_data = await types_response.json()
#
#         for type_data in types_data:
#             type_id = type_data["id"]
#             type_name = type_data["name"]
#
#             years_endpoint = years_endpoints[type_name.lower()]
#             years_response = await session.get(years_endpoint)
#             years_data = await years_response.json()
#
#             for year in years_data:
#                 makes_endpoint = (f"https://shop.advanceautoparts.com/"
#                                   f"capi/v29/vehicles/makes?type={type_id}&year={year}")
#                 makes_response = await session.get(makes_endpoint)
#                 makes_data = await makes_response.json()
#
#                 for make in makes_data:
#                     models_endpoint = (f"https://shop.advanceautoparts.com/capi/v29/vehicles/models?"
#                                        f"type={type_id}&year={year}&make={make.replace(' ', '+')}")
#                     models_response = await session.get(models_endpoint)
#                     models_data = await models_response.json()
#
#                     for model in models_data:
#                         final_endpoint = (f"https://shop.advanceautoparts.com/capi/v29/vehicles?type="
#                                           f"{type_id}&year={year}&make={make.replace(' ', '+')}"
#                                           f"&model={model.replace(' ', '+')}")
#                         data = await fetch_data(final_endpoint)
#                         await save_car_to_database(data)
#
#
# asyncio.run(get_final_endpoint())
import requests
from django_setup import *
from app.models import Vehicle


def fetch_data(url):
    response = requests.get(url)
    return response.json()


def save_car_to_database(data):
    car = Vehicle.objects.create(
        vehicle_type="Car/Truck" if data[0]["type"] == 3 else "Motorcycle",
        vehicle_year=data[0]["year"],
        vehicle_make=data[0]["make"],
        vehicle_model=data[0]["model"],
        vehicle_engine=data[0]["engine"],
    )
    car.save()


def get_final_endpoint():
    types_endpoint = "https://shop.advanceautoparts.com/capi/v29/vehicles/types"
    years_endpoints = {
        "car/truck": "https://shop.advanceautoparts.com/capi/v29/vehicles/years?type=3",
        "motorcycle": "https://shop.advanceautoparts.com/capi/v29/vehicles/years?type=6",
    }

    types_response = requests.get(types_endpoint)
    types_data = types_response.json()

    for type_data in types_data:
        type_id = type_data["id"]
        type_name = type_data["name"]

        years_endpoint = years_endpoints[type_name.lower()]
        years_response = requests.get(years_endpoint)
        years_data = years_response.json()

        for year in years_data:
            makes_endpoint = (f"https://shop.advanceautoparts.com/"
                              f"capi/v29/vehicles/makes?type={type_id}&year={year}")
            makes_response = requests.get(makes_endpoint)
            makes_data = makes_response.json()

            for make in makes_data:
                models_endpoint = (f"https://shop.advanceautoparts.com/capi/v29/vehicles/models?"
                                   f"type={type_id}&year={year}&make={make.replace(' ', '+')}")
                models_response = requests.get(models_endpoint)
                models_data = models_response.json()

                for model in models_data:
                    final_endpoint = (f"https://shop.advanceautoparts.com/capi/v29/vehicles?type="
                                      f"{type_id}&year={year}&make={make.replace(' ', '+')}"
                                      f"&model={model.replace(' ', '+')}")
                    data = fetch_data(final_endpoint)
                    save_car_to_database(data)


get_final_endpoint()

