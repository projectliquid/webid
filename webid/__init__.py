"""
This module provides a WebID implementation.

Important SPECS:

- https://www.w3.org/2005/Incubator/webid/spec/identity/
- http://xmlns.com/foaf/spec/



"""
__version__ = "0.1.0"

from rdflib import Graph, URIRef, Literal
from rdflib.namespace import FOAF, RDF
from rdflib import Namespace

SOLID = Namespace("http://www.w3.org/ns/solid/terms#")


class WebID:
    def __init__(
        self,
        url: str,
        document_kind: str = "ProfileDocument",
        kind: str = "Person",
        solid: bool = False,
        oidcissuer: str = "",
    ) -> None:
        """Initiates a WebID class. The URL is the primary ID URL.

        :args document_kind: ProfileDocument
        :args kind: str, Person or Agent.
        :args oidcissuer: URL of the OIDC provider. Default empty string.
        """
        self.url = url
        self.solid = solid
        self.oidcissuer = oidcissuer
        if document_kind not in ["ProfileDocument"]:
            raise ValueError("Not correct document kind.j")

        if kind not in ["Person", "Agent"]:
            raise ValueError("Wrong data type, can be either Person or Agent")
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
        if kind == "Person":
            self.g.add((self.me_uri, RDF.type, FOAF.Person))
        else:
            self.g.add((self.me_uri, RDF.type, FOAF.Agent))
        # Add the OIDC issuer value if available
        if self.oidcissuer:
            self.g.add((self.me_uri, SOLID.oidcIssuer, URIRef(self.oidcissuer)))

    def serialize(self) -> str:
        return self.g.serialize(format="turtle")
