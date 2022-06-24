from masonite.routes import Route

ROUTES = [
    Route.get("/", "HomeController@show").name("home").middleware("auth"),
    Route.get("/auth", "AuthController@auth").name("auth.login"),
    Route.get("/auth/callback", "AuthController@callback"),
    Route.get("/auth/logout", "AuthController@logout").name("auth.logout"),
    Route.post("/save", "FileController@save").name("save").middleware("auth"),
    Route.post("/sign", "FileController@sign").name("sign").middleware("auth"),
    Route.get("/delete/@id", "FileController@delete").name("delete").middleware("auth"),
    Route.get("/share/@id", "FileController@share").name("share").middleware("auth"),
    Route.get("/lang/@lang", "LangController@switch").name("language_switcher").middleware("auth"),
    Route.post("/generate", "FileController@generate").name("generate").middleware("auth"),
]
