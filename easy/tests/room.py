from django.test import TestCase
from django.db import models
from easy.models import Rooms


class RoomTestcase(TestCase):
    def setUp(self):
        Rooms.objects.create(
            room_number="101",
            square_meter=13.1,
            price=105,
            floor=2,
            single_bed=True,
            double_bed=True,
        )

    def test_room_entities(self):
        """Room entity test"""
        room = Rooms.objects.get(room_number="101")
        self.assertEqual(room.room_number, '101')
        self.assertEqual(room.square_meter, 13.1)
        self.assertEqual(room.price, 105.0)
        self.assertEqual(room.floor, 2)
        self.assertEqual(room.single_bed, 1)
        self.assertEqual(room.double_bed, 1)
        self.assertEqual(room.child_bed, 0)