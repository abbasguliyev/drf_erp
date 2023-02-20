from django.test import TestCase
from company.models import Team


class TeamTest(TestCase):
    def setUp(self) -> None:
        self.team = Team(name="Team")
        self.team.save()
    
    def tearDown(self) -> None:
        self.team.delete()
    
    def test_read_team(self):
        self.assertEqual(self.team.name, "Team")
        self.assertTrue(self.team.is_active)
    
    def test_update_team_name(self):
        self.team.name = "Team2"
        self.team.save()
        self.assertEqual(self.team.name, "Team2")
    
    def test_update_team_is_active(self):
        self.team.is_active =False
        self.team.save()
        self.assertFalse(self.team.is_active)
