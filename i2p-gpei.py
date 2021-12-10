"""
    Find out reusable local IP addresses.
"""
import csv
import ipaddress
import sys

import click


def is_broadcast(ip_addr):
    return any((
        '.255' in ip_addr,
        ip_addr.endswith('.0'),
    ))


def ip_range(subnet_mask):
    for ip_addr in ipaddress.IPv4Network(subnet_mask):
        if not is_broadcast(ip_addr.exploded):
            yield ip_addr


@click.command()
@click.argument('subnet')
@click.argument('input', type=click.File('r'))
@click.option('--output', type=click.File('w'), default=sys.stdout,
              help='Output file path.')
def cli(subnet, input, output):
    """
    Iterate non-broadcast IP addresses available in the `SUBNET` network,
    assign them to i2p names from the `INPUT` CSV file.
    """
    reader = csv.reader(input)
    for line, ip_addr in zip(reader, ip_range(subnet)):
        name, *_ = line
        entry = f'address=/{ name }/{ ip_addr }\n'
        output.write(entry)

if __name__ == '__main__':
    cli()
