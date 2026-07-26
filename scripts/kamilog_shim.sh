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
    # no bin found, pass stdin through as-is
    cat
    # BUG newline handling is wrong
}
# END of kamilog_shim  #########################################################