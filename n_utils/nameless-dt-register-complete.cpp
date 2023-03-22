#include <iostream>
#include <string>
#include <vector>

constexpr auto BASE_STR = R"delimiter(_ndt_complete() {
  local IFS=$'\013'
  local COMP_CUR="${COMP_WORDS[COMP_CWORD]}"
  local COMP_PREV="${COMP_WORDS[COMP_CWORD - 1]}"
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
    "$1" 8>&1 9>&2 1> /dev/null 2> /dev/null) )
  if [[ $? != 0 ]]; then
    unset COMPREPLY
  elif [[ $SUPPRESS_SPACE == 1 ]] && [[ "$COMPREPLY" =~ [=/:]$ ]]; then
    compopt -o nospace
  fi
}
complete -o nospace -F _ndt_complete "ndt"
)delimiter";

constexpr auto PROJECT_ENV_STR = R"delimiter(_projectenv_hook() {
  local previous_exit_status=$?
  eval "$(nameless-dt-load-project-env)"
  return $previous_exit_status
}
if ! [[ "$PROMPT_COMMAND" =~ _projectenv_hook ]]; then
  PROMPT_COMMAND="_projectenv_hook;$PROMPT_COMMAND"
fi
)delimiter";

constexpr auto NEP_COMPLETE_STR = R"delimiter(_nep_complete() {
  if [ -n "$(command -v nameless-dt-print-aws-profiles)" ]; then
    ndt_print_command="nameless-dt-print-aws-profiles"
  else
    ndt_print_command="ndt print-aws-profiles"
  fi
  COMPREPLY=($($ndt_print_command "${COMP_WORDS[COMP_CWORD]}"))
}

nep() {
  if [ "$1" = "-h" ] || [ "$1" = "--help" ]; then
    ndt enable-profile -h
    return
  fi
  eval "$(ndt enable-profile "$@")"
}
complete -F _nep_complete nep
)delimiter";

int main(int argc, const char* argv[]) {
    std::cout << BASE_STR << std::endl;
    std::vector<std::string> arguments(argv, argv + argc);
    for (const auto& arg : arguments) {
        if (arg == "--project-env") {
            std::cout << PROJECT_ENV_STR << std::endl;
        } else if (arg == "--nep-function") {
            std::cout << NEP_COMPLETE_STR << std::endl;
        }
    }
}
