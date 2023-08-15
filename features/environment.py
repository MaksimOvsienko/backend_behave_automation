import pathlib

import requests
from utilities.configurations import get_config
from utilities.resources import ApiResources
import logging
from behave import fixture, use_fixture

log = logging.getLogger(__file__.split('\\')[-1])


@fixture()
def user_auth(context):
    context.user_tokens = {}

    context.new_announcement_id = {'id': ''}
    context.user_data = {}


def before_all(context):
    context.config.setup_logging(
        filename='behave.log',
        level=logging.INFO,
        force=True,
        format="%(asctime)s | %(name)s | %(levelname)s | %(message)s",
        filemode='w'
    )

    # context.log = custom_logger()


def before_tag(context, tag):
    if tag == "fixture.user_auth":
        use_fixture(user_auth, context)


def after_feature(context, feature):
    # if "announcement" in feature.tags:
    #     delete_announcement = requests.delete(
    #         get_config()['API']['endpoint'] + ApiResources.announcements + f"/{context.new_announcement_id['id']}",
    #         headers={
    #             "accept": "*/*",
    #             "Authorization": "Bearer " + context.user_tokens['access token']
    #         },
    #     )
    #     print(delete_announcement.status_code)
    #     assert delete_announcement.status_code == 204

    if "change_data" in feature.tags:
        assert context.user_tokens['access token']
        change_back_user_fields = requests.put(
            get_config()['API']['endpoint'] + ApiResources.landlords + f"/{context.user_data['id']}",
            json={
                "id": context.user_data['id'],
                "name": "api32",
                "surname": "test32",
                "patronymic": "qa3",
                "phone": "+380669879879",
                "email": "test23@gmail.com",
                "genderId": 1
            },
            headers={
                "content-type": "application/json; charset=utf-8",
                "Authorization": "Bearer " + context.user_tokens['access token']
            },
        )

        assert change_back_user_fields.status_code == 204
