"""
This module provides a WebID implementation.

Important SPECS:

- https://www.w3.org/2005/Incubator/webid/spec/identity/
- http://xmlns.com/foaf/spec/

Read the `documentation <https://webid.readthedocs.io/en/latest/index.html>`_. 

"""
__version__ = "0.0.1"

from enum import Enum
from rdflib import Graph, URIRef, Literal
from rdflib.namespace import FOAF, RDF
from rdflib import Namespace

SOLID = Namespace("http://www.w3.org/ns/solid/terms#")

SELECT_PRIMARYID = """SELECT ?subject
WHERE {
    ?subject foaf:maker ?maker .
    ?subject foaf:primaryTopic ?topic .

}
"""
SELECT_PRIMARYID_FOR_SOLID = """SELECT ?subject
WHERE {
    ?subject foaf:maker ?maker .
    ?subject foaf:primaryTopic ?topic .

    ?maker solid:oidcIssuer ?issuer .
}
"""


class ParseError(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)

    def __str__(self):
        return "The parsed graph does not contained required WebID tripples."


class FOAFKind(Enum):
    """The kind of FOAF document, for an agent or person."""

    Person = 1  # doc: The document is for a Person.
    Agent = 2  # doc: The document is for an Agent.


class WebID:
    """Initiates a WebID class. The URL is the primary ID URL.

    :param kind: The kind of document owner, a person or an agent.
    :type kind: :class:`webid.FOAFKind`, optional
    :param oidcissuer: URL of the OIDC provider. Default empty string.
    :type oidcissuer: str, optional
    """

    def __init__(
        self,
        url: str,
        kind: FOAFKind = FOAFKind.Person,
        oidcissuer: str = "",
    ) -> None:

        self.url = url
        self.oidcissuer = oidcissuer

        self.me_url = f"{self.url}/#me"
        # This is our actual graph inside
        self.g = Graph()
        # The two default namespaces
        self.g.bind("foaf", FOAF)
        self.g.bind("solid", SOLID)
        self.webid_uri = URIRef(self.url)
        self.g.add((self.webid_uri, RDF.type, FOAF.PersonalProfileDocument))
        # For #me URL of the card
        self.me_uri = URIRef(self.me_url)
        self.g.add((self.webid_uri, FOAF.maker, self.me_uri))
        self.g.add((self.webid_uri, FOAF.primaryTopic, self.me_uri))
        # Now type of the WebID document
        if kind == FOAFKind.Person:
            self.g.add((self.me_uri, RDF.type, FOAF.Person))
        else:
            self.g.add((self.me_uri, RDF.type, FOAF.Agent))
        # Add the OIDC issuer value if available
        if self.oidcissuer:
            self.g.add((self.me_uri, SOLID.oidcIssuer, URIRef(self.oidcissuer)))

    def add_oidc_issuer_registration_token(self, token: str):
        """Adds the given registration token to the card.

        :param token: registration token given by the IDP.
        :type token: str
        """
        self.g.set((self.me_uri, SOLID.oidcIssuerRegistrationToken, Literal(token)))

    @staticmethod
    def parse(data: str, publicid: str = "", solid: bool = False) -> "WebID":
        """
        Parses the given data and creates a WebID.

        :param data: The existing WebID document
        :type data: str
        :param publicid: The primary ID URL, this is optional, default empty string.
        :type publicid: str, optional
        :param solid: If this is a Solid WebID, requires oidcIssuer value in data, default `False`.
        :type solid: bool, optional

        :raises ParseError: Means any required WebID tripples is missing.

        :return: Returns a WebID object
        :rtype: WebID
        """
        g = Graph()
        # If the publicID is already in the turtle, then it will not be changed due to
        # us passing it. But, if it is something like `<>`, then our primaryID URL will
        # be used there.
        g.parse(publicID=publicid, data=data)
        g.bind("foaf", FOAF)
        g.bind("solid", SOLID)
        if not solid:
            qres = g.query(SELECT_PRIMARYID)
        else:
            qres = g.query(SELECT_PRIMARYID_FOR_SOLID)
        if len(qres) != 1:
            raise ParseError

        w = WebID(list(qres)[0][0])
        # Now set our graph internally
        w.g = g
        return w

    def remove_oidc_issuer_registration_token(self):
        """Removes registration token from the card (if any)"""
        self.g.remove((self.me_uri, SOLID.oidcIssuerRegistrationToken, None))

    def serialize(self) -> str:
        """
        Returns a Turtle representation of the WebID document.

        :return: Returns a Turtle representation along with prefixes (if any).
        :rtype: str
        """
        return self.g.serialize(format="turtle")
