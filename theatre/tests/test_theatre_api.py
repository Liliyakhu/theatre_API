import tempfile
import os


from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status

from theatre.models import Play, Performance, TheatreHall, Genre, Actor
from theatre.serializers import PlayListSerializer, PlayDetailSerializer


PLAY_URL = reverse("theatre:play-list")
PERFORMANCE_URL = reverse("theatre:performance-list")


def sample_play(**params):
    defaults = {
        "title": "Sample play",
        "description": "Sample description"
    }
    defaults.update(params)

    return Play.objects.create(**defaults)


def sample_genre(**params):
    defaults = {
        "name": "Drama",
    }
    defaults.update(params)

    return Genre.objects.create(**defaults)


def sample_actor(**params):
    defaults = {"first_name": "Lyudmila", "last_name": "Monastyrska"}
    defaults.update(params)

    return Actor.objects.create(**defaults)


def sample_performance(**params):
    theatre_hall = TheatreHall.objects.create(
        name="Blue", rows=20, seats_in_row=20
    )

    defaults = {
        "show_time": "2022-06-02 14:00:00",
        "play": None,
        "theatre_hall": theatre_hall,
    }
    defaults.update(params)

    return Performance.objects.create(**defaults)


def detail_url(play_id):
    return reverse("theatre:play-detail", args=[play_id])


class UnauthenticatedPlayApiTests(TestCase):

    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        res = self.client.get(PLAY_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class AuthenticatedPlayApiTests(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            email="test@test.com",
            password="testpass"
        )
        self.client.force_authenticate(user=self.user)

    def test_plays_list(self):
        sample_play()
        play_with_actor_and_genre = sample_play()

        actor = sample_actor()
        genre = sample_genre()

        play_with_actor_and_genre.actors.add(actor)
        play_with_actor_and_genre.genres.add(genre)

        res = self.client.get(PLAY_URL)
        plays = Play.objects.all()
        serializer = PlayListSerializer(plays, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        # print(res.data)

        # with version of djangorestframework == 3.13
        # the next assertion was correct:
        # self.assertEqual(res.data["results"], serializer.data)

        self.assertEqual(res.data["results"], serializer.data)

    def test_filter_plays_by_title(self):
        play_1 = sample_play()
        play_2 = sample_play(title="Test play")

        res = self.client.get(
            PLAY_URL,
            {"title": "Test play"}
        )

        serializer_test_play = PlayListSerializer(play_2)

        print(res.data)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data["results"]), 1)
        self.assertEqual(res.data["results"][0], serializer_test_play.data)
        self.assertEqual(res.data["results"][0]["title"], "Test play")

    def test_filter_plays_by_actors(self):
        play = sample_play()
        play_with_actor_1 = sample_play(title="Test_1")
        play_with_actor_2 = sample_play(title="Test_2")

        actor_1 = sample_actor()
        actor_2 = sample_actor(first_name="Oleksandr")

        play_with_actor_1.actors.add(actor_1)
        play_with_actor_2.actors.add(actor_2)

        res = self.client.get(
            PLAY_URL,
            {"actors": f"{actor_1.id},{actor_2.id}"}
        )

        serializer = PlayListSerializer(play)
        serializer_play_actor_1 = PlayListSerializer(play_with_actor_1)
        serializer_play_actor_2 = PlayListSerializer(play_with_actor_2)

        print(res.data)

        self.assertIn(serializer_play_actor_1.data, res.data["results"])
        self.assertIn(serializer_play_actor_2.data, res.data["results"])
        self.assertNotIn(serializer.data, res.data["results"])

    def test_filter_plays_by_genres(self):
        play = sample_play()
        play_with_genre_1 = sample_play(title="Test_1")
        play_with_genre_2 = sample_play(title="Test_2")

        genre_1 = sample_genre()
        genre_2 = sample_genre(name="Comedy")

        play_with_genre_1.genres.add(genre_1)
        play_with_genre_2.genres.add(genre_2)

        res = self.client.get(
            PLAY_URL,
            {"genres": f"{genre_1.id},{genre_2.id}"}
        )

        serializer = PlayListSerializer(play)
        serializer_play_genre_1 = PlayListSerializer(play_with_genre_1)
        serializer_play_genre_2 = PlayListSerializer(play_with_genre_2)

        self.assertIn(serializer_play_genre_1.data, res.data["results"])
        self.assertIn(serializer_play_genre_2.data, res.data["results"])
        self.assertNotIn(serializer.data, res.data["results"])

    def test_retrieve_play_detail(self):
        play = sample_play()
        play.actors.add(sample_actor())
        play.genres.add(sample_genre())

        url = detail_url(play.id)

        res = self.client.get(url)

        serializer = PlayDetailSerializer(play)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_create_play_forbidden(self):
        payload = {
            "title": "Test title",
            "description": "Some description"
        }

        res = self.client.post(PLAY_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)


class AdminBusTests(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            email="admin@admin.com",
            password="testpass",
            is_staff=True,
        )
        self.client.force_authenticate(user=self.user)

    def test_create_play(self):
        payload = {
            "title": "Test title",
            "description": "Some description"
        }

        res = self.client.post(PLAY_URL, payload)

        play = Play.objects.get(id=res.data["id"])

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        for key in payload:
            self.assertEqual(payload[key], getattr(play, key))

    def test_create_play_with_actors(self):
        actor_1 = sample_actor()
        actor_2 = sample_actor(first_name="Leo")
        payload = {
            "title": "Test title",
            "description": "Some description",
            "duration": 90,
            "actors": [actor_1.id, actor_2.id]
        }

        res = self.client.post(PLAY_URL, payload)

        play = Play.objects.get(id=res.data["id"])
        actors = Actor.objects.all()

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertIn(actor_1, actors)
        self.assertIn(actor_2, actors)
        self.assertEqual(actors.count(), 2)

    def test_create_play_with_genres(self):
        genre_1 = sample_genre()
        genre_2 = sample_genre(name="Poem")
        payload = {
            "title": "Test title",
            "description": "Some description",
            "duration": 90,
            "genres": [genre_1.id, genre_2.id]
        }

        res = self.client.post(PLAY_URL, payload)

        play = Play.objects.get(id=res.data["id"])
        genres = Genre.objects.all()

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertIn(genre_1, genres)
        self.assertIn(genre_2, genres)
        self.assertEqual(genres.count(), 2)

    def test_delete_play_not_allowed(self):
        play = sample_play()

        url = detail_url(play.id)

        res = self.client.delete(url)

        self.assertEqual(res.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

