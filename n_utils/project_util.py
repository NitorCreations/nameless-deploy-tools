from os import linesep
from sys import argv
from n_utils.profile_util import enable_profile
import locale
import subprocess

def load_project_env():
    """ Print parameters set by git config variables to setup project environment with region and aws credentials
    """
    proc = subprocess.Popen(["git", "config", "--list", "--local"], stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE)
    out = proc.communicate()
    if proc.returncode:
        return
    vars = {}
    for line in out[0].decode(locale.getpreferredencoding()).split("\n"):
        if line:
            next = line.split("=", 1)
            vars[next[0]] = next[1]
    do_print = False
    ret = ""
    if "ndt.profile.azure" in vars:
        enable_profile("azure", vars["ndt.profile.azure"])
    if "ndt.profile.iam" in vars:
        enable_profile("iam", vars["ndt.profile.iam"])
    if "ndt.profile.ndt" in vars:
        enable_profile("ndt", vars["ndt.profile.ndt"])
    if "ndt.source.env" in vars:
        do_print = True
        ret = ret + ". " + vars["ndt.source.env"] + linesep
    if "ndt.aws.profile" in vars:
        do_print = True
        ret = ret + "export AWS_PROFILE=" + vars["ndt.aws.profile"] + \
            " AWS_DEFAULT_PROFILE=" + vars["ndt.aws.profile"] + linesep
    if "ndt.aws.region" in vars:
        do_print = True
        ret = ret + "export AWS_REGION=" + vars["ndt.aws.region"] + \
            " AWS_DEFAULT_REGION=" + vars["ndt.aws.region"] + linesep
    if do_print:
        print(ret.strip())


def ndt_register_complete():
    """Print out shell function and command to register ndt command completion
    """
    print("""_ndt_complete() {
    local IFS=$'\\013'
    local COMP_CUR="${COMP_WORDS[COMP_CWORD]}"
    local COMP_PREV="${COMP_WORDS[COMP_CWORD-1]}"
    local SUPPRESS_SPACE=0
    if compopt +o nospace 2> /dev/null; then
        SUPPRESS_SPACE=1
    fi
    COMPREPLY=( $(IFS="$IFS" \\
                  COMP_LINE="$COMP_LINE" \\
                  COMP_POINT="$COMP_POINT" \\
                  COMP_TYPE="$COMP_TYPE" \\
                  COMP_CUR="$COMP_CUR" \\
                  COMP_PREV="$COMP_PREV" \\
                  COMP_CWORD=$COMP_CWORD \\
                  _ARGCOMPLETE_COMP_WORDBREAKS="$COMP_WORDBREAKS" \\
                  _ARGCOMPLETE=1 \\
                  _ARGCOMPLETE_SUPPRESS_SPACE=$SUPPRESS_SPACE \\
                  "$1" 8>&1 9>&2 1>/dev/null 2>/dev/null) )
    if [[ $? != 0 ]]; then
        unset COMPREPLY
    elif [[ $SUPPRESS_SPACE == 1 ]] && [[ "$COMPREPLY" =~ [=/:]$ ]]; then
        compopt -o nospace
    fi
}
complete -o nospace -F _ndt_complete "ndt" """)
    if len(argv) > 1 and argv[1] == "--project-env":
        print("""_projectenv_hook() {
  local previous_exit_status=$?;
  eval "$(nameless-dt-load-project-env)";
  return $previous_exit_status;
};
if ! [[ "$PROMPT_COMMAND" =~ _projectenv_hook ]]; then
  PROMPT_COMMAND="_projectenv_hook;$PROMPT_COMMAND";
fi""")
