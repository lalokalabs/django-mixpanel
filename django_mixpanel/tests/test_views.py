from django.test import Client
from django.urls import reverse
from responses import _recorder
import responses

@responses.activate
def test_track_distinct_id_not_exists():
    responses.add(
        responses.POST,
        "https://mixpanel.com/api/2.0/jql",
        body="[]\n",
        status=200,
        content_type="text/plain"
    )

    client = Client()
    data = {
        "email": "test@aaa.com"
    }
    resp = client.post(reverse("dm-track"), data=data)
    assert resp.status_code == 200

@responses.activate
def test_track_distinct_id_exists():
    email = "test@aaa.com"
    responses.add(
        responses.POST,
        "https://mixpanel.com/api/2.0/jql",
        body=f'[{{"distinct_id":"{email}", "email": "{email}"}}]\n',
        status=200,
        content_type="text/plain"
    )

    client = Client()
    data = {
        "email": email,
    }
    resp = client.post(reverse("dm-track"), data=data)
    assert resp.status_code == 200
    mixpanel_messages = resp.wsgi_request.mixpanel.mocked_messages
    assert mixpanel_messages[0]["msg"]["$set"]["$email"] == email
    assert mixpanel_messages[0]["endpoint"] == "people"
    assert mixpanel_messages[1]["endpoint"] == "events"