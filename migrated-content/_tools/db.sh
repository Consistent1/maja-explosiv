#!/usr/bin/env bash
# Single source of truth for how this migration talks to the database.
#
# --default-character-set=latin1 is REQUIRED. The dump's double-encoding was undone
# on import, so the stored bytes ARE correct UTF-8. Connecting as utf8 re-introduces
# mojibake. See content-migration-plan.md §2.3.
#
# stderr is filtered for the password warning ONLY. Real errors must reach the caller
# and must fail the pipeline -- a suppressed error is how a stage passes on no data.
set -o pipefail
mysql -u maja -pmaja usr_p51487_2 --default-character-set=latin1 "$@" \
  2> >(grep -v '^mysql: \[Warning\] Using a password' >&2)
status=$?
exit $status
