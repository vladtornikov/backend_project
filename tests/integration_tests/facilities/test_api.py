async def test_add_facilites(ac):
    facility_title = 'унитаз с подогревом'
    response = await ac.post(
        '/facilities',
        json={'title': facility_title}
    )
    print(f'{response.json()=}')
    res = response.json()
    assert response.status_code == 200
    assert isinstance(res, dict)
    assert res['data']['title'] == facility_title


async def test_get_facilities(ac):
    response = await ac.get('/facilities')
    print(f'{response.json()=}')
    assert response.status_code == 200
    assert isinstance(response.json(), list)

