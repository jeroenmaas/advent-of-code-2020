import re

with open('day19.txt') as f:
    input = f.read().strip().split('\n\n')

def parse_lookups(text):
    return list(map(lambda a: int(a), text.split(' ')))

rules_input = input[0].split('\n')
to_test = input[1].split('\n')

rules = {}
for r in rules_input:
    rule_definition = r.split(': ')[1]

    if '|' in rule_definition:
        type = 'or'
        part1 = rule_definition.split(' | ')[0]
        part2 = rule_definition.split(' | ')[1]
        value = [parse_lookups(part1), parse_lookups(part2)]
    elif '"' in rule_definition:
        type = 'letter'
        value = rule_definition.replace('"', '')
    else:
        type = 'lookup'
        value = parse_lookups(rule_definition)

    rules[int(r.split(':')[0])] = {
        'type': type,
        'value': value
    }

def test_rule(rule, text):
    type = rule['type']
    value = rule['value']
    if type == 'letter':
        return [text[0] == value, text[1:]]
    elif type == 'lookup':
        text_left = text
        for i, v in enumerate(value):
            match, text_left = test_rule(rules[v], text_left)
            if not match:
                return [False, ""]
        return [True, text_left]
    elif type == 'or':
        for lookups in value:
            match, text_left = test_rule({'type': 'lookup', 'value': lookups}, text)
            if match:
                return [match, text_left]

        return [False, ""]
    else:
        print('unknown type')
        exit()

c = 0
for t in to_test:
    match, left = test_rule(rules[0], t)
    if match and len(left) == 0:
        c += 1

print('part1: ' + str(c))
