import requests
import logging

from behave import given, when, then

from utilities.configurations import get_config
from utilities.resources import ApiResources

log = logging.getLogger(__file__.split('\\')[-1])


@given('user id {user_id} and user role {user_role}')
def step_impl(context, user_id, user_role):
    context.user_id = user_id
    log.info("user id = " + context.user_id)
    context.user_role = user_role


@when('request with user id is sent')
def step_impl(context):
    log.info("user role = " + context.user_role)

    if context.user_role == 'Landlord':
        context.user_fields = requests.get(
            get_config()['API']['endpoint'] + ApiResources.landlords + f"/{context.user_data['id']}",
            headers={
                "accept": "text/plain",
                "Authorization": "Bearer " + context.user_tokens['access token']
            },
        )

    if context.user_role == 'Tenant':
        context.user_fields = requests.get(
            get_config()['API']['endpoint'] + ApiResources.tenants + f"/{context.user_data['id']}",
            headers={
                "accept": "text/plain",
                "Authorization": "Bearer " + context.user_tokens['access token']
            },
        )


@then('response code should be 200, should receive json with id and other fields')
def step_impl(context):
    assert context.user_fields.status_code == 200
    user_fields = context.user_fields.json()
    for i in user_fields:
        context.user_data[i] = user_fields[i]
    log.info("user data = " + str(context.user_data))
    assert int(context.user_id) == context.user_data['id']


@given('access token and resource determined by user role and id')
def step_impl(context):
    assert context.user_tokens['access token']


@when('request with new user data is sent')
def step_impl(context):
    new_user_fields = requests.put(
        get_config()['API']['endpoint'] + ApiResources.landlords + f"/{context.user_data['id']}",
        json={
            "id": context.user_data['id'],
            "name": "newname",
            "surname": "new sur",
            "patronymic": "new patronymic",
            "phone": "+380669898989",
            "email": "newmail@gmail.com",
            "genderId": 2
        },
        headers={
            "content-type": "application/json; charset=utf-8",
            "Authorization": "Bearer " + context.user_tokens['access token']
        },
    )

    context.resp_status_code = new_user_fields.status_code

# @then('response code is 204, new data appeared')
# def step_impl(context):
#     assert context.new_user_fields.status_code == 204
