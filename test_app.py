import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from app import create_app
from models import setup_db, Movie, Actor

CASTING_ASSISTANCE_TOKEN = "Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6ImdLcnE0V2d5SlJnMGJSNGt0QWh1WCJ9.eyJpc3MiOiJodHRwczovL2Rldi13MHR3dmFtNy5ldS5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NWYyYzgyMmI2ODAzM2YwMDNkNjQ5MmE2IiwiYXVkIjoiY2Fwc3RvbmUiLCJpYXQiOjE1OTcxNDAzMzUsImV4cCI6MTU5NzE0NzUzNSwiYXpwIjoiZklxQXpGVk1DR0hVNXpnVjNPSkJIVm93c3ZZNFFRWE0iLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImdldDphY3RvcnMiLCJnZXQ6bW92aWVzIl19.VHP1xLe4Y8-QfCO6JaFzgg6UQenIOZS8VOTKYcNdl7km1MgTE3_2BrgpPyZU3WHacGXamNXEPVz6UQX_kRXH0XC4Xv0_-mP5CaBpR-kwNqOVIK1nltOKNQs_derFTsWsl6DWsShI_Yv0jPxxj4Zi4DUlnwmK1LspSF8DJ4MNdIqa8kMNVUQYhrJUBuDozAOv99HFqex2m9QaWuc6-ooj2oUj17oWpi3AzKj6bB_gh7uZRoGmAEEqgvK4H17OXjryJiAIIuBmXOi-nJaLxBEBz9DHweoBxmPu7K9pDHX2pi90XZSqCllCmz1ZzdaXc0-6EmBOvwfSe9FO3fj2OSx9ew"

CASTING_DIRECTOR_TOKEN = "Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6ImdLcnE0V2d5SlJnMGJSNGt0QWh1WCJ9.eyJpc3MiOiJodHRwczovL2Rldi13MHR3dmFtNy5ldS5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NWYyYzgyNTg3M2E4YmIwMDNkMjRkNWMwIiwiYXVkIjoiY2Fwc3RvbmUiLCJpYXQiOjE1OTcxNDQwODksImV4cCI6MTU5NzIzMDQ4OSwiYXpwIjoiZklxQXpGVk1DR0hVNXpnVjNPSkJIVm93c3ZZNFFRWE0iLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImRlbGV0ZTphY3RvcnMiLCJnZXQ6YWN0b3JzIiwiZ2V0Om1vdmllcyIsInBhdGNoOmFjdG9ycyIsInBhdGNoOm1vdmllcyIsInBvc3Q6YWN0b3JzIl19.VGgXARIcPFdtSYFp1o8fnqp5a5-ewzgM4UEvZ2soaxyHI4LrTUW2puTxhAALnSk-ZEjvnnauQP7uQ-iLEbqrOrPGJdFkcwSwrwuopwtt_cm5eTvXYBWpuuQkFRzioXgGh5HZEHftp0Z1otRpZoxwl3Ls7vQGQpazjqbLgqUCuSskvKp4X-f3NYbJT65QW8UqAtWhrdHrvp6UZrT8xAM6DAlA5Pq7CY-P1xAUTSOFRaslEyDiURqei7xU4SizkWMvFvKl6eCXB37IwdoBC_eILzt-BB1EgGMABd8jxri4UaKUPOeyTju7pzUssbd2hxFCRpxcg5PNIYErlTvecDq9_w"

EXECUTIVE_PRODUCER_TOKEN = "Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6ImdLcnE0V2d5SlJnMGJSNGt0QWh1WCJ9.eyJpc3MiOiJodHRwczovL2Rldi13MHR3dmFtNy5ldS5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NWYyYzgyN2YxOTg2N2EwMDM3MzE3ZGIwIiwiYXVkIjoiY2Fwc3RvbmUiLCJpYXQiOjE1OTcxNDI1OTgsImV4cCI6MTU5NzE0OTc5OCwiYXpwIjoiZklxQXpGVk1DR0hVNXpnVjNPSkJIVm93c3ZZNFFRWE0iLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImRlbGV0ZTphY3RvcnMiLCJkZWxldGU6bW92aWVzIiwiZ2V0OmFjdG9ycyIsImdldDptb3ZpZXMiLCJwYXRjaDphY3RvcnMiLCJwYXRjaDptb3ZpZXMiLCJwb3N0OmFjdG9ycyIsInBvc3Q6bW92aWVzIl19.G0a4cdDyfTH44XWRulFErRaxr0j-WqA79q7-rJr_ae5uvrRu17rdRn2J9TQ_GmjB1jeekx2yu6SxMSnizgKrYLtnRha_qBfkFaHO6HG-wAOwWnhl0VaiaRjAHNcpBCTcLa5w_3jAFbjUtHtNFMpFs9CAPYdUMY0DD56aaFAcYHvl6DLLwTGMRUR7YRc6KO4_EGr4MQ5KH2O4RBMvFjoGxRJm2SXvx0WFAwkahfH-A0LThWV5T2zTNoczspKGwOqh_14dtZf768_WD2j08oHacku18ARBslG52KNSjZIgKcYdr8AN5XQLSyYg7pS83WiZlAnPPgvvnLzAzcymS1mQ-A"


class CapstoneTestCase(unittest.TestCase):
    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "capstone_test"
        self.database_path = "postgres://{}:{}@{}/{}".format(
            'postgres', 'admin', 'localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            self.db.create_all()

        actor = Actor(name="test", age=25, gender="male")
        actor.insert()
        movie = Movie(title="test", release_date="2020-10-10")
        movie.insert()

    def tearDown(self):

        pass

    def test_get_actors_success(self):
        res = self.client().get(
            '/actors', headers={"Authorization": f"{CASTING_ASSISTANCE_TOKEN}"})
        body = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(body['success'], True)
        self.assertEqual(len(body['actors']), 10)

    def test_get_actors_error(self):
        res = self.client().get('/actors?page=100',
                                headers={"Authorization": f"{CASTING_ASSISTANCE_TOKEN}"})
        body = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(body['error'], 404)
        self.assertEqual(body['message'], 'RESOURCE NOT FOUND!')

    def test_get_movies_success(self):
        res = self.client().get(
            '/movies', headers={"Authorization": f"{CASTING_ASSISTANCE_TOKEN}"})
        body = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(body['success'], True)
        self.assertEqual(len(body['movies']), 10)

    def test_get_movies_error(self):
        res = self.client().get('/movies?page=100',
                                headers={"Authorization": f"{CASTING_ASSISTANCE_TOKEN}"})
        body = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(body['error'], 404)
        self.assertEqual(body['message'], 'RESOURCE NOT FOUND!')

    def test_delete_actor_success(self):
        res = self.client().delete(
            '/actors/7', headers={"Authorization": f"{CASTING_DIRECTOR_TOKEN}"})
        body = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(body['success'], True)
        self.assertEqual(body['actor_id'], 7)

    def test_delete_actor_error(self):
        res = self.client().delete(
            '/actors/100', headers={"Authorization": f"{CASTING_DIRECTOR_TOKEN}"})
        body = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(body['error'], 404)
        self.assertEqual(body['message'], 'RESOURCE NOT FOUND!')

    def test_delte_movie_success(self):
        res = self.client().delete(
            '/movies/9', headers={"Authorization": f"{EXECUTIVE_PRODUCER_TOKEN}"})
        body = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(body['success'], True)
        self.assertEqual(body['movie_id'], 9)

    def test_delete_movie_error(self):
        res = self.client().delete(
            '/movies/100', headers={"Authorization": f"{EXECUTIVE_PRODUCER_TOKEN}"})
        body = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(body['error'], 404)
        self.assertEqual(body['message'], 'RESOURCE NOT FOUND!')

    def test_create_actor_success(self):
        res = self.client().post('/actors', json={
            'name': 'test',
            'age': 25,
            'gender': 'male'
        }, headers={"Authorization": f"{CASTING_DIRECTOR_TOKEN}"})
        body = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(body['success'], True)
        self.assertTrue(body['actor'])

    def test_create_actor_error(self):
        res = self.client().post('/actors', json={
            'name': 'test',
            'age': 25
        }, headers={"Authorization": f"{CASTING_DIRECTOR_TOKEN}"})
        body = json.loads(res.data)
        self.assertEqual(res.status_code, 422)
        self.assertEqual(body['error'], 422)
        self.assertEqual(body['message'], 'UNPROCESSABLE ENTITY!')

    def test_create_movie_success(self):
        res = self.client().post('/movies', json={
            'title': 'test',
            'release_date': '2020-10-10',
        }, headers={"Authorization": f"{EXECUTIVE_PRODUCER_TOKEN}"})
        body = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(body['success'], True)
        self.assertTrue(body['movie'])

    def test_create_movie_error(self):
        res = self.client().post('/movies', json={
            'title': 'test'
        }, headers={"Authorization": f"{EXECUTIVE_PRODUCER_TOKEN}"})
        body = json.loads(res.data)
        self.assertEqual(res.status_code, 422)
        self.assertEqual(body['error'], 422)
        self.assertEqual(body['message'], 'UNPROCESSABLE ENTITY!')

    def test_modify_actor_success(self):
        res = self.client().patch('/actors/15', json={
            'name': 'test2',
            'age': 26,
            'gender': 'male'
        }, headers={"Authorization": f"{CASTING_DIRECTOR_TOKEN}"})
        body = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(body['success'], True)
        self.assertEqual(body['actor'].get('name'), 'test2')
        self.assertEqual(body['actor'].get('age'), 26)

    def test_modify_actor_error(self):
        res = self.client().patch(
            '/actors/100', headers={"Authorization": f"{CASTING_DIRECTOR_TOKEN}"})
        body = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(body['error'], 404)
        self.assertEqual(body['message'], 'RESOURCE NOT FOUND!')

    def test_modify_movie_success(self):
        res = self.client().patch('/movies/17', json={
            'title': 'test2',
            'release_date': '2021-10-10'
        }, headers={"Authorization": f"{CASTING_DIRECTOR_TOKEN}"})
        body = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(body['success'], True)
        self.assertEqual(body['movie'].get('title'), 'test2')
        self.assertEqual(body['movie'].get('release_date'),
                         'Sun, 10 Oct 2021 00:00:00 GMT')

    def test_modify_movie_error(self):
        res = self.client().patch(
            '/movies/100', headers={"Authorization": f"{CASTING_DIRECTOR_TOKEN}"})
        body = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(body['error'], 404)
        self.assertEqual(body['message'], 'RESOURCE NOT FOUND!')

    # TESTING RBAC

    def test_assistance_role_success(self):
        res = self.client().get(
            '/actors', headers={"Authorization": f"{CASTING_ASSISTANCE_TOKEN}"})
        self.assertEqual(res.status_code, 200)

    def test_assistance_role_error(self):
        res = self.client().delete(
            '/actors/1', headers={"Authorization": f"{CASTING_ASSISTANCE_TOKEN}"})
        self.assertEqual(res.status_code, 401)

    def test_director_role_success(self):
        res = self.client().patch(
            '/actors/2', json={
                'name': 'test2',
                'age': 26,
                'gender': 'male'
            }, headers={"Authorization": f"{CASTING_DIRECTOR_TOKEN}"})
        self.assertEqual(res.status_code, 200)

    def test_director_role_error(self):
        res = self.client().delete(
            '/movies/1', headers={"Authorization": f"{CASTING_DIRECTOR_TOKEN}"})
        self.assertEqual(res.status_code, 401)

    def test_producer_role_success(self):
        res = self.client().get(
            '/actors', headers={"Authorization": f"{EXECUTIVE_PRODUCER_TOKEN}"})
        self.assertEqual(res.status_code, 200)

    def test_producer_role_success(self):
        res = self.client().post(
            '/movies', json={
                'title': 'test2',
                'release_date': '2021-10-10'}, headers={"Authorization": f"{EXECUTIVE_PRODUCER_TOKEN}"})
        self.assertEqual(res.status_code, 200)


if __name__ == "__main__":
    unittest.main()
