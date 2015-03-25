from __future__ import print_function

from ignoretogether import IgnoreRuleSet

if __name__ == '__main__':
    print('Simulation of commands which would be run on example-ruleset.')
    rs = IgnoreRuleSet('example', 'example-ruleset.yml')
    rs.load()

    print('Ruleset installation.')
    rs.install()

    print('Ruleset uninstallation.')
    rs.uninstall()

