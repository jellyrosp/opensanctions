#!/usr/bin/env bash

_opensanctions_completion() {
    local cur
    cur="${COMP_WORDS[COMP_CWORD]}"

    # Only complete the first argument
    if [[ $COMP_CWORD -eq 1 ]]; then
        COMPREPLY=($(
            opensanctions list_functions 2>/dev/null | \
            grep "^${cur}"
        ))
    fi
}

complete -F _opensanctions_completion opensanctions
