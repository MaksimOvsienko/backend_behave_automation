@change_data
@fixture.user_auth
Feature: user profile actions
  # profile the same for landlord and tenant, but different api resources

  Scenario Outline: user authorization
    Given user role <user_role> and user id <user_id> for authorization
    Examples:
      | user_role | user_id |
      | Landlord  | 1208    |
#      | Tenant    | 1084    |

  Scenario Outline: get user profile data
    Given user id <user_id> and user role <user_role>
    When request with user id is sent
    Then response code should be 200, should receive json with id and other fields
    Examples:
      | user_role | user_id |
#      | Tenant    | 1084    |
      | Landlord  | 1208    |

  Scenario: edit user profile data
    Given access token and resource determined by user role and id
    When request with new user data is sent
    Then status code of response should be 204