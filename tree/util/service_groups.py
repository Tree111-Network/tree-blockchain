from __future__ import annotations

from typing import Generator, KeysView

SERVICES_FOR_GROUP = {
    "all": (
        "tree_harvester tree_timelord_launcher tree_timelord tree_farmer "
        "tree_full_node tree_wallet tree_data_layer tree_data_layer_http"
    ).split(),
    # TODO: should this be `data_layer`?
    "data": "tree_wallet tree_data_layer".split(),
    "data_layer_http": "tree_data_layer_http".split(),
    "node": "tree_full_node".split(),
    "harvester": "tree_harvester".split(),
    "farmer": "tree_harvester tree_farmer tree_full_node tree_wallet".split(),
    "farmer-no-wallet": "tree_harvester tree_farmer tree_full_node".split(),
    "farmer-only": "tree_farmer".split(),
    "timelord": "tree_timelord_launcher tree_timelord tree_full_node".split(),
    "timelord-only": "tree_timelord".split(),
    "timelord-launcher-only": "tree_timelord_launcher".split(),
    "wallet": "tree_wallet".split(),
    "introducer": "tree_introducer".split(),
    "simulator": "tree_full_node_simulator".split(),
    "crawler": "tree_crawler".split(),
    "seeder": "tree_crawler tree_seeder".split(),
    "seeder-only": "tree_seeder".split(),
}


def all_groups() -> KeysView[str]:
    return SERVICES_FOR_GROUP.keys()


def services_for_groups(groups) -> Generator[str, None, None]:
    for group in groups:
        for service in SERVICES_FOR_GROUP[group]:
            yield service


def validate_service(service: str) -> bool:
    return any(service in _ for _ in SERVICES_FOR_GROUP.values())
