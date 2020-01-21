# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


# The following global variables are used/set by Bash programmable completion
#     COMP_CWORD: An index into ${COMP_WORDS} of the word containing the
#                 current cursor position
#     COMP_LINE:  The current command line
#     COMP_WORDS: an array containing individual command arguments typed so far
#     COMPREPLY:  an array containing possible completions as a result of your
#                 function

# Bash programmable completion for Spack
_bash_completion_spack () {
    # In all following examples, let the cursor be denoted by brackets, i.e. []

    # For our purposes, flags should not affect tab completion. For instance,
    # `spack install []` and `spack -d install --jobs 8 []` should both give the same
    # possible completions. Therefore, we need to ignore any flags in COMP_WORDS.
    local COMP_WORDS_NO_FLAGS=()
    local index=0
    while [[ "$index" -lt "$COMP_CWORD" ]]
    do
        if [[ "${COMP_WORDS[$index]}" == [a-z]* ]]
        then
            COMP_WORDS_NO_FLAGS+=("${COMP_WORDS[$index]}")
        fi
        let index++
    done

    # Options will be listed by a subfunction named after non-flag arguments.
    # For example, `spack -d install []` will call _spack_install
    # and `spack compiler add []` will call _spack_compiler_add
    local subfunction=$(IFS='_'; echo "_${COMP_WORDS_NO_FLAGS[*]}")

    # Translate dashes to underscores, as dashes are not permitted in
    # compatibility mode. See https://github.com/spack/spack/pull/4079
    subfunction=${subfunction//-/_}

    # However, the word containing the current cursor position needs to be
    # added regardless of whether or not it is a flag. This allows us to
    # complete something like `spack install --keep-st[]`
    COMP_WORDS_NO_FLAGS+=("${COMP_WORDS[$COMP_CWORD]}")

    # Since we have removed all words after COMP_CWORD, we can safely assume
    # that COMP_CWORD_NO_FLAGS is simply the index of the last element
    local COMP_CWORD_NO_FLAGS=$(( ${#COMP_WORDS_NO_FLAGS[@]} - 1 ))

    # There is no guarantee that the cursor is at the end of the command line
    # when tab completion is envoked. For example, in the following situation:
    #     `spack -d [] install`
    # if the user presses the TAB key, a list of valid flags should be listed.
    # Note that we cannot simply ignore everything after the cursor. In the
    # previous scenario, the user should expect to see a list of flags, but
    # not of other subcommands. Obviously, `spack -d list install` would be
    # invalid syntax. To accomplish this, we use the variable list_options
    # which is true if the current word starts with '-' or if the cursor is
    # not at the end of the line.
    local list_options=false
    if [[ "${COMP_WORDS[$COMP_CWORD]}" == -* || \
          "$COMP_CWORD" -ne "${#COMP_WORDS[@]}-1" ]]
    then
        list_options=true
    fi

    # In general, when envoking tab completion, the user is not expecting to
    # see optional flags mixed in with subcommands or package names. Tab
    # completion is used by those who are either lazy or just bad at spelling.
    # If someone doesn't remember what flag to use, seeing single letter flags
    # in their results won't help them, and they should instead consult the
    # documentation. However, if the user explicitly declares that they are
    # looking for a flag, we can certainly help them out.
    #     `spack install -[]`
    # and
    #     `spack install --[]`
    # should list all flags and long flags, respectively. Furthermore, if a
    # subcommand has no non-flag completions, such as `spack arch []`, it
    # should list flag completions.

    local cur=${COMP_WORDS_NO_FLAGS[$COMP_CWORD_NO_FLAGS]}
    local prev=${COMP_WORDS_NO_FLAGS[$COMP_CWORD_NO_FLAGS-1]}

    #_test_vars

    # Make sure function exists before calling it
    if [[ "$(type -t $subfunction)" == "function" ]]
    then
        COMPREPLY=($($subfunction))
    fi
}

# Spack commands

_spack () {
    if $list_options
    then
        compgen -W "-h --help -H --all-help --color -C --config-scope -d --debug --timestamp --pdb -e --env -D --env-dir -E --no-env --use-env-repo -k --insecure -l --enable-locks -L --disable-locks -m --mock -p --profile --sorted-profile --lines -v --verbose --stacktrace -V --version --print-shell-vars" -- "$cur"
    else
        compgen -W "$(_subcommands)" -- "$cur"
    fi
}

_spack_activate () {
    if $list_options
    then
        compgen -W "-h --help -f --force -v --view" -- "$cur"
    else
        compgen -W "$(_installed_packages)" -- "$cur"
    fi
}

_spack_add () {
    if $list_options
    then
        compgen -W "-h --help -l --list-name" -- "$cur"
    else
        compgen -W "$(_all_packages)" -- "$cur"
    fi
}

_spack_arch () {
    compgen -W "-h --help --known-targets -p --platform -o --operating-system -t --target -f --frontend -b --backend" -- "$cur"
}

_spack_blame () {
    if $list_options
    then
        compgen -W "-h --help -t --time -p --percent -g --git" -- "$cur"
    else
        compgen -W "$(_all_packages)" -- "$cur"
    fi
}

_spack_bootstrap () {
    compgen -W "-h --help -j --jobs --keep-prefix --keep-stage -n --no-checksum -v --verbose --use-cache --no-cache --cache-only --clean --dirty" -- "$cur"
}

_spack_build () {
    if $list_options
    then
        compgen -W "-h --help -v --verbose" -- "$cur"
    else
        compgen -W "$(_all_packages)" -- "$cur"
    fi
}

_spack_build_env () {
    if $list_options
    then
        compgen -W "-h --help --clean --dirty --dump --pickle" -- "$cur"
    else
        compgen -W "$(_all_packages)" -- "$cur"
    fi
}

_spack_buildcache () {
    if $list_options
    then
        compgen -W "-h --help" -- "$cur"
    else
        compgen -W "create install list keys preview check download get-buildcache-name save-yaml copy update-index" -- "$cur"
    fi
}

_spack_buildcache_create () {
    if $list_options
    then
        compgen -W "-h --help -r --rel -f --force -u --unsigned -a --allow-root -k --key -d --directory --no-rebuild-index -y --spec-yaml --no-deps" -- "$cur"
    else
        compgen -W "$(_all_packages)" -- "$cur"
    fi
}

_spack_buildcache_install () {
    if $list_options
    then
        compgen -W "-h --help -f --force -m --multiple -a --allow-root -u --unsigned" -- "$cur"
    else
        compgen -W "$(_all_packages)" -- "$cur"
    fi
}

_spack_buildcache_list () {
    if $list_options
    then
        compgen -W "-h --help -l --long -L --very-long -v --variants -f --force" -- "$cur"
    else
        compgen -W "$(_all_packages)" -- "$cur"
    fi
}

_spack_buildcache_keys () {
    compgen -W "-h --help -i --install -t --trust -f --force" -- "$cur"
}

_spack_buildcache_preview () {
    if $list_options
    then
        compgen -W "-h --help" -- "$cur"
    else
        compgen -W "$(_installed_packages)" -- "$cur"
    fi
}

_spack_buildcache_check () {
    compgen -W "-h --help -m --mirror-url -o --output-file --scope -s --spec -y --spec-yaml --rebuild-on-error" -- "$cur"
}

_spack_buildcache_download () {
    compgen -W "-h --help -s --spec -y --spec-yaml -p --path -c --require-cdashid" -- "$cur"
}

_spack_buildcache_get_buildcache_name () {
    compgen -W "-h --help -s --spec -y --spec-yaml" -- "$cur"
}

_spack_buildcache_save_yaml () {
    compgen -W "-h --help --root-spec --root-spec-yaml -s --specs -y --yaml-dir" -- "$cur"
}

_spack_buildcache_copy () {
    compgen -W "-h --help --base-dir --spec-yaml --destination-url" -- "$cur"
}

_spack_buildcache_update_index () {
    compgen -W "-h --help -d --mirror-url" -- "$cur"
}

_spack_cd () {
    if $list_options
    then
        compgen -W "-h --help -m --module-dir -r --spack-root -i --install-dir -p --package-dir -P --packages -s --stage-dir -S --stages -b --build-dir -e --env" -- "$cur"
    else
        compgen -W "$(_all_packages)" -- "$cur"
    fi
}

_spack_checksum () {
    if $list_options
    then
        compgen -W "-h --help --keep-stage" -- "$cur"
    else
        compgen -W "$(_all_packages)" -- "$cur"
    fi
}

_spack_clean () {
    if $list_options
    then
        compgen -W "-h --help -s --stage -d --downloads -m --misc-cache -p --python-cache -a --all" -- "$cur"
    else
        compgen -W "$(_all_packages)" -- "$cur"
    fi
}

_spack_clone () {
    if $list_options
    then
        compgen -W "-h --help -r --remote" -- "$cur"
    fi
}

_spack_commands () {
    if $list_options
    then
        compgen -W "-h --help --format --header --update" -- "$cur"
    fi
}

_spack_compiler () {
    if $list_options
    then
        compgen -W "-h --help" -- "$cur"
    else
        compgen -W "find add remove rm list info" -- "$cur"
    fi
}

_spack_compiler_find () {
    if $list_options
    then
        compgen -W "-h --help --scope" -- "$cur"
    fi
}

_spack_compiler_add () {
    # Alias to `spack compiler find`
    _spack_compiler_find
}

_spack_compiler_remove () {
    if $list_options
    then
        compgen -W "-h --help -a --all --scope" -- "$cur"
    else
        compgen -W "$(_installed_compilers)" -- "$cur"
    fi
}

_spack_compiler_rm () {
    # Alias to `spack compiler remove`
    _spack_compiler_remove
}

_spack_compiler_list () {
    compgen -W "-h --help --scope" -- "$cur"
}

_spack_compiler_info () {
    if $list_options
    then
        compgen -W "-h --help --scope" -- "$cur"
    else
        compgen -W "$(_installed_compilers)" -- "$cur"
    fi
}

_spack_compilers () {
    # Alias to `spack compiler list`
    _spack_compiler_list
}

_spack_concretize () {
    compgen -W "-h --help -f --force" -- "$cur"
}

_spack_config () {
    if $list_options
    then
        compgen -W "-h --help --scope" -- "$cur"
    else
        compgen -W "get blame edit" -- "$cur"
    fi
}

_spack_config_get () {
    if $list_options
    then
        compgen -W "-h --help" -- "$cur"
    else
        compgen -W "compilers mirrors repos packages modules config upstreams" -- "$cur"
    fi
}

_spack_config_blame () {
    if $list_options
    then
        compgen -W "-h --help" -- "$cur"
    else
        compgen -W "compilers mirrors repos packages modules config upstreams" -- "$cur"
    fi
}

_spack_config_edit () {
    if $list_options
    then
        compgen -W "-h --help --print-file" -- "$cur"
    else
        compgen -W "compilers mirrors repos packages modules config upstreams" -- "$cur"
    fi
}

_spack_configure () {
    if $list_options
    then
        compgen -W "-h --help -v --verbose" -- "$cur"
    else
        compgen -W "$(_all_packages)" -- "$cur"
    fi
}

_spack_create () {
    if $list_options
    then
        compgen -W "-h --help --keep-stage -n --name -t --template -r --repo -N --namespace -f --force --skip-editor" -- "$cur"
    fi
}

_spack_deactivate () {
    if $list_options
    then
        compgen -W "-h --help -f --force -v --view -a --all" -- "$cur"
    else
        compgen -W "$(_installed_packages)" -- "$cur"
    fi
}

_spack_debug () {
    if $list_options
    then
        compgen -W "-h --help" -- "$cur"
    else
        compgen -W "create-db-tarball" -- "$cur"
    fi
}

_spack_debug_create_db_tarball () {
    compgen -W "-h --help" -- "$cur"
}

_spack_dependencies () {
    if $list_options
    then
        compgen -W "-h --help -i --installed -t --transitive --deptype -V --no-expand-virtuals" -- "$cur"
    else
        compgen -W "$(_all_packages)" -- "$cur"
    fi
}

_spack_dependents () {
    if $list_options
    then
        compgen -W "-h --help -i --installed -t --transitive" -- "$cur"
    else
        compgen -W "$(_all_packages)" -- "$cur"
    fi
}

_spack_deprecate () {
    if $list_options
    then
        compgen -W "-h --help -y --yes-to-all -d --dependencies -D --no-dependencies -i --install-deprecator -I --no-install-deprecator -l --link-type" -- "$cur"
    else
        compgen -W "$(_all_packages)" -- "$cur"
    fi
}

_spack_dev_build () {
    if $list_options
    then
        compgen -W "-h --help -j --jobs -d --source-path -i --ignore-dependencies -n --no-checksum --keep-prefix --skip-patch -q --quiet -u --until --clean --dirty" -- "$cur"
    else
        compgen -W "$(_all_packages)" -- "$cur"
    fi
}

_spack_diy () {
    if $list_options
    then
        compgen -W "-h --help -j --jobs -d --source-path -i --ignore-dependencies -n --no-checksum --keep-prefix --skip-patch -q --quiet -u --until --clean --dirty" -- "$cur"
    else
        compgen -W "$(_all_packages)" -- "$cur"
    fi
}

_spack_docs () {
    compgen -W "-h --help" -- "$cur"
}

_spack_edit () {
    if $list_options
    then
        compgen -W "-h --help -b --build-system -c --command -d --docs -t --test -m --module -r --repo -N --namespace" -- "$cur"
    else
        compgen -W "$(_all_packages)" -- "$cur"
    fi
}

_spack_env () {
    if $list_options
    then
        compgen -W "-h --help" -- "$cur"
    else
        compgen -W "activate deactivate create remove rm list ls status st loads view" -- "$cur"
    fi
}

_spack_env_activate () {
    if $list_options
    then
        compgen -W "-h --help --sh --csh -v --with-view -V --without-view -d --dir -p --prompt" -- "$cur"
    else
        compgen -W "$(_environments)" -- "$cur"
    fi
}

_spack_env_deactivate () {
    compgen -W "-h --help --sh --csh" -- "$cur"
}

_spack_env_create () {
    if $list_options
    then
        compgen -W "-h --help -d --dir --without-view --with-view" -- "$cur"
    fi
}

_spack_env_remove () {
    if $list_options
    then
        compgen -W "-h --help -y --yes-to-all" -- "$cur"
    else
        compgen -W "$(_environments)" -- "$cur"
    fi
}

_spack_env_rm () {
    # Alias to `spack env remove`
    _spack_env_remove
}

_spack_env_list () {
    compgen -W "-h --help" -- "$cur"
}

_spack_env_ls () {
    # Alias to `spack env list`
    _spack_env_list
}

_spack_env_status () {
    compgen -W "-h --help" -- "$cur"
}

_spack_env_st () {
    # Alias to `spack env status`
    _spack_env_status
}

_spack_env_loads () {
    if $list_options
    then
        compgen -W "-h --help -m --module-type --input-only -p --prefix -x --exclude -r --dependencies" -- "$cur"
    else
        compgen -W "$(_environments)" -- "$cur"
    fi
}

_spack_env_view () {
    if $list_options
    then
        compgen -W "-h --help" -- "$cur"
    else
        compgen -W "regenerate enable disable" -- "$cur"
    fi
}

_spack_extensions () {
    if $list_options
    then
        compgen -W "-h --help -l --long -L --very-long -d --deps -p --paths -s --show -v --view" -- "$cur"
    else
        compgen -W "aspell go-bootstrap go icedtea jdk kim-api lua matlab mofem-cephas octave openjdk perl python r ruby rust tcl yorick" -- "$cur"
    fi
}

_spack_fetch () {
    if $list_options
    then
        compgen -W "-h --help -n --no-checksum -m --missing -D --dependencies" -- "$cur"
    else
        compgen -W "$(_all_packages)" -- "$cur"
    fi
}

_spack_find () {
    if $list_options
    then
        compgen -W "-h --help --format --json -d --deps -p --paths --groups --no-groups -l --long -L --very-long -t --tags -c --show-concretized -f --show-flags --show-full-compiler -x --explicit -X --implicit -u --unknown -m --missing -v --variants -M --only-missing --deprecated --only-deprecated -N --namespace --start-date --end-date" -- "$cur"
    else
        compgen -W "$(_installed_packages)" -- "$cur"
    fi
}

_spack_flake8 () {
    if $list_options
    then
        compgen -W "-h --help -b --base -k --keep-temp -a --all -o --output -r --root-relative -U --no-untracked" -- "$cur"
    fi
}

_spack_gpg () {
    if $list_options
    then
        compgen -W "-h --help" -- "$cur"
    else
        compgen -W "verify trust untrust sign create list init export" -- "$cur"
    fi
}

_spack_gpg_verify () {
    if $list_options
    then
        compgen -W "-h --help" -- "$cur"
    else
        compgen -W "$(installed_packages)" -- "$cur"
    fi
}

_spack_gpg_trust () {
    if $list_options
    then
        compgen -W "-h --help" -- "$cur"
    fi
}

_spack_gpg_untrust () {
    if $list_options
    then
        compgen -W "-h --help --signing" -- "$cur"
    else
        compgen -W "$(_keys)" -- "$cur"
    fi
}

_spack_gpg_sign () {
    if $list_options
    then
        compgen -W "-h --help --output --key --clearsign" -- "$cur"
    else
        compgen -W "$(installed_packages)" -- "$cur"
    fi
}

_spack_gpg_create () {
    if $list_options
    then
        compgen -W "-h --help --comment --expires --export" -- "$cur"
    fi
}

_spack_gpg_list () {
    compgen -W "-h --help --trusted --signing" -- "$cur"
}

_spack_gpg_init () {
    compgen -W "-h --help" -- "$cur"
}

_spack_gpg_export () {
    if $list_options
    then
        compgen -W "-h --help" -- "$cur"
    else
        compgen -W "$(_keys)" -- "$cur"
    fi
}

_spack_graph () {
    if $list_options
    then
        compgen -W "-h --help -a --ascii -d --dot -s --static -i --installed --deptype" -- "$cur"
    else
        compgen -W "$(_all_packages)" -- "$cur"
    fi
}

_spack_help () {
    if $list_options
    then
        compgen -W "-h --help -a --all --spec" -- "$cur"
    else
        compgen -W "$(_subcommands)" -- "$cur"
    fi
}

_spack_info () {
    if $list_options
    then
        compgen -W "-h --help" -- "$cur"
    else
        compgen -W "$(_all_packages)" -- "$cur"
    fi
}

_spack_install () {
    if $list_options
    then
        compgen -W "-h --help --only -u --until -j --jobs --overwrite --keep-prefix --keep-stage --dont-restage --use-cache --no-cache --cache-only --show-log-on-error --source -n --no-checksum -v --verbose --fake --only-concrete -f --file --clean --dirty --test --run-tests --log-format --log-file --help-cdash -y --yes-to-all --cdash-upload-url --cdash-build --cdash-site --cdash-track --cdash-buildstamp" -- "$cur"
    else
        compgen -W "$(_all_packages)" -- "$cur"
    fi
}

_spack_license () {
    if $list_options
    then
        compgen -W "-h --help" -- "$cur"
    else
        compgen -W "list-files verify" -- "$cur"
    fi
}

_spack_license_list_files () {
    compgen -W "-h --help" -- "$cur"
}

_spack_license_verify () {
    compgen -W "-h --help --root" -- "$cur"
}

_spack_list () {
    if $list_options
    then
        compgen -W "-h --help -d --search-description --format --update -t --tags" -- "$cur"
    else
        compgen -W "$(_all_packages)" -- "$cur"
    fi
}

_spack_load () {
    if $list_options
    then
        compgen -W "-h --help -r --dependencies" -- "$cur"
    else
        compgen -W "$(_installed_packages)" -- "$cur"
    fi
}

_spack_location () {
    if $list_options
    then
        compgen -W "-h --help -m --module-dir -r --spack-root -i --install-dir -p --package-dir -P --packages -s --stage-dir -S --stages -b --build-dir -e --env" -- "$cur"
    else
        compgen -W "$(_all_packages)" -- "$cur"
    fi
}

_spack_log_parse () {
    if $list_options
    then
        compgen -W "-h --help --show -c --context -p --profile -w --width -j --jobs" -- "$cur"
    fi
}

_spack_maintainers () {
    if $list_options
    then
        compgen -W "-h --help --maintained --unmaintained -a --all --by-user" -- "$cur"
    else
        compgen -W "$(_all_packages)" -- "$cur"
    fi
}

_spack_mirror () {
    if $list_options
    then
        compgen -W "-h --help -n --no-checksum" -- "$cur"
    else
        compgen -W "create add remove rm set-url list" -- "$cur"
    fi
}

_spack_mirror_create () {
    if $list_options
    then
        compgen -W "-h --help -d --directory -a --all -f --file -D --dependencies -n --versions-per-spec" -- "$cur"
    else
        compgen -W "$(_all_packages)" -- "$cur"
    fi
}

_spack_mirror_add () {
    if $list_options
    then
        compgen -W "-h --help --scope" -- "$cur"
    fi
}

_spack_mirror_remove () {
    if $list_options
    then
        compgen -W "-h --help --scope" -- "$cur"
    else
        compgen -W "$(_mirrors)" -- "$cur"
    fi
}

_spack_mirror_rm () {
    # Alias to `spack mirror remove`
    _spack_mirror_remove
}

_spack_mirror_set_url () {
    if $list_options
    then
        compgen -W "-h --help --push --scope" -- "$cur"
    else
        compgen -W "$(_mirrors)" -- "$cur"
    fi
}

_spack_mirror_list () {
    compgen -W "-h --help --scope" -- "$cur"
}

_spack_module () {
    if $list_options
    then
        compgen -W "-h --help" -- "$cur"
    else
        compgen -W "lmod tcl" -- "$cur"
    fi
}

_spack_module_lmod () {
    if $list_options
    then
        compgen -W "-h --help" -- "$cur"
    else
        compgen -W "refresh find rm loads setdefault" -- "$cur"
    fi
}

_spack_module_lmod_refresh () {
    if $list_options
    then
        compgen -W "-h --help --delete-tree --upstream-modules -y --yes-to-all" -- "$cur"
    else
        compgen -W "$(_installed_packages)" -- "$cur"
    fi
}

_spack_module_lmod_find () {
    if $list_options
    then
        compgen -W "-h --help --full-path -r --dependencies" -- "$cur"
    else
        compgen -W "$(_installed_packages)" -- "$cur"
    fi
}

_spack_module_lmod_rm () {
    if $list_options
    then
        compgen -W "-h --help -y --yes-to-all" -- "$cur"
    else
        compgen -W "$(_installed_packages)" -- "$cur"
    fi
}

_spack_module_lmod_loads () {
    if $list_options
    then
        compgen -W "-h --help --input-only -p --prefix -x --exclude -r --dependencies" -- "$cur"
    else
        compgen -W "$(_installed_packages)" -- "$cur"
    fi

}

_spack_module_lmod_setdefault () {
    if $list_options
    then
        compgen -W "-h --help" -- "$cur"
    else
        compgen -W "$(_installed_packages)" -- "$cur"
    fi
}

_spack_module_tcl () {
    if $list_options
    then
        compgen -W "-h --help" -- "$cur"
    else
        compgen -W "refresh find rm loads" -- "$cur"
    fi
}

_spack_module_tcl_refresh () {
    if $list_options
    then
        compgen -W "-h --help --delete-tree --upstream-modules -y --yes-to-all" -- "$cur"
    else
        compgen -W "$(_installed_packages)" -- "$cur"
    fi
}

_spack_module_tcl_find () {
    if $list_options
    then
        compgen -W "-h --help --full-path -r --dependencies" -- "$cur"
    else
        compgen -W "$(_installed_packages)" -- "$cur"
    fi
}

_spack_module_tcl_rm () {
    if $list_options
    then
        compgen -W "-h --help -y --yes-to-all" -- "$cur"
    else
        compgen -W "$(_installed_packages)" -- "$cur"
    fi
}

_spack_module_tcl_loads () {
    if $list_options
    then
        compgen -W "-h --help --input-only -p --prefix -x --exclude -r --dependencies" -- "$cur"
    else
        compgen -W "$(_installed_packages)" -- "$cur"
    fi
}

_spack_patch () {
    if $list_options
    then
        compgen -W "-h --help -n --no-checksum" -- "$cur"
    else
        compgen -W "$(_all_packages)" -- "$cur"
    fi
}

_spack_pkg () {
    if $list_options
    then
        compgen -W "-h --help" -- "$cur"
    else
        compgen -W "add list diff added changed removed" -- "$cur"
    fi
}

_spack_pkg_add () {
    if $list_options
    then
        compgen -W "-h --help" -- "$cur"
    else
        compgen -W "$(_all_packages)" -- "$cur"
    fi
}

_spack_pkg_list () {
    # FIXME: How to list git revisions?
    if $list_options
    then
        compgen -W "-h --help" -- "$cur"
    fi
}

_spack_pkg_diff () {
    # FIXME: How to list git revisions?
    if $list_options
    then
        compgen -W "-h --help" -- "$cur"
    fi
}

_spack_pkg_added () {
    # FIXME: How to list git revisions?
    if $list_options
    then
        compgen -W "-h --help" -- "$cur"
    fi
}

_spack_pkg_changed () {
    # FIXME: How to list git revisions?
    if $list_options
    then
        compgen -W "-h --help -t --type" -- "$cur"
    fi
}

_spack_pkg_removed () {
    # FIXME: How to list git revisions?
    if $list_options
    then
        compgen -W "-h --help" -- "$cur"
    fi
}

_spack_providers () {
    if $list_options
    then
        compgen -W "-h --help" -- "$cur"
    else
        compgen -W "$(_providers)" -- "$cur"
    fi
}

_spack_pydoc () {
    if $list_options
    then
        compgen -W "-h --help" -- "$cur"
    fi
}

_spack_python () {
    if $list_options
    then
        compgen -W "-h --help -c" -- "$cur"
    fi
}

_spack_reindex () {
    compgen -W "-h --help" -- "$cur"
}

_spack_release_jobs () {
    compgen -W "-h --help -o --output-file -p --print-summary --cdash-credentials" -- "$cur"
}

_spack_remove () {
    if $list_options
    then
        compgen -W "-h --help -a --all -l --list-name -f --force" -- "$cur"
    else
        compgen -W "$(_all_packages)" -- "$cur"
    fi
}

_spack_repo () {
    if $list_options
    then
        compgen -W "-h --help" -- "$cur"
    else
        compgen -W "create list add remove rm" -- "$cur"
    fi
}

_spack_repo_create () {
    if $list_options
    then
        compgen -W "-h --help" -- "$cur"
    fi
}

_spack_repo_list () {
    compgen -W "-h --help --scope" -- "$cur"
}

_spack_repo_add () {
    if $list_options
    then
        compgen -W "-h --help --scope" -- "$cur"
    fi
}

_spack_repo_remove () {
    if $list_options
    then
        compgen -W "-h --help --scope" -- "$cur"
    else
        compgen -W "$(_repos)" -- "$cur"
    fi
}

_spack_repo_rm () {
    # Alias to `spack repo remove`
    _spack_repo_remove
}

_spack_resource () {
    if $list_options
    then
        compgen -W "-h --help" -- "$cur"
    else
        compgen -W "list show" -- "$cur"
    fi
}

_spack_resource_list () {
    compgen -W "-h --help --only-hashes" -- "$cur"
}

_spack_resource_show () {
    if $list_options
    then
        compgen -W "-h --help" -- "$cur"
    else
        compgen -W "$(_all_resource_hashes)" -- "$cur"
    fi
}

_spack_restage () {
    if $list_options
    then
        compgen -W "-h --help" -- "$cur"
    else
        compgen -W "$(_all_packages)" -- "$cur"
    fi
}

_spack_setup () {
    if $list_options
    then
        compgen -W "-h --help -i --ignore-dependencies -n --no-checksum -v --verbose --clean --dirty" -- "$cur"
    else
        compgen -W "$(_all_packages)" -- "$cur"
    fi
}

_spack_spec () {
    if $list_options
    then
        compgen -W "-h --help -l --long -L --very-long -I --install-status -y --yaml -j --json -c --cover -N --namespaces -t --types" -- "$cur"
    else
        compgen -W "$(_all_packages)" -- "$cur"
    fi
}

_spack_stage () {
    if $list_options
    then
        compgen -W "-h --help -n --no-checksum -p --path" -- "$cur"
    else
        compgen -W "$(_all_packages)" -- "$cur"
    fi
}

_spack_test () {
    if $list_options
    then
        compgen -W "-h --help -H --pytest-help --extension -l --list -L --list-long -N --list-names -s -k --showlocals" -- "$cur"
    else
        compgen -W "$(_tests)" -- "$cur"
    fi
}

_spack_uninstall () {
    if $list_options
    then
        compgen -W "-h --help -f --force -R --dependents -y --yes-to-all -a --all" -- "$cur"
    else
        compgen -W "$(_installed_packages)" -- "$cur"
    fi
}

_spack_unload () {
    if $list_options
    then
        compgen -W "-h --help" -- "$cur"
    else
        compgen -W "$(_installed_packages)" -- "$cur"
    fi
}

_spack_upload_s3 () {
    if $list_options
    then
        compgen -W "-h --help" -- "$cur"
    else
        compgen -W "spec index" -- "$cur"
    fi
}

_spack_upload_s3_spec () {
    compgen -W "-h --help -s --spec -y --spec-yaml -b --base-dir -e --endpoint-url" -- "$cur"
}

_spack_upload_s3_index () {
    compgen -W "-h --help -e --endpoint-url" -- "$cur"
}

_spack_url () {
    if $list_options
    then
        compgen -W "-h --help" -- "$cur"
    else
        compgen -W "parse list summary stats" -- "$cur"
    fi
}

_spack_url_parse () {
    if $list_options
    then
        compgen -W "-h --help -s --spider" -- "$cur"
    fi
}

_spack_url_list () {
    compgen -W "-h --help -c --color -e --extrapolation -n --incorrect-name -N --correct-name -v --incorrect-version -V --correct-version" -- "$cur"
}

_spack_url_summary () {
    compgen -W "-h --help" -- "$cur"
}

_spack_url_stats () {
    compgen -W "-h --help" -- "$cur"
}

_spack_verify () {
    if $list_options
    then
        compgen -W "-h --help -l --local -j --json -a --all -s --specs -f --files" -- "$cur"
    else
        compgen -W "$(_all_packages)" -- "$cur"
    fi
}

_spack_versions () {
    if $list_options
    then
        compgen -W "-h --help -s --safe-only" -- "$cur"
    else
        compgen -W "$(_all_packages)" -- "$cur"
    fi
}

_spack_view () {
    if $list_options
    then
        compgen -W "-h --help -v --verbose -e --exclude -d --dependencies" -- "$cur"
    else
        compgen -W "symlink add soft hardlink hard remove rm statlink status check" -- "$cur"
    fi
}

_spack_view_symlink () {
    if $list_options
    then
        compgen -W "-h --help --projection-file -i --ignore-conflicts" -- "$cur"
    fi
}

_spack_view_add () {
    # Alias for `spack view symlink`
    _spack_view_symlink
}

_spack_view_soft () {
    # Alias for `spack view symlink`
    _spack_view_symlink
}

_spack_view_hardlink () {
    if $list_options
    then
        compgen -W "-h --help --projection-file -i --ignore-conflicts" -- "$cur"
    fi
}

_spack_view_hard () {
    # Alias for `spack view hardlink`
    _spack_view_hardlink
}

_spack_view_remove () {
    if $list_options
    then
        compgen -W "-h --help --no-remove-dependents -a --all" -- "$cur"
    fi
}

_spack_view_rm () {
    # Alias for `spack view remove`
    _spack_view_remove
}

_spack_view_statlink () {
    if $list_options
    then
        compgen -W "-h --help" -- "$cur"
    fi
}

_spack_view_status () {
    # Alias for `spack view statlink`
    _spack_view_statlink
}

_spack_view_check () {
    # Alias for `spack view statlink`
    _spack_view_statlink
}

# Helper functions for subcommands

_subcommands () {
    spack commands
}

_all_packages () {
    spack list
}

_all_resource_hashes () {
    spack resource list --only-hashes
}

_installed_packages () {
    spack --color=never find --no-groups
}

_installed_compilers () {
    spack compilers | egrep -v "^(-|=)"
}

_providers () {
    spack providers
}

_mirrors () {
    spack mirror list | awk '{print $1}'
}

_repos () {
    spack repo list | awk '{print $1}'
}

_tests () {
    spack test -l
}

_environments () {
    spack env list
}

_keys () {
    spack gpg list
}

# Testing functions

_test_vars () {
    echo "-----------------------------------------------------"             >> temp
    echo "Full line:                '$COMP_LINE'"                            >> temp
    echo                                                                     >> temp
    echo "Word list w/ flags:       $(_pretty_print COMP_WORDS[@])"          >> temp
    echo "# words w/ flags:         '${#COMP_WORDS[@]}'"                     >> temp
    echo "Cursor index w/ flags:    '$COMP_CWORD'"                           >> temp
    echo                                                                     >> temp
    echo "Word list w/out flags:    $(_pretty_print COMP_WORDS_NO_FLAGS[@])" >> temp
    echo "# words w/out flags:      '${#COMP_WORDS_NO_FLAGS[@]}'"            >> temp
    echo "Cursor index w/out flags: '$COMP_CWORD_NO_FLAGS'"                  >> temp
    echo                                                                     >> temp
    echo "Subfunction:              '$subfunction'"                          >> temp
    if $list_options
    then
        echo "List options:             'True'"  >> temp
    else
        echo "List options:             'False'" >> temp
    fi
    echo "Current word:             '$cur'"  >> temp
    echo "Previous word:            '$prev'" >> temp
}

# Pretty-prints one or more arrays
# Syntax: _pretty_print array1[@] ...
_pretty_print () {
    for arg in $@
    do
        local array=("${!arg}")
        echo -n "$arg: ["
        printf   "'%s'" "${array[0]}"
        printf ", '%s'" "${array[@]:1}"
        echo "]"
    done
}

complete -o default -F _bash_completion_spack spack
