import pytest

from webid import WebID

FULL_WEBID = "@prefix foaf: <http://xmlns.com/foaf/0.1/> .\n@prefix solid: <http://www.w3.org/ns/solid/terms#> .\n\n<http://localhost:3000/example/profile/card> a foaf:PersonalProfileDocument ;\n    foaf:maker <http://localhost:3000/example/profile/card/#me> ;\n    foaf:primaryTopic <http://localhost:3000/example/profile/card/#me> .\n\n<http://localhost:3000/example/profile/card/#me> a foaf:Person ;\n    solid:oidcIssuer <http://localhost:3000/> .\n\n"
FULL_WEBID_WITH_AGENT = "@prefix foaf: <http://xmlns.com/foaf/0.1/> .\n@prefix solid: <http://www.w3.org/ns/solid/terms#> .\n\n<http://localhost:3000/example/profile/card> a foaf:PersonalProfileDocument ;\n    foaf:maker <http://localhost:3000/example/profile/card/#me> ;\n    foaf:primaryTopic <http://localhost:3000/example/profile/card/#me> .\n\n<http://localhost:3000/example/profile/card/#me> a foaf:Agent ;\n    solid:oidcIssuer <http://localhost:3000/> .\n\n"
FULL_WEBID_WITHOUT_OIDC = "@prefix foaf: <http://xmlns.com/foaf/0.1/> .\n\n<http://localhost:3000/example/profile/card> a foaf:PersonalProfileDocument ;\n    foaf:maker <http://localhost:3000/example/profile/card/#me> ;\n    foaf:primaryTopic <http://localhost:3000/example/profile/card/#me> .\n\n<http://localhost:3000/example/profile/card/#me> a foaf:Person .\n\n"


def test_full_webid():
    "Tests a full webid creation in turtle format"
    w = WebID(
        "http://localhost:3000/example/profile/card",
        oidcissuer="http://localhost:3000/",
    )

    res = w.serialize()
    assert FULL_WEBID == res


def test_full_webid_with_agent():
    "Tests a full webid creation in turtle format"
    w = WebID(
        "http://localhost:3000/example/profile/card",
        kind="Agent",
        oidcissuer="http://localhost:3000/",
    )

    res = w.serialize()
    assert FULL_WEBID_WITH_AGENT == res


def test_full_webid_without_oidc():
    "Tests a full webid creation in turtle format"
    w = WebID(
        "http://localhost:3000/example/profile/card",
        kind="Person",
    )

    res = w.serialize()
    assert FULL_WEBID_WITHOUT_OIDC == res


def test_issuer_token():
    "Tests adding and removing issuer registration token"
    w = WebID(
        "http://localhost:3000/example/profile/card",
    )

    w.add_oidc_issuer_registration_token("Hack the planet!")
    res = w.serialize()
    assert 'solid:oidcIssuerRegistrationToken "Hack the planet!"' in res
    w.remove_oidc_issuer_registration_token()
    res = w.serialize()
    assert not 'solid:oidcIssuerRegistrationToken "Hack the planet!"' in res
