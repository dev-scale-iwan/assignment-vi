from fastapi import Query

def standard_query_params(
    limit: int | None = Query(default=None),
    offset: int | None = Query(default=None),
):
    return {"limit": limit, "offset": offset}