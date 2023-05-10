import requests


def get_address_from_coord(lat: str, lon: str) -> tuple[bool, str]:
    """Получить адресс по координатам"""
    url = (
        f"https://nominatim.openstreetmap.org/reverse?format=jsonv2&lat={lat}&lon={lon}"
    )

    try:
        response = requests.get(url)
        response.raise_for_status()

        data = response.json()
        address = data["display_name"]
        return (True, address)

    except requests.exceptions.HTTPError as e:
        return (False, e)
