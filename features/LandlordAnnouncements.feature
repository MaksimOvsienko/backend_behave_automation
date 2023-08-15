@announcement
@fixture.user_auth
Feature: creation of announcement by landlord
  # only landlord can create announcements

  Scenario Outline: user authorization
    Given user role <user_role> and user id <user_id> for authorization
    Examples:
      | user_role | user_id |
      | Tenant    | 1084    |
      | Landlord  | 1208    |

  Scenario: getting user refresh and access tokens via refresh token
    Given user refresh token
    When request with user refresh token is sent
    Then response code should be 200, should receive json with access and refresh token

  Scenario: creating announcement without media
    Given announcement text data
    When text data are sent
    Then response status code should be 201, should receive json of new announcement

# moved it to after-feature. If need to use this test uncomment it and comment after-feature
  Scenario: deleting announcement without media
    Given previously created announcement
    When delete announcement request is sent
    Then status code of response should be 204
