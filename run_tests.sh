set -ev
./node_modules/karma/bin/karma start --browsers NodeWebkitTravis \
test/karma.conf.js \
--single-run --log-level=debug
exit
