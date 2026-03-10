from contextlib import nullcontext
from datetime import date, time
from unittest.mock import MagicMock, patch

from django.test import SimpleTestCase

from .models import Client
import logging

logger = logging.getLogger(__name__)



class ClientManualSortieTests(SimpleTestCase):
	@patch("client.models.transaction.atomic", return_value=nullcontext())
	@patch("client.models.Presence.objects.select_for_update")
	def test_manual_sortie_persists_sortie_and_deducts_time(
		self, select_for_update_mock, _atomic_mock
	):
		client = Client(id="C0001", first_name="John", blood="A+")

		abc = MagicMock()
		abc.is_time_volume.return_value = True
		abc.presence_quantity = 120

		presence = MagicMock()
		presence.hour_entree = time(10, 0, 0)
		presence.date = date(2026, 3, 10)
		presence.abc = abc
		presence.get_time_consumed.return_value = 45

		queryset = MagicMock()
		queryset.first.return_value = presence
		select_for_update_mock.return_value.filter.return_value = queryset

		result = client.init_output_sortie_manuelle("10:45:00")

		self.assertTrue(result)
		self.assertEqual(presence.hour_sortie, time(10, 45, 0))
		presence.save.assert_called_once_with(update_fields=["hour_sortie", "updated"])
		presence.get_time_consumed.assert_called_once_with(sortie=time(10, 45, 0))
		self.assertEqual(abc.presence_quantity, 75)
		abc.save.assert_called_once_with(update_fields=["presence_quantity"])

	@patch("client.models.transaction.atomic", return_value=nullcontext())
	@patch("client.models.Presence.objects.select_for_update")
	def test_manual_sortie_handles_midnight_wraparound(
		self, select_for_update_mock, _atomic_mock
	):
		client = Client(id="C0002", first_name="Jane", blood="B+")

		abc = MagicMock()
		abc.is_time_volume.return_value = True
		abc.presence_quantity = 60

		presence = MagicMock()
		presence.hour_entree = time(23, 55, 0)
		presence.date = date(2026, 3, 10)
		presence.abc = abc
		presence.get_time_consumed.return_value = 20

		queryset = MagicMock()
		queryset.first.return_value = presence
		select_for_update_mock.return_value.filter.return_value = queryset

		result = client.init_output_sortie_manuelle("00:15:00")

		self.assertTrue(result)
		self.assertEqual(presence.hour_sortie, time(0, 15, 0))
		presence.get_time_consumed.assert_called_once_with(sortie=time(0, 15, 0))
		self.assertEqual(abc.presence_quantity, 40)

	@patch("client.models.transaction.atomic", return_value=nullcontext())
	@patch("client.models.Presence.objects.select_for_update")
	def test_manual_sortie_rejects_too_short_duration(
		self, select_for_update_mock, _atomic_mock
	):
		client = Client(id="C0003", first_name="Ali", blood="O+")

		abc = MagicMock()
		abc.is_time_volume.return_value = True
		abc.presence_quantity = 90

		presence = MagicMock()
		presence.hour_entree = time(10, 0, 0)
		presence.date = date(2026, 3, 10)
		presence.abc = abc

		queryset = MagicMock()
		queryset.first.return_value = presence
		select_for_update_mock.return_value.filter.return_value = queryset

		result = client.init_output_sortie_manuelle("10:00:01")

		self.assertFalse(result)
		presence.save.assert_not_called()
		presence.get_time_consumed.assert_not_called()
		self.assertEqual(abc.presence_quantity, 90)
		abc.save.assert_not_called()
