#include <string.h>

#include <iostream>

const std::string base_str = R"delimiter(_ndt_complete() {
    local IFS=$'\013'
    local COMP_CUR="${COMP_WORDS[COMP_CWORD]}"
    local COMP_PREV="${COMP_WORDS[COMP_CWORD-1]}"
    local SUPPRESS_SPACE=0
    if compopt +o nospace 2> /dev/null; then
        SUPPRESS_SPACE=1
    fi
    COMPREPLY=( $(IFS="$IFS" \
                  COMP_LINE="$COMP_LINE" \
                  COMP_POINT="$COMP_POINT" \
                  COMP_TYPE="$COMP_TYPE" \
                  COMP_CUR="$COMP_CUR" \
                  COMP_PREV="$COMP_PREV" \
                  COMP_CWORD=$COMP_CWORD \
                  _ARGCOMPLETE_COMP_WORDBREAKS="$COMP_WORDBREAKS" \
                  _ARGCOMPLETE=1 \
                  _ARGCOMPLETE_SUPPRESS_SPACE=$SUPPRESS_SPACE \
                  "$1" 8>&1 9>&2 1>/dev/null 2>/dev/null) )
    if [[ $? != 0 ]]; then
        unset COMPREPLY
    elif [[ $SUPPRESS_SPACE == 1 ]] && [[ "$COMPREPLY" =~ [=/:]$ ]]; then
        compopt -o nospace
    fi
}
complete -o nospace -F _ndt_complete "ndt"
)delimiter";
const std::string project_env_str = R"delimiter(_projectenv_hook() {
  local previous_exit_status=$?;
  eval "$(nameless-dt-load-project-env)";
  return $previous_exit_status;
};
if ! [[ "$PROMPT_COMMAND" =~ _projectenv_hook ]]; then
  PROMPT_COMMAND="_projectenv_hook;$PROMPT_COMMAND";
fi
)delimiter";
const std::string nep_complete_str = R"delimiter(_nep_complete() {
    COMPREPLY=( $(ndt print-aws-profiles "${COMP_WORDS[COMP_CWORD]}" ) )
}

nep() {
    if [ "$1" = "-h" -o "$1" = "--help" ]; then
        ndt enable-profile -h
        return
    fi
    eval "$(ndt enable-profile $@)"
}

complete -F _nep_complete nep
)delimiter";
int main(int argc, char *argv[]) {
  std::cout << base_str << std::endl;
  if (argc > 1) {
    for (uint32_t i = 1; i < argc; ++i) {
      if (!strcmp(argv[i], "--project-env")) {
        std::cout << project_env_str << std::endl;
      }
      if (!strcmp(argv[i], "--nep-function")) {
        std::cout << nep_complete_str << std::endl;
      }
    }
  }
}
