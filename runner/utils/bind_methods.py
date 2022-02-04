from fastapi_jsonrpc import Entrypoint


def bind_methods_on_router(router: Entrypoint, methods_list: list) -> Entrypoint:
    for method in methods_list:
        router.add_method_route(func=method)
    return router
