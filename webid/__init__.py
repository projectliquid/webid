from rdflib import Graph, URIRef, Literal
from rdflib.namespace import FOAF, RDF
from rdflib import Namespace

SOLID = Namespace("http://www.w3.org/ns/solid/terms#")


# Important SPECS:
# https://www.w3.org/2005/Incubator/webid/spec/identity/
# http://xmlns.com/foaf/spec/


class WebID:
    def __init__(
        self,
        url: str,
        document_kind: str = "ProfileDocument",
        kind: str = "Person",
        solid: bool = False,
    ) -> None:
        """Initiates a WebID class. The URL is the primary ID URL.

        :args document_kind: ProfileDocument
        :args kind: str, Person or Agent.
        """
        self.url = url
        self.solid = solid
        if document_kind not in ["ProfileDocument"]:
            raise ValueError("Not correct document kind.j")
        self.tripples = {}

        if kind not in ["Person", "Agent"]:
            raise ValueError("Wrong data type, can be either Person or Agent")
        self.me_url = f"{self.url}/#me"
        internal = []
        if kind == "Person":
            internal.append((RDF.type, FOAF.Person))
        else:
            internal.append((RDF.type, FOAF.Agent))
        self.tripples[self.me_url] = internal

    def add_oidcissuer(self, issuer: str) -> None:
        """Adds the oidc issuer to the WebID document.

        :args issuer: URL of the OIDC provider.
        """
        self.tripples["oidcissuer"] = issuer

    def serialize(self) -> str:
        g = Graph()
        g.bind("foaf", FOAF)
        g.bind("solid", SOLID)
        self_uri = URIRef(self.url)
        g.add((self_uri, RDF.type, FOAF.PersonalProfileDocument))
        internal = self.tripples.get(self.me_url, [])
        me_uri = URIRef(self.me_url)
        # Add maker
        g.add((self_uri, FOAF.maker, me_uri))
        # Add primary topic
        g.add((self_uri, FOAF.primaryTopic, me_uri))

        # Each entry is a tuple of predicate & object
        for entry in internal:
            g.add((me_uri, entry[0], entry[1]))

        # Add any OIDC issuer
        if "oidcissuer" in self.tripples:
            g.add((me_uri, SOLID.oidcIssuer, URIRef(self.tripples["oidcissuer"])))

        return g.serialize(format="turtle")
