# ignore-together.py - a distributed ignore list engine for IRC.

from __future__ import print_function

import sys
import yaml

try:
    import weechat
except:
    class FakeWeechat:
        def command(self, cmd):
            print(cmd)
     weechat = FakeWeechat()


class IgnoreRule:
    """An ignore rule.
    This provides instrumentation for converting ignore rules into weechat filters.
    It handles both types of ignore-together ignore rules.
    """
    def __init__(self, ignorelist, rulename, typename='ignore', hostmasks=[], accountnames=[], patterns=[]):
        self.ignorelist = ignorelist
        self.rulename = rulename
        self.typename = typename
        self.hostmasks = hostmasks
        self.accountnames = accountnames
        self.patterns = patterns

    def install(self):
        "Install an ignore rule."
        subrule_ctr = 0
        if self.typename == 'ignore':
            for pattern in self.hostmasks:
                weechat.command('/filter add ignore-together.{ignorelist}.{rulename}.{ctr} irc.* * {pattern}'.format(
                    ignorelist=self.ignorelist.name, rulename=self.rulename, ctr=subrule_ctr, pattern=pattern)
                subrule_ctr++
            # XXX - accountnames
        elif self.typename == 'message':
            for pattern in self.patterns:
                weechat.command('/filter add ignore-together.{ignorelist}.{rulename}.{ctr} irc.* * {pattern}'.format(
                    ignorelist=self.ignorelist.name, rulename=self.rulename, ctr=subrule_ctr, pattern=pattern)
                subrule_ctr++

    def uninstall(self):
        "Uninstall an ignore rule."
        subrule_ctr = 0
        if self.typename == 'ignore':
            for pattern in self.hostmasks:
                weechat.command('/filter del ignore-together.{ignorelist}.{rulename}.{ctr}'.format(
                    ignorelist=self.ignorelist.name, rulename=self.rulename, ctr=subrule_ctr)
                subrule_ctr++
        elif self.typename == 'message':
            for pattern in self.patterns:
                weechat.command('/filter del ignore-together.{ignorelist}.{rulename}.{ctr}'.format(
                    ignorelist=self.ignorelist.name, rulename=self.rulename, ctr=subrule_ctr)
                subrule_ctr++


class IgnoreRuleSet:
    """A downloaded collection of rules.
    Handles merging updates vs current state, and so on."""
    def __init__(self, name, uri):
        self.name = name
        self.uri = uri

