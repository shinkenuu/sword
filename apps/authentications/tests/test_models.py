from django.test import TestCase
from apps.authentications.models import User, Role


class RoleTestCase(TestCase):
    def test_technicians_are_not_managers(self):
        self.assertNotEqual(Role.MANAGER, Role.TECHNICIAN)


class UserIsManagerTestCase(TestCase):
    def test_is_manager_returns_true_when_role_is_manager(self):
        # ARRANGE
        manager_employee = User(role=Role.MANAGER)

        # ACT
        is_manager_result = manager_employee.is_manager

        # ASSERT
        self.assertTrue(is_manager_result)

    def test_is_manager_returns_false_when_role_is_not_manager(self):
        # ARRANGE
        not_a_manager_employee = User(role=Role.TECHNICIAN)

        # ACT
        is_manager_result = not_a_manager_employee.is_manager

        # ASSERT
        self.assertFalse(is_manager_result)


class UserIsTechnicianTestCase(TestCase):
    def test_is_technician_returns_true_when_role_is_technician(self):
        # ARRANGE
        technician_employee = User(role=Role.TECHNICIAN)

        # ACT
        is_technician_result = technician_employee.is_technician

        # ASSERT
        self.assertTrue(is_technician_result)

    def test_is_technician_returns_false_when_role_is_not_technician(self):
        # ARRANGE
        not_a_technician_employee = User(role=Role.MANAGER)

        # ACT
        is_technician_result = not_a_technician_employee.is_technician

        # ASSERT
        self.assertFalse(is_technician_result)
