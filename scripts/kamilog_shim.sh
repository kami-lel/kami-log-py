
# Todo link to the github project


################################################################################
# kamilog_shim
# lets scripts call `kamilog` safely even when it is not installed
################################################################################
_KAMILOG_BIN="$(type -P kamilog 2>/dev/null || true)"

kamilog() {
    if [ -n "$_KAMILOG_BIN" ]; then
        "$_KAMILOG_BIN" "$@"
        return
    fi
    case "$1" in
        cb|cb0)
            printf '# %s\n' "$(cat)"
            ;;
        logger)
            printf '%s:\t%s\n' "$2" "$(cat)"
            ;;
        *)
            cat  # no bin found, pass stdin through as-is
            ;;
    esac
}
# END of kamilog_shim  #########################################################