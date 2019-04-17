#!/usr/bin/env bash

# Script to test if ssh-keygen and tinysshd-printkey produce
# the same public key output, indicating that the conversion
# successfully produces the same key.
set -e -o pipefail

# create temporary directory
tmp=$(mktemp -d)
trap "rm -rf '$tmp'" INT TERM EXIT

# generate key with openssh tools
ssh-keygen -t ed25519 -f "$tmp/test" -N '' -C ''
OPENSSH=$(head -c 80 "$tmp/test.pub")

# convert the key
./tinyssh-keyconvert -v "$tmp/test" -d "$tmp"

# print publuc key with tinyssh tools
TINYSSH=$(tinysshd-printkey "$tmp")

# compare
printf 'OpenSSH: %s\nTinySSH: %s\n' "$OPENSSH" "$TINYSSH"
if [[ $OPENSSH != $TINYSSH ]]; then
  exit 1
fi