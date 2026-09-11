"""Check representative destinations using the README's rule ordering."""
from pathlib import Path


def rules(client, name):
    ext = 'list' if client == 'Shadowrocket' else 'yaml'
    lines = Path(f'rule/{client}/{name}/{name}.{ext}').read_text().splitlines()
    return [line.strip().removeprefix('- ').split(',', 1) for line in lines
            if line.strip().removeprefix('- ').startswith('DOMAIN')]


def matches(host, rule):
    kind, value = rule
    if kind == 'DOMAIN':
        return host == value
    if kind == 'DOMAIN-SUFFIX':
        return host == value or host.endswith('.' + value)
    if kind == 'DOMAIN-KEYWORD':
        return value in host
    raise AssertionError(f'Unsupported rule: {rule}')


proxy = [
    'stock.adobe.com', 'contributor.stock.adobe.com', 'stock.adobe.io',
    'adobestock.com', 'www.fotolia.com', 'as1.ftcdn.net', 'audios.ftcdn.net',
    'slp-statics.astockcdn.net', 'stock-landing-pages.adobe.io',
    'fotolia-prod-templates.s3.amazonaws.com',
    'stock-apex-images-prod-ew1.s3.eu-west-1.amazonaws.com',
    'firefly.adobe.com', 'www.behance.net',
]
direct = ['account.adobe.com', 'ims-na1.adobelogin.com', 'fonts.adobe.com',
          'creativecloud.com', 'cc-api-storage.adobe.io', 'helpx.adobe.com']
unmatched = ['unrelated.s3.amazonaws.com', 'unrelated.cloudfront.net',
             'notftcdn.net', 'ftcdn.net.example.org', 'stock.adobe.com.example.org']

for client in ['Shadowrocket', 'Mihomo']:
    for groups in [['AdobeProxy'], ['AdobeAI', 'Behance', 'AdobeStock']]:
        ordered = [(rule, 'PROXY') for name in groups for rule in rules(client, name)]
        ordered += [(rule, 'DIRECT') for rule in rules(client, 'AdobeDirect')]
        for expected, hosts in [('PROXY', proxy), ('DIRECT', direct), (None, unmatched)]:
            for host in hosts:
                actual = next((policy for rule, policy in ordered if matches(host, rule)), None)
                assert actual == expected, (client, groups, host, expected, actual)
    assert {tuple(r) for r in rules(client, 'AdobeProxy')} == {
        tuple(r) for name in ['AdobeAI', 'Behance', 'AdobeStock'] for r in rules(client, name)
    }
    for name in ['AdobeAI', 'Behance', 'AdobeStock', 'AdobeProxy', 'AdobeDirect']:
        assert rules('Shadowrocket', name) == rules('Mihomo', name), name
print('PASS: 96 routing scenarios; merged/split policies and client parity verified.')
