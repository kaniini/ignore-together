# ignore-together

A distributed ignore list engine for IRC.

The idea is essentially that there are users whose behaviours you'd rather not deal with,
ignore-together allows you to preemptively ignore these users if other people you subscribed
to have already ignored them.  This is like the hydra effect, but with the goal of enforcing
good behaviour instead of abusive or anti-social behaviour, by introducing reputation data
to the IRC experience.

This package contains a specification for ignore-list rulesets and an example implementation
for weechat.

## usage (weechat)

This example installs the script and loads my ruleset into the client.

    /script install ignore-together.py
    /ignore-together add http://turtle.dereferenced.org/~kaniini/ignore-together-rules
