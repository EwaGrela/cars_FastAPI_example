import requests

# helper function which checks for data validity in external API


def get_external_data(provided_data):
    url = 'https://vpic.nhtsa.dot.gov/api/vehicles/GetModelsForMake/{}?format=json'.format(
        provided_data["make"])
    cars_in_ext_api = requests.get(url).json()['Results']
    found_item = [
        item for item in cars_in_ext_api if item['Model_Name'] == provided_data["model"]]
    return found_item
