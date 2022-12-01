#!/usr/bin/env bash
# Post install script for the UI .rpm to place symlinks in places to allow the CLI to work similarly in both versions

set -e

ln -s /opt/tree/resources/app.asar.unpacked/daemon/tree /usr/bin/tree || true
ln -s /opt/tree/tree-blockchain /usr/bin/tree-blockchain || true
