#!/usr/bin/env bash
set -euo pipefail

APP_DIR="$(cd "$(dirname "$0")" && pwd)"
export CHURCH_CAP_UPDATE_APP_DIR="$APP_DIR"
export CHURCH_CAP_UPDATE_START_SCRIPT="start-linux.sh"
export CHURCH_CAP_UPDATE_SETUP_SCRIPT="setup-linux.sh"
export CHURCH_CAP_UPDATE_TAG_PREFIX="linux-"
export CHURCH_CAP_UPDATE_ASSET_NAME="Church-Cap-Linux-CLI.tar.gz"
export CHURCH_CAP_UPDATE_PLATFORM="linux"
exec /usr/bin/env bash "$APP_DIR/scripts/update-unix.sh" "$@"
