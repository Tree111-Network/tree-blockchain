from __future__ import annotations

import asyncio
import logging
from typing import Tuple

import aiohttp
from cryptography import x509
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes, serialization

from tree.protocols.shared_protocol import capabilities, protocol_version
from tree.server.outbound_message import NodeType
from tree.server.server import TreeServer, ssl_context_for_client
from tree.server.ssl_context import tree_ssl_ca_paths
from tree.server.ws_connection import WSTreeConnection
from tree.simulator.time_out_assert import time_out_assert
from tree.ssl.create_ssl import generate_ca_signed_cert
from tree.types.blockchain_format.sized_bytes import bytes32
from tree.types.peer_info import PeerInfo
from tree.util.config import load_config
from tree.util.ints import uint16

log = logging.getLogger(__name__)


async def disconnect_all(server: TreeServer) -> None:
    connections = list(server.all_connections.values())
    await asyncio.gather(*(connection.close() for connection in connections))

    await asyncio.sleep(5)  # 5 seconds to allow connections and tasks to all drain


async def disconnect_all_and_reconnect(server: TreeServer, reconnect_to: TreeServer, self_hostname: str) -> bool:
    await disconnect_all(server)
    return await server.start_client(PeerInfo(self_hostname, uint16(reconnect_to._port)), None)


async def add_dummy_connection(
    server: TreeServer, self_hostname: str, dummy_port: int, type: NodeType = NodeType.FULL_NODE
) -> Tuple[asyncio.Queue, bytes32]:
    timeout = aiohttp.ClientTimeout(total=10)
    session = aiohttp.ClientSession(timeout=timeout)
    incoming_queue: asyncio.Queue = asyncio.Queue()
    config = load_config(server.root_path, "config.yaml")
    tree_ca_crt_path, tree_ca_key_path = tree_ssl_ca_paths(server.root_path, config)
    dummy_crt_path = server.root_path / "dummy.crt"
    dummy_key_path = server.root_path / "dummy.key"
    generate_ca_signed_cert(
        tree_ca_crt_path.read_bytes(), tree_ca_key_path.read_bytes(), dummy_crt_path, dummy_key_path
    )
    ssl_context = ssl_context_for_client(tree_ca_crt_path, tree_ca_key_path, dummy_crt_path, dummy_key_path)
    pem_cert = x509.load_pem_x509_certificate(dummy_crt_path.read_bytes(), default_backend())
    der_cert = x509.load_der_x509_certificate(pem_cert.public_bytes(serialization.Encoding.DER), default_backend())
    peer_id = bytes32(der_cert.fingerprint(hashes.SHA256()))
    url = f"wss://{self_hostname}:{server._port}/ws"
    ws = await session.ws_connect(url, autoclose=True, autoping=True, ssl=ssl_context)
    wsc = WSTreeConnection.create(
        type,
        ws,
        server._port,
        log,
        True,
        self_hostname,
        incoming_queue,
        None,
        peer_id,
        100,
        30,
        local_capabilities_for_handshake=capabilities,
    )
    await wsc.perform_handshake(server._network_id, protocol_version, dummy_port, NodeType.FULL_NODE)
    return incoming_queue, peer_id


async def connect_and_get_peer(server_1: TreeServer, server_2: TreeServer, self_hostname: str) -> WSTreeConnection:
    """
    Connect server_2 to server_1, and get return the connection in server_1.
    """
    await server_2.start_client(PeerInfo(self_hostname, uint16(server_1._port)))

    async def connected():
        for node_id_c, _ in server_1.all_connections.items():
            if node_id_c == server_2.node_id:
                return True
        return False

    await time_out_assert(10, connected, True)
    for node_id, wsc in server_1.all_connections.items():
        if node_id == server_2.node_id:
            return wsc
    assert False
