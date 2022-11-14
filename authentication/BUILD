python_sources(
    name="authentication",
    dependencies=[
        "shared",
        "//:requirements"
    ],
)

pex_binary(
    name="run",
    entry_point="run.py",
    dependencies=[
        ":authentication",
        "//:requirements"
    ],
    restartable=True,
)