# ignore-together.py - a distributed ignore list engine for IRC.

from __future__ import print_function

import os
import sys
import yaml

weechat_is_fake = False

try:
    import weechat
except:
    class FakeWeechat:
        def command(self, cmd):
            print(cmd)
    weechat = FakeWeechat()
    weechat_is_fake = True


class IgnoreRule:
    """An ignore rule.
    This provides instrumentation for converting ignore rules into weechat filters.
    It handles both types of ignore-together ignore rules.
    """
    def __init__(self, ignorelist, rulename, rationale, typename='ignore', hostmasks=[], accountnames=[], patterns=[]):
        self.ignorelist = ignorelist
        self.rulename = rulename.replace(' ', '_')
        self.rationale = rationale
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
                    ignorelist=self.ignorelist.name, rulename=self.rulename, ctr=subrule_ctr, pattern=pattern))
                subrule_ctr += 1
            # XXX - accountnames
        elif self.typename == 'message':
            for pattern in self.patterns:
                weechat.command('/filter add ignore-together.{ignorelist}.{rulename}.{ctr} irc.* * {pattern}'.format(
                    ignorelist=self.ignorelist.name, rulename=self.rulename, ctr=subrule_ctr, pattern=pattern))
                subrule_ctr += 1

    def uninstall(self):
        "Uninstall an ignore rule."
        subrule_ctr = 0
        if self.typename == 'ignore':
            for pattern in self.hostmasks:
                weechat.command('/filter del ignore-together.{ignorelist}.{rulename}.{ctr}'.format(
                    ignorelist=self.ignorelist.name, rulename=self.rulename, ctr=subrule_ctr))
                subrule_ctr += 1
        elif self.typename == 'message':
            for pattern in self.patterns:
                weechat.command('/filter del ignore-together.{ignorelist}.{rulename}.{ctr}'.format(
                    ignorelist=self.ignorelist.name, rulename=self.rulename, ctr=subrule_ctr))
                subrule_ctr += 1


class IgnoreRuleSet:
    """A downloaded collection of rules.
    Handles merging updates vs current state, and so on."""
    def __init__(self, name, uri):
        self.name = name
        self.uri = uri
        self.rules = []

    def load(self):
        def build_rules(s):
            for k, v in s.items():
                self.rules.append(IgnoreRule(self, k, v.get('rationale', '???'), v.get('type', 'ignore'), v.get('hostmasks', []), v.get('accountnames', []), v.get('patterns', [])))
        def test_load_cb(payload):
            build_rules(yaml.load(payload))
        if weechat_is_fake:
            d = open(self.uri, 'r')
            return test_load_cb(d.read())

    def install(self):
        [r.install() for r in self.rules]

    def uninstall(self):
        [r.uninstall() for r in self.rules]


rules = {}

