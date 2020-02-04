from app import create_app
from datetime import datetime
from .utils import create_domains
import json
import pytest


@pytest.yield_fixture(scope='module', autouse=True)
def app():
    app = create_app()
    yield app


@pytest.fixture(autouse=True)
def test_cli(loop, app, sanic_client):
    return loop.run_until_complete(sanic_client(app))


async def test_create_domain(test_cli):
    data = {
        'links': [
            'funbox.ru',
            'vk.com',
            'mail.ru',
            'google.ru'
        ]
    }
    domain = await test_cli.post('/domains', data=json.dumps(data))
    assert domain.status == 200
    data_response = {
        'status': 'ok'
    }
    assert data_response == await domain.json()


async def test_fail_create_domain(test_cli):
    domain = await test_cli.post('/domains', data=json.dumps({}))
    assert domain.status == 400


async def test_get_domains(test_cli):
    domains = [
        'funbox.ru',
        'vk.com',
        'mail.ru',
        'google.ru'
    ]
    timestamp = int(datetime.now().timestamp())
    await create_domains(domains, timestamp)
    domain = await test_cli.get('/domains', params={
        'from': timestamp,
        'to': timestamp
    })
    assert domain.status == 200
    response = await domain.json()
    assert set(domains) == set(response.get('domains'))


async def test_fail_get_domains(test_cli):
    timestamp = int(datetime.now().timestamp())
    domain = await test_cli.get('/domains', params={
        'to': timestamp
    })
    assert domain.status == 400

    domain = await test_cli.get('/domains', params={
        'from': timestamp
    })
    assert domain.status == 400

    domain = await test_cli.get('/domains', params={
    })
    assert domain.status == 400

