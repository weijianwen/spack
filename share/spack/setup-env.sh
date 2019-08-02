# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


########################################################################
#
# This file is part of Spack and sets up the spack environment for bash,
# zsh, and dash (sh).  This includes dotkit support, module support, and
# it also puts spack in your path.  The script also checks that at least
# module support exists, and provides suggestions if it doesn't. Source
# it like this:
#
#    . /path/to/spack/share/spack/setup-env.sh
#
########################################################################
# This is a wrapper around the spack command that forwards calls to
# 'spack use' and 'spack unuse' to shell functions.  This in turn
# allows them to be used to invoke dotkit functions.
#
# 'spack use' is smarter than just 'use' because it converts its
# arguments into a unique spack spec that is then passed to dotkit
# commands.  This allows the user to use packages without knowing all
# their installation details.
#
# e.g., rather than requiring a full spec for libelf, the user can type:
#
#     spack use libelf
#
# This will first find the available libelf dotkits and use a
# matching one.  If there are two versions of libelf, the user would
# need to be more specific, e.g.:
#
#     spack use libelf@0.8.13
#
# This is very similar to how regular spack commands work and it
# avoids the need to come up with a user-friendly naming scheme for
# spack dotfiles.
########################################################################

spack() {
    # Zsh does not do word splitting by default, this enables it for this
    # function only
    if [ -n "${ZSH_VERSION:-}" ]; then
        emulate -L sh
    fi

    # accumulate flags meant for the main spack command
    # the loop condition is unreadable, but it means:
    #     while $1 is set (while there are arguments)
    #       and $1 starts with '-' (and the arguments are flags)
    _sp_flags=""
    while [ ! -z ${1+x} ] && [ "${1#-}" != "${1}" ]; do
        _sp_flags="$_sp_flags $1"
        shift
    done

    # h and V flags don't require further output parsing.
    if [ -n "$_sp_flags" ] && \
       [ "${_sp_flags#*h}" != "${_sp_flags}" ] || \
       [ "${_sp_flags#*V}" != "${_sp_flags}" ];
    then
        command spack $_sp_flags "$@"
        return
    fi

    # set the subcommand if there is one (if $1 is set)
    _sp_subcommand=""
    if [ ! -z ${1+x} ]; then
        _sp_subcommand="$1"
        shift
    fi

    # Filter out use and unuse.  For any other commands, just run the
    # command.
    case $_sp_subcommand in
        "cd")
            _sp_arg=""
            if [ -n "$1" ]; then
                _sp_arg="$1"
                shift
            fi
            if [ "$_sp_arg" = "-h" ] || [ "$_sp_arg" = "--help" ]; then
                command spack cd -h
            else
                LOC="$(spack location $_sp_arg "$@")"
                if [ -d "$LOC" ] ; then
                    cd "$LOC"
                else
                    return 1
                fi
            fi
            return
            ;;
        "env")
            _sp_arg=""
            if [ -n "$1" ]; then
                _sp_arg="$1"
                shift
            fi

            if [ "$_sp_arg" = "-h" ] || [ "$_sp_arg" = "--help" ]; then
                command spack env -h
            else
                case $_sp_arg in
                    activate)
                        _a="$@"
                        if [ -z ${1+x} ] || \
                           [ "${_a#*--sh}" != "$_a" ] || \
                           [ "${_a#*--csh}" != "$_a" ] || \
                           [ "${_a#*-h}" != "$_a" ];
                        then
                            # no args or args contain -h/--help, --sh, or --csh: just execute
                            command spack env activate "$@"
                        else
                            # actual call to activate: source the output
                            eval $(command spack $_sp_flags env activate --sh "$@")
                        fi
                        ;;
                    deactivate)
                        _a="$@"
                        if [ "${_a#*--sh}" != "$_a" ] || \
                           [ "${_a#*--csh}" != "$_a" ];
                        then
                            # just  execute the command if --sh or --csh are provided
                            command spack env deactivate "$@"
                        elif [ -n "$*" ]; then
                            # any other arguments are an error or help, so just run help
                            command spack env deactivate -h
                        else
                            # no args: source the output of the command
                            eval $(command spack $_sp_flags env deactivate --sh)
                        fi
                        ;;
                    *)
                        command spack env $_sp_arg "$@"
                        ;;
                esac
            fi
            return
            ;;
        "use"|"unuse"|"load"|"unload")
            # Shift any other args for use off before parsing spec.
            _sp_subcommand_args=""
            _sp_module_args=""
            while [ "${1#-}" != "${1}" ]; do
                if [ "$1" = "-h" ] || [ "$1" = "--help" ]; then
                    command spack $_sp_flags $_sp_subcommand $_sp_subcommand_args "$@"
                    return
                elif [ "$1" = "-r" ] || [ "$1" = "--dependencies" ]; then
                    _sp_subcommand_args="$_sp_subcommand_args $1"
                else
                    _sp_module_args="$_sp_module_args $1"
                fi
                shift
            done

            # Here the user has run use or unuse with a spec.  Find a matching
            # spec using 'spack module find', then use the appropriate module
            # tool's commands to add/remove the result from the environment.
            # If spack module command comes back with an error, do nothing.
            case $_sp_subcommand in
                "use")
                    if _sp_full_spec=$(command spack $_sp_flags module dotkit find $_sp_subcommand_args "$@"); then
                        use $_sp_module_args $_sp_full_spec
                    else
                        $(exit 1)
                    fi
                    ;;
                "unuse")
                    if _sp_full_spec=$(command spack $_sp_flags module dotkit find $_sp_subcommand_args "$@"); then
                        unuse $_sp_module_args $_sp_full_spec
                    else
                        $(exit 1)
                    fi
                    ;;
                "load")
                    if _sp_full_spec=$(command spack $_sp_flags module tcl find $_sp_subcommand_args "$@"); then
                        module load $_sp_module_args $_sp_full_spec
                    else
                        $(exit 1)
                    fi
                    ;;
                "unload")
                    if _sp_full_spec=$(command spack $_sp_flags module tcl find $_sp_subcommand_args "$@"); then
                        module unload $_sp_module_args $_sp_full_spec
                    else
                        $(exit 1)
                    fi
                    ;;
            esac
            ;;
        *)
            command spack $_sp_flags $_sp_subcommand "$@"
            ;;
    esac
}


########################################################################
# Prepends directories to path, if they exist.
#      pathadd /path/to/dir            # add to PATH
# or   pathadd OTHERPATH /path/to/dir  # add to OTHERPATH
########################################################################
_spack_pathadd() {
    # If no variable name is supplied, just append to PATH
    # otherwise append to that variable.
    _pa_varname=PATH
    _pa_new_path="$1"
    if [ -n "$2" ]; then
        _pa_varname="$1"
        _pa_new_path="$2"
    fi

    # Do the actual prepending here.
    eval "_pa_oldvalue=\${${_pa_varname}:-}"

    _pa_canonical=":$_pa_oldvalue:"
    if [ -d "$_pa_new_path" ] && \
       [ "${_pa_canonical#*:${_pa_new_path}:}" = "${_pa_canonical}" ];
    then
        if [ -n "$_pa_oldvalue" ]; then
            eval "export $_pa_varname=\"$_pa_new_path:$_pa_oldvalue\""
        else
            export $_pa_varname="$_pa_new_path"
        fi
    fi
}


#
# Determine which shell is being used
#
_spack_determine_shell() {
    if [ -n "${BASH:-}" ]; then
        echo bash
    elif [ -n "${ZSH_NAME:-}" ]; then
        echo zsh
    else
        PS_FORMAT= ps -p $$ | tail -n 1 | awk '{print $4}' | sed 's/^-//' | xargs basename
    fi
}
_sp_shell=$(_spack_determine_shell)


# Export spack function so it is available in subshells (only works with bash)
if [ "$_sp_shell" = bash ]; then
    export -f spack
fi

#
# Figure out where this file is.
#
if [ "$_sp_shell" = bash ]; then
    _sp_source_file="${BASH_SOURCE[0]:-}"
elif [ "$_sp_shell" = zsh ]; then
    _sp_source_file="${(%):-%N}"
else
    # Try to read the /proc filesystem (works on linux without lsof)
    # In dash, the sourced file is the last one opened (and it's kept open)
    _sp_source_file_fd="$(\ls /proc/$$/fd 2>/dev/null | sort -n | tail -1)"
    if ! _sp_source_file="$(readlink /proc/$$/fd/$_sp_source_file_fd)"; then
        # Last resort: try lsof. This works in dash on macos -- same reason.
        # macos has lsof installed by default; some linux containers don't.
        _sp_lsof_output="$(lsof -p $$ -Fn0 | tail -1)"
        _sp_source_file="${_sp_lsof_output#*n}"
    fi

    # If we can't find this script's path after all that, bail out with
    # plain old $0, which WILL NOT work if this is sourced indirectly.
    if [ ! -f "$_sp_source_file" ]; then
        _sp_source_file="$0"
    fi
fi

#
# Find root directory and add bin to path.
#
# We send cd output to /dev/null to avoid because a lot of users set up
# their shell so that cd prints things out to the tty.
_sp_share_dir="$(cd "$(dirname $_sp_source_file)" > /dev/null && pwd)"
_sp_prefix="$(cd "$(dirname $(dirname $_sp_share_dir))" > /dev/null && pwd)"
if [ -x "$_sp_prefix/bin/spack" ]; then
    export SPACK_ROOT="${_sp_prefix}"
else
    # If the shell couldn't find the sourced script, fall back to
    # whatever the user set SPACK_ROOT to.
    if [ -n "$SPACK_ROOT" ]; then
        _sp_prefix="$SPACK_ROOT"
        _sp_share_dir="$_sp_prefix/share/spack"
    fi

    # If SPACK_ROOT didn't work, fail.  We should need this rarely, as
    # the tricks above for finding the sourced file are pretty robust.
    if [ ! -x "$_sp_prefix/bin/spack" ]; then
        echo "==> Error: SPACK_ROOT must point to spack's prefix when using $_sp_shell"
        echo "Run this with the correct prefix before sourcing setup-env.sh:"
        echo "    export SPACK_ROOT=</path/to/spack>"
        return 1
    fi
fi
_spack_pathadd PATH "${_sp_prefix%/}/bin"

#
# Check whether a function of the given name is defined
#
_spack_fn_exists() {
	LANG= type $1 2>&1 | grep -q 'function'
}

need_module="no"
if ! _spack_fn_exists use && ! _spack_fn_exists module; then
	need_module="yes"
fi;

#
# make available environment-modules
#
if [ "${need_module}" = "yes" ]; then
    eval `spack --print-shell-vars sh,modules`

    # _sp_module_prefix is set by spack --print-sh-vars
    if [ "${_sp_module_prefix}" != "not_installed" ]; then
        # activate it!
        # environment-modules@4: has a bin directory inside its prefix
        _sp_module_bin="${_sp_module_prefix}/bin"
        if [ ! -d "${_sp_module_bin}" ]; then
            # environment-modules@3 has a nested bin directory
            _sp_module_bin="${_sp_module_prefix}/Modules/bin"
        fi

        # _sp_module_bin and _sp_shell are evaluated here; the quoted
        # eval statement and $* are deferred.
        _sp_cmd="module() { eval \`${_sp_module_bin}/modulecmd ${_sp_shell} \$*\`; }"
        eval "$_sp_cmd"
        _spack_pathadd PATH "${_sp_module_bin}"
    fi;
else
    eval `spack --print-shell-vars sh`
fi;


#
# set module system roots
#
_sp_multi_pathadd() {
    local IFS=':'
    if [ "$_sp_shell" = zsh ]; then
        setopt sh_word_split
    fi
    for pth in $2; do
        _spack_pathadd "$1" "${pth}/${_sp_sys_type}"
    done
}
_sp_multi_pathadd MODULEPATH "$_sp_tcl_roots"
_sp_multi_pathadd DK_NODE "$_sp_dotkit_roots"

# Add programmable tab completion for Bash
#
if [ "$_sp_shell" = bash ]; then
    source $_sp_share_dir/spack-completion.bash
fi
