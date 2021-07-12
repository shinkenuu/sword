import factory

from apps.authentications.factories import UserFactory, Role
from apps.tasks.factories import TaskFactory
from apps.tasks.models import Task
from apps.tasks.serializers import TaskDetailSerializer, TaskListSerializer
from tests import BaseTestCase


class ListTestCase(BaseTestCase):
    BASE_URL = '/tasks'

    def test_manager_list_tasks_of_all_technicians(self):
        # ARRANGE
        technicians = UserFactory.create_batch(3, role=Role.TECHNICIAN)
        tasks = [TaskFactory(user=technician) for technician in technicians]

        expected_tasks = [
            TaskListSerializer(task).data for task in tasks
        ]

        # ACT
        self.login_as_manager()
        response = self.client.get(self.BASE_URL)

        # ASSERT
        self.assertEqual(response.status_code, 200)
        self.assertListEqual(response.data, expected_tasks)

    def test_technician_only_list_tasks_of_themselves(self):
        # ARRANGE
        other_technicians = UserFactory.create_batch(3, role=Role.TECHNICIAN)
        other_technicians_tasks = [TaskFactory(user=technician) for technician in other_technicians]

        expected_tasks = [
            TaskListSerializer(task).data
            for task in TaskFactory.create_batch(2, user=self.technician)
        ]

        # ACT
        self.login_as_technician()
        response = self.client.get(self.BASE_URL)

        # ASSERT
        self.assertEqual(response.status_code, 200)
        self.assertListEqual(response.data, expected_tasks)


class CreateTestCase(BaseTestCase):
    BASE_URL = '/tasks'

    def test_manager_can_create_task_to_technician(self):
        # ARRANGE
        task = factory.build(dict, FACTORY_CLASS=TaskFactory)
        task['performed_at'] = None
        task['user'] = self.technician.id

        # ACT
        self.login_as_manager()
        response = self.client.post(self.BASE_URL, task, format='json')

        # ASSERT
        self.assertEqual(response.status_code, 201)

        self.assertEqual(response.data['user'], task['user'])
        self.assertEqual(response.data['summary'], task['summary'])
        self.assertEqual(response.data['performed_at'], task['performed_at'])

    def test_technician_cannot_create_task(self):
        # ARRANGE
        task = factory.build(dict, FACTORY_CLASS=TaskFactory)
        task['user'] = self.technician.id

        # ACT
        self.login_as_technician()
        response = self.client.post(self.BASE_URL, task, format='json')

        # ASSERT
        self.assertEqual(response.status_code, 403)


class RetrieveTestCase(BaseTestCase):
    BASE_URL = '/tasks/{pk}'

    def test_manager_can_retrieve_task_of_technician(self):
        # ARRANGE
        task = TaskFactory(user=self.technician)
        expected_task = TaskDetailSerializer(task).data

        # ACT
        self.login_as_manager()
        response = self.client.get(self.BASE_URL.format(pk=task.id))

        # ASSERT
        self.assertEqual(response.status_code, 200)

        self.assertEqual(response.data['user'], expected_task['user'])
        self.assertEqual(response.data['summary'], expected_task['summary'])
        self.assertEqual(response.data['performed_at'], expected_task['performed_at'])

    def test_technician_can_retrieve_their_own_task(self):
        # ARRANGE
        task = TaskFactory(user=self.technician)
        expected_task = TaskDetailSerializer(task).data

        # ACT
        self.login_as_technician()
        response = self.client.get(self.BASE_URL.format(pk=task.id))

        # ASSERT
        self.assertEqual(response.status_code, 200)

        self.assertEqual(response.data['user'], expected_task['user'])
        self.assertEqual(response.data['summary'], expected_task['summary'])
        self.assertEqual(response.data['performed_at'], expected_task['performed_at'])

    def test_technician_cannot_retrieve_others_task(self):
        # ARRANGE
        task = TaskFactory()

        # ACT
        self.login_as_technician()
        response = self.client.get(self.BASE_URL.format(pk=task.id))

        # ASSERT
        self.assertTrue(Task.objects.filter(id=task.id).exists())
        self.assertEqual(response.status_code, 404)


class UpdateTestCase(BaseTestCase):
    BASE_URL = '/tasks/{pk}'

    def test_manager_cannot_update_task(self):
        # ARRANGE
        task = TaskFactory(user=self.technician)
        updating_task = TaskDetailSerializer(task).data
        updating_task['performed_at'] = '2020-01-01'

        # ACT
        self.login_as_manager()
        response = self.client.put(self.BASE_URL.format(pk=task.id), updating_task, format='json')

        # ASSERT
        self.assertEqual(response.status_code, 403)

    def test_technician_can_update_their_own_task(self):
        # ARRANGE
        task = TaskFactory(user=self.technician)
        updating_task = TaskDetailSerializer(task).data
        updating_task['performed_at'] = '2020-01-01'

        # ACT
        self.login_as_technician()
        response = self.client.put(self.BASE_URL.format(pk=task.id), updating_task, format='json')

        # ASSERT
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['performed_at'], updating_task['performed_at'])

    def test_technician_cannot_update_others_task(self):
        # ARRANGE
        task = TaskFactory()
        updating_task = TaskDetailSerializer(task).data
        updating_task['performed_at'] = '2020-01-01'

        # ACT
        self.login_as_technician()
        response = self.client.put(self.BASE_URL.format(pk=task.id), updating_task, format='json')

        # ASSERT
        self.assertEqual(response.status_code, 404)

    def test_technician_cannot_update_task_user(self):
        # ARRANGE
        task = TaskFactory(user=self.technician)
        updating_task = TaskDetailSerializer(task).data

        other_technician = UserFactory(role=Role.TECHNICIAN.value)
        updating_task['user'] = other_technician.id

        expected_user = {
            'id': self.technician.id,
            'username': self.technician.username,
        }

        # ACT
        self.login_as_technician()
        response = self.client.put(self.BASE_URL.format(pk=task.id), updating_task, format='json')

        # ASSERT
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['user'], expected_user)


class DeleteTestCase(BaseTestCase):
    BASE_URL = '/tasks/{pk}'

    def test_manager_can_delete_task(self):
        # ARRANGE
        task = TaskFactory(user=self.technician)

        # ACT
        self.login_as_manager()
        response = self.client.delete(self.BASE_URL.format(pk=task.id))

        # ASSERT
        self.assertEqual(response.status_code, 204)

    def test_technician_cannot_delete_task(self):
        # ARRANGE
        task = TaskFactory(user=self.technician)

        # ACT
        self.login_as_technician()
        response = self.client.delete(self.BASE_URL.format(pk=task.id))

        # ASSERT
        self.assertEqual(response.status_code, 403)
