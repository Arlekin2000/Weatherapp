from app.models import City, User, UserHistory


def test_city_statistic(client):
    u1 = User.insert(email="user1", password="pass1").execute()
    u2 = User.insert(email="user2", password="pass2").execute()

    c1 = City.insert(name="city1", latitude="44.11", longitude="44.11").execute()
    c2 = City.insert(name="city2", latitude="55.11", longitude="55.11").execute()

    UserHistory.insert(user=u1, city=c1).execute()
    UserHistory.insert(user=u2, city=c1).execute()
    UserHistory.insert(user=u1, city=c2).execute()
    UserHistory.insert(user=u2, city=c2).execute()
    UserHistory.insert(user=u2, city=c2).execute()

    response = client.get('/city_statistics')
    assert response.status_code == 200
    assert response.json
    assert response.json == [
        {'count': 2, 'id': 1, 'name': 'city1'},
        {'count': 3, 'id': 2, 'name': 'city2'}
    ]
