from api.models.geomap import ArialInMap, ChannelGeomap, PlaceInMap, TypePlace, WhatTodo
from django.urls import reverse
from rest_framework.test import APIClient, APITestCase


class PlaceTests(APITestCase):
    def setUp(self):
        self.client = APIClient()

        self.arial_in_map = ArialInMap.objects.create(
            name="Test ArialInMap",
        )

        self.channel_geomap = ChannelGeomap.objects.create(
            name="Test ChannelGeomap",
            arial_in_map=self.arial_in_map,
            shard=1,
        )

        self.what_todo = WhatTodo.objects.create(todo="Test WhatTodo")

        self.type_place = TypePlace.objects.create(
            name="Test TypePlace",
            img_url="https://example.com/image.jpg",
            img_size_w=1.0,
            img_size_h=1.0,
        )

        self.place_in_map = PlaceInMap.objects.create(
            simpl_name="Test PlaceInMap",
            cord_x="10",
            cord_y="20",
            rating=5,
            address="123 Test St",
            channel_geomap=self.channel_geomap,
            type_place=self.type_place,
        )

        self.place_in_map.what_todo.add(self.what_todo)

    def test_place_detail(self):
        except_data = {
            "id": str(self.place_in_map.id),
            "self_url": f"http://testserver/api/v1/place/{self.place_in_map.id}/",
            "cord_x": self.place_in_map.cord_x,
            "cord_y": self.place_in_map.cord_y,
            "simpl_name": self.place_in_map.simpl_name,
            "rating": self.place_in_map.rating,
            "address": self.place_in_map.address,
            "channel_geomap": self.channel_geomap.id,
            "channel_geomap_obj": {
                "id": self.channel_geomap.id,
                "self_url": f"http://testserver/api/v1/channel_geomap/{self.channel_geomap.id}/",
                "name": self.channel_geomap.name,
                "arial_in_map": self.arial_in_map.id,
                "arial_in_map_obj": {
                    "id": self.arial_in_map.id,
                    "self_url": f"http://testserver/api/v1/arial_in_map/{self.arial_in_map.id}/",
                    "name": self.arial_in_map.name,
                },
                "shard": self.channel_geomap.shard,
                "default_coord_x": "",
                "default_coord_y": "",
            },
            "what_todo": [self.what_todo.id],
            "what_todo_obj": [
                {
                    "id": self.what_todo.id,
                    "self_url": f"http://testserver/api/v1/what_todo/{self.what_todo.id}/",
                    "todo": self.what_todo.todo,
                }
            ],
            "type_place": self.type_place.id,
            "type_place_obj": {
                "id": self.type_place.id,
                "self_url": f"http://testserver/api/v1/type_place/{self.type_place.id}/",
                "name": self.type_place.name,
                "img_url": self.type_place.img_url,
                "img_size_w": self.type_place.img_size_w,
                "img_size_h": self.type_place.img_size_h,
            },
        }
        url = reverse("place-detail", kwargs={"pk": str(self.place_in_map.id)})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), except_data)

    def test_channel_geomap_place_detail(self):
        except_data = {
            "id": self.channel_geomap.id,
            "self_url": f"http://testserver/api/v1/channel_geomap_place/{self.channel_geomap.id}/",
            "name": self.channel_geomap.name,
            "arial_in_map": self.arial_in_map.id,
            "arial_in_map_obj": {
                "id": self.arial_in_map.id,
                "self_url": f"http://testserver/api/v1/arial_in_map/{self.arial_in_map.id}/",
                "name": self.arial_in_map.name,
            },
            "shard": self.channel_geomap.shard,
            "places": {
                "place": {
                    str(self.type_place.id): [
                        {
                            "id": str(self.place_in_map.id),
                            "self_url": f"http://testserver/api/v1/place/{self.place_in_map.id}/",
                            "cord_x": self.place_in_map.cord_x,
                            "cord_y": self.place_in_map.cord_y,
                            "simpl_name": self.place_in_map.simpl_name,
                            "rating": self.place_in_map.rating,
                            "address": self.place_in_map.address,
                            "what_todo_obj": [
                                {
                                    "id": self.what_todo.id,
                                    "self_url": f"http://testserver/api/v1/what_todo/{self.what_todo.id}/",
                                    "todo": self.what_todo.todo,
                                }
                            ],
                            "type_place": self.type_place.id,
                        }
                    ]
                },
                "settings": {
                    str(self.type_place.id): {
                        "id": self.type_place.id,
                        "self_url": f"http://testserver/api/v1/type_place/{self.type_place.id}/",
                        "name": self.type_place.name,
                        "img_url": self.type_place.img_url,
                        "img_size_w": self.type_place.img_size_w,
                        "img_size_h": self.type_place.img_size_h,
                    }
                },
            },
            "default_coord_x": "",
            "default_coord_y": "",
        }
        url = reverse(
            "channel_geomap_place-detail", kwargs={"pk": str(self.channel_geomap.id)}
        )
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), except_data)
