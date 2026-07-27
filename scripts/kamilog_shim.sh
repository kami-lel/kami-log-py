################################################################################
# kamilog_shim
# lets scripts call `kamilog` safely even when it is not installed
# shipped with kamilog v2.9.1, q.v. https://github.com/kami-lel/kamilog
################################################################################
# FIXME better wording
_KAMILOG_BIN="$(type -P kamilog 2>/dev/null || true)"

kamilog() {
    if [ -n "$_KAMILOG_BIN" ]; then
        "$_KAMILOG_BIN" "$@"
        return
    fi
    case "$1" in
        cb|cb0)
            printf '# %s' "$(cat)"
            ;;
        logger)
            printf '%s:\t%s' "$2" "$(cat)"
            ;;
        *)
            cat  # no bin found, pass stdin through as-is
            ;;
    esac
}
# END of kamilog_shim  #########################################################