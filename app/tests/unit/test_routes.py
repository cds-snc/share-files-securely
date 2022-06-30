from tests import TestCase


class Routes(TestCase):
    def test_protected_routes(self):
        self.get("/").assertRedirect("/auth")
        self.post("/save").assertRedirect("/auth")
        self.post("/sign").assertRedirect("/auth")
        self.get("/delete/id").assertRedirect("/auth")
        self.get("/share/id").assertRedirect("/auth")
        self.get("/lang/lang").assertRedirect("/auth")
        self.post("/generate").assertRedirect("/auth")

    def test_unprotected_routes(self):
        self.get("/auth").assertIsStatus(302)
        self.get("/auth/logout").assertIsStatus(302)
