from datetime import date, time, timedelta

from abonnement.models import Abonnement, AbonnementClient
from client.models import Client
from creneau.models import Creneau
from django.test import TestCase
from planning.models import Planning
from salle_activite.models import Activity, Salle
from salle_sport.models import SalleSport

from presence.models import Presence


class PresenceAndClientTests(TestCase):
    def setUp(self):
        # Setup required objects for models
        self.salle_sport = SalleSport.objects.create(
            name="Gym Center", adresse="123 Street", phone="123456789"
        )
        self.planning = Planning.objects.create(
            name="Standard Planning", salle_sport=self.salle_sport, is_default=True
        )
        self.salle = Salle.objects.create(name="Main Salle")
        self.activity = Activity.objects.create(name="Cardio", salle=self.salle)
        self.creneau = Creneau.objects.create(
            hour_start=time(10, 0),
            hour_finish=time(12, 0),
            day="LU",
            planning=self.planning,
            activity=self.activity,
        )

        # Create an Abonnement with Time Volume (VH)
        self.abonnement_type = Abonnement.objects.create(
            name="1000 Minutes",
            type_of="VH",
            price=1000,
            length="30",
            seances_quantity=1000,
        )
        self.abonnement_type.salles.add(self.salle)

        self.client = Client.objects.create(
            id="C0001", first_name="John", last_name="Doe", blood="O+", carte="12345678"
        )

        self.abonnement_client = AbonnementClient.objects.create(
            client=self.client,
            type_abonnement=self.abonnement_type,
            start_date=date.today() - timedelta(days=1),
            end_date=date.today() + timedelta(days=30),
            presence_quantity=1000,
        )

    # def test_get_time_consumed_same_day(self):
    #     """Test calculation of duration on the same day."""
    #     presence = Presence.objects.create(
    #         abc=self.abonnement_client,
    #         creneau=self.creneau,
    #         date=date(2026, 2, 22),
    #         hour_entree=time(10, 0),
    #     )
    #     # Entry at 10:00, Exit at 11:30
    #     consumed = presence.get_time_consumed(sortie="11:30:00")
    #     self.assertEqual(consumed, 90)
    #     self.assertEqual(presence.hour_sortie, time(11, 30))

    def test_get_time_consumed_midnight_wraparound(self):
        """Test calculation of duration when crossing midnight."""
        presence = Presence.objects.create(
            abc=self.abonnement_client,
            creneau=self.creneau,
            date=date(2026, 2, 22),
            hour_entree=time(23, 0),
        )
        # Entry at 23:00, Exit at 01:00 next day
        consumed = presence.get_time_consumed(sortie="01:00:00")
        self.assertEqual(consumed, 120)
        self.assertEqual(presence.hour_sortie, time(1, 0))

    # def test_calculate_duration_minutes_same_day(self):
    #     """Test calculate_duration_minutes on the same day."""
    #     presence = Presence.objects.create(
    #         abc=self.abonnement_client,
    #         creneau=self.creneau,
    #         date=date(2026, 2, 22),
    #         hour_entree=time(10, 0),
    #         hour_sortie=time(11, 0),
    #     )
    #     duration = presence.calculate_duration_minutes()
    #     self.assertEqual(duration, 60)

    def test_calculate_duration_minutes_midnight_wraparound(self):
        """Verify calculate_duration_minutes behavior with midnight wraparound."""
        print('=========== test_calculate_duration_minutes_midnight_wraparound called ===========')
        presence = Presence.objects.create(
            abc=self.abonnement_client,
            creneau=self.creneau,
            date=date(2026, 2, 22),
            hour_entree=time(23, 0),
            hour_sortie=time(1, 0),
        )
        duration = presence.calculate_duration_minutes()
        
        self.assertEqual(duration, 120)

    def test_client_init_output_normal(self):
        """Test Client.init_output correctly records exit and deducts time."""
        presence = Presence.objects.create(
            abc=self.abonnement_client,
            creneau=self.creneau,
            date=date.today(),
            hour_entree=time(10, 0),
        )

        # Mocking time logic by passing exit_hour
        success = self.client.init_output(exit_hour="11:30:00")

        self.assertTrue(success)
        presence.refresh_from_db()
        self.assertEqual(presence.hour_sortie, time(11, 30))

        self.abonnement_client.refresh_from_db()
        # Original (1000 * 60) - 90 consumed = 59910
        self.assertEqual(self.abonnement_client.presence_quantity, 59910)

    def test_client_init_output_skip(self):
        """Test Client.init_output skips if exit is within 10 seconds of entry."""
        # Current time mock is hard, but we can rely on how init_output parses it
        # Entry time 12:00:00
        # Exit time 12:00:05
        presence = Presence.objects.create(
            abc=self.abonnement_client,
            creneau=self.creneau,
            date=date.today(),
            hour_entree="12:00:00",
        )

        result = self.client.init_output(exit_hour="12:00:05")
        self.assertEqual(result, "skip")

        presence.refresh_from_db()
        self.assertIsNone(presence.hour_sortie)

    def test_client_init_output_no_presence(self):
        """Test Client.init_output returns False if no active presence exists."""
        result = self.client.init_output()
        self.assertFalse(result)

    def test_client_init_output_midnight_wraparound(self):
        """Test Client.init_output handles midnight wraparound across days."""
        # Entry at 23:30
        # Exit at 00:30 next day
        presence = Presence.objects.create(
            abc=self.abonnement_client,
            creneau=self.creneau,
            date=date.today(),
            hour_entree="23:30:00",
        )

        success = self.client.init_output(exit_hour="00:30:00")
        self.assertTrue(success)

        presence.refresh_from_db()
        self.assertEqual(presence.hour_sortie, time(0, 30))

        self.abonnement_client.refresh_from_db()
        # (1000 * 60) - 60 = 59940
        self.assertEqual(self.abonnement_client.presence_quantity, 59940)
