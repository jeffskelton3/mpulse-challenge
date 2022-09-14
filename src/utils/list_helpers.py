from pydantic import BaseModel


def unique_basemodel_list(
    items: list[BaseModel], dedupe_by_key: str | int
) -> list[BaseModel]:
    item_map = {}
    for item in items:
        item_map[item.dict()[dedupe_by_key]] = item
    unique = []
    for k, v in item_map.items():
        unique.append(v.dict())
    return unique
