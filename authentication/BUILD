python_sources(
    name="authentication",
    dependencies=[
        "shared-0.0.1",
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