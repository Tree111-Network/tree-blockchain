from __future__ import annotations

import os

from setuptools import setup

dependencies = [
    "aiofiles==22.1.0",  # Async IO for files
    "blspy==1.0.16",  # Signature library
    "chiavdf==1.0.8",  # timelord and vdf verification
    "chiabip158==1.1",  # bip158-style wallet filters
    "chiapos==1.0.11",  # proof of space
    "clvm==0.9.7",
    "clvm_tools==0.4.6",  # Currying, Program.to, other conveniences
    "chia_rs==0.1.14",
    "clvm-tools-rs==0.1.25",  # Rust implementation of clvm_tools' compiler
    "aiohttp==3.8.3",  # HTTP server for full node rpc
    "aiosqlite==0.17.0",  # asyncio wrapper for sqlite, to store blocks
    "bitstring==3.1.9",  # Binary data management library
    "colorama==0.4.5",  # Colorizes terminal output
    "colorlog==6.7.0",  # Adds color to logs
    "concurrent-log-handler==0.9.20",  # Concurrently log and rotate logs
    "cryptography==38.0.3",  # Python cryptography library for TLS - keyring conflict
    "filelock==3.8.0",  # For reading and writing config multiprocess and multithread safely  (non-reentrant locks)
    "keyring==23.9.3",  # Store keys in MacOS Keychain, Windows Credential Locker
    "PyYAML==6.0",  # Used for config file format
    "setproctitle==1.2.3",  # Gives the tree processes readable names
    "sortedcontainers==2.4.0",  # For maintaining sorted mempools
    "click==8.1.3",  # For the CLI
    "dnspython==2.2.1",  # Query DNS seeds
    "watchdog==2.1.9",  # Filesystem event watching - watches keyring.yaml
    "dnslib==0.9.23",  # dns lib
    "typing-extensions==4.4.0",  # typing backports like Protocol and TypedDict
    "zstd==1.5.2.6",
    "packaging==21.3",
    "psutil==5.9.1",
]

upnp_dependencies = [
    "miniupnpc==2.2.2",  # Allows users to open ports on their router
]

dev_dependencies = [
    "build",
    "coverage",
    "diff-cover",
    "pre-commit",
    "py3createtorrent",
    "pylint",
    "pytest",
    "pytest-asyncio>=0.18.1",  # require attribute 'fixture'
    "pytest-cov",
    "pytest-monitor; sys_platform == 'linux'",
    "pytest-xdist",
    "twine",
    "isort",
    "flake8",
    "mypy",
    "black==22.10.0",
    "aiohttp_cors",  # For blackd
    "ipython",  # For asyncio debugging
    "pyinstaller==5.6.2",
    "types-aiofiles",
    "types-cryptography",
    "types-pkg_resources",
    "types-pyyaml",
    "types-setuptools",
]

kwargs = dict(
    name="tree-blockchain",
    author="Mariano Sorgente",
    author_email="mariano@tree111.com",
    description="Tree blockchain full node, farmer, timelord, and wallet.",
    url="https://tree111.com/",
    license="Apache License",
    python_requires=">=3.7, <4",
    keywords="tree blockchain node",
    install_requires=dependencies,
    extras_require=dict(
        dev=dev_dependencies,
        upnp=upnp_dependencies,
    ),
    packages=[
        "build_scripts",
        "tree",
        "tree.cmds",
        "tree.clvm",
        "tree.consensus",
        "tree.daemon",
        "tree.data_layer",
        "tree.full_node",
        "tree.timelord",
        "tree.farmer",
        "tree.harvester",
        "tree.introducer",
        "tree.plot_sync",
        "tree.plotters",
        "tree.plotting",
        "tree.pools",
        "tree.protocols",
        "tree.rpc",
        "tree.seeder",
        "tree.server",
        "tree.simulator",
        "tree.types.blockchain_format",
        "tree.types",
        "tree.util",
        "tree.wallet",
        "tree.wallet.db_wallet",
        "tree.wallet.puzzles",
        "tree.wallet.cat_wallet",
        "tree.wallet.did_wallet",
        "tree.wallet.nft_wallet",
        "tree.wallet.settings",
        "tree.wallet.trading",
        "tree.wallet.util",
        "tree.ssl",
        "mozilla-ca",
    ],
    entry_points={
        "console_scripts": [
            "tree = tree.cmds.tree:main",
            "tree_daemon = tree.daemon.server:main",
            "tree_wallet = tree.server.start_wallet:main",
            "tree_full_node = tree.server.start_full_node:main",
            "tree_harvester = tree.server.start_harvester:main",
            "tree_farmer = tree.server.start_farmer:main",
            "tree_introducer = tree.server.start_introducer:main",
            "tree_crawler = tree.seeder.start_crawler:main",
            "tree_seeder = tree.seeder.dns_server:main",
            "tree_timelord = tree.server.start_timelord:main",
            "tree_timelord_launcher = tree.timelord.timelord_launcher:main",
            "tree_full_node_simulator = tree.simulator.start_simulator:main",
            "tree_data_layer = tree.server.start_data_layer:main",
            "tree_data_layer_http = tree.data_layer.data_layer_server:main",
        ]
    },
    package_data={
        "tree": ["pyinstaller.spec"],
        "": ["*.clvm", "*.clvm.hex", "*.clib", "*.clinc", "*.clsp", "py.typed"],
        "tree.util": ["initial-*.yaml", "english.txt"],
        "tree.ssl": ["tree_ca.crt", "tree_ca.key", "dst_root_ca.pem"],
        "mozilla-ca": ["cacert.pem"],
    },
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    zip_safe=False,
    project_urls={
        "Source": "https://github.com/Tree111-Network/tree-blockchain/",
        "Changelog": "https://github.com/Tree111-Network/tree-blockchain/blob/main/CHANGELOG.md",
    },
)


if len(os.environ.get("TREE_SKIP_SETUP", "")) < 1:
    setup(**kwargs)  # type: ignore
