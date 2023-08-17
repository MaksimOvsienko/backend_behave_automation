import requests

from behave import given, when, then

import logging

from utilities.configurations import get_config, get_password, perform_query
from utilities.resources import ApiResources

log = logging.getLogger(__file__.split('\\')[-1])


@given('user role {user_role} and user id {user_id} for authorization')
def step_impl(context, user_role, user_id):
    user_data_from_query = perform_query(f"SELECT * FROM users WHERE user_role = '{user_role}' AND user_id = '{user_id}'")
    phone = user_data_from_query[0]
    user_role = user_data_from_query[1]
    context.user_data['id'] = user_data_from_query[2]

    response_with_phone_validation_id = requests.post(
        get_config()['API']['endpoint'] + ApiResources.validation_tokens,
        json={
            "phone": phone,
            "userRole": user_role
        },
        headers={
            "accept": "text/plain",
            "Content-Type": "application/json"
        },
    )

    assert response_with_phone_validation_id.status_code == 200

    json_response = response_with_phone_validation_id.json()
    context.user_tokens['phone validation token id'] = json_response['id']
    log.info("phone validation token id = " + context.user_tokens['phone validation token id'])

    user_id_confirmation = requests.put(
        get_config()['API']['endpoint'] + ApiResources.validation_tokens,
        json={
            "id": context.user_tokens['phone validation token id'],
            "code": get_password()
        },
        headers={
            "accept": "*/*", "Content-Type": "application/json"
        },
    )

    assert user_id_confirmation.status_code == 204

    resp_with_acc_n_refr_tokens = requests.post(get_config()['API']['endpoint'] + ApiResources.access_tokens,
                                                json={
                                                    "phoneValidationTokenId": context.user_tokens[
                                                        'phone validation token id'],
                                                    "userRole": user_role
                                                },
                                                headers={"accept": "text/plain",
                                                         "Content-Type": "application/json"
                                                         },
                                                )

    assert resp_with_acc_n_refr_tokens.status_code == 200

    context.user_tokens['access token'] = resp_with_acc_n_refr_tokens.text
    log.info("access token = " + context.user_tokens['access token'])
    context.user_tokens['refresh token'] = resp_with_acc_n_refr_tokens.headers["Refresh-Token"]
    log.info("refresh token = " + context.user_tokens['refresh token'])


@given('user refresh token')
def step_impl(context):
    context.refresh_token = context.user_tokens['refresh token']
    assert context.refresh_token, "user refresh token is missing"


@when('request with user refresh token is sent')
def step_impl(context):
    context.response_with_user_tokens = requests.post(
        get_config()['API']['endpoint'] + ApiResources.access_tokens,
        json={
            "refreshToken": context.refresh_token
        },
        headers={"accept": "text/plain",
                 "Content-Type": "application/json"
                 },
    )


@then('response code should be 200, should receive json with access and refresh token')
def step_impl(context):
    assert context.response_with_user_tokens.status_code == 200
    context.user_tokens['access token'] = context.response_with_user_tokens.text
    log.info("new access token = " + context.user_tokens['access token'])
    context.user_tokens['refresh token'] = context.response_with_user_tokens.headers["Refresh-Token"]
    log.info("new refresh token = " + context.user_tokens['refresh token'])


@given('announcement text data')
def step_impl(context):
    context.announcement_data = {
        "landlordId": context.user_data['id'],
        "currencyId": 1,
        "price": 10000,
        "numberOfRooms": 2,
        "areaTotal": 100,
        "areaResidential": 80,
        "areaKitchen": 20,
        "numberOfStoreys": 13,
        "floor": 6,
        "heatingId": 2,
        "cityId": 1,
        "address": "Test street 7",
        "districtId": 19,
        "latitude": 50,
        "longitude": 30,
        "yearBuilt": 1950,
        "wallId": 7,
        "entranceId": 4,
        "parking": True,
        "repairId": 13,
        "description": "Test api",
        "furniture": True,
        "objectRegistrationNumber": "1488228",
        "kids": True,
        "foreigners": True,
        "animals": True,
        "smoking": True,
        "appliancesId": 16,
        "layoutId": 4,
        "videoFileName": "",
        "videoFirstFrameFileName": "",
        "mapboxBuildingId": "",
        "announcementFacilities": [
            {
                "facilitiesId": 5
            }
        ],
        "announcementAppliances": [
            {
                "appliancesId": 16
            },
            {
                "appliancesId": 17
            }
        ],
        "announcementMetroStations": [
            {
                "metroStationId": 6,
                "distance": 350
            }
        ]
    }


@when('text data are sent')
def step_impl(context):
    context.new_announcement = requests.post(
        get_config()['API']['endpoint'] + ApiResources.announcements,
        json=context.announcement_data,
        headers={
            "accept": "text/plain",
            "Authorization": "Bearer " + context.user_tokens['access token'],
            "Content-Type": "application/json"
        },
    )


@then('response status code should be 201, should receive json of new announcement')
def step_impl(context):
    assert context.new_announcement.status_code == 201
    context.new_announcement_id['id'] = context.new_announcement.json()['id']
    log.info("new announcement id = " + str(context.new_announcement_id['id']))


@given('previously created announcement')
def step_impl(context):
    assert context.new_announcement_id['id']


@when('delete announcement request is sent')
def step_impl(context):
    delete_announcement = requests.delete(
        get_config()['API']['endpoint'] + ApiResources.announcements + f"/{context.new_announcement_id['id']}",
        headers={
            "accept": "*/*",
            "Authorization": "Bearer " + context.user_tokens['access token']
        },
    )
    context.resp_status_code = delete_announcement.status_code


@then('status code of response should be {status_code:d}')
def step_impl(context, status_code):
    assert context.resp_status_code == status_code
