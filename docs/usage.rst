Usage guide
============


This module provides an implementation to build and modify `WebID <https://www.w3.org/2005/Incubator/webid/spec/identity/>`_ 
documents.

How to install?
-----------------

To install the latest release from pypi.

::

    python3 -m pip install pywebid


Parsing an existing document
-----------------------------

You can parse any existing Solid compliant WebID to create a new object. Using the static method :py:meth:`webid.WebID.parse` for the same.


::

    data = """@prefix foaf: <http://xmlns.com/foaf/0.1/>.
    @prefix solid: <http://www.w3.org/ns/solid/terms#>.

    <>
        a foaf:PersonalProfileDocument;
        foaf:maker <http://localhost:3000/example/profile/card#me>;
        foaf:primaryTopic <http://localhost:3000/example/profile/card#me>.

    <http://localhost:3000/example/profile/card#me>

        solid:oidcIssuer <http://localhost:3000/>;
        a foaf:Agent.
    """
    w = WebID.parse(data, publicid="http://localhost:3000/example/profile/card")


Create new WebID
-----------------

You will need an URL for the WebID document, you can also pass `oidcIssuer` if you want.

::

    w = WebID(
        "http://localhost:3000/example/profile/card",
        kind=FOAFKind.Agent,
        oidcissuer="http://localhost:3000/",
    )
    res = w.serialize()

You can also add or remove registration token for the oidcIssuer, have a look at the API documentation and test cases.
