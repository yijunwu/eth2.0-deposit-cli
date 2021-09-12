import sys
import click

from eth2deposit.cli.existing_mnemonic import existing_mnemonic
from eth2deposit.cli.new_mnemonic import new_mnemonic
from eth2deposit.cli.existing_mnemonic_partial import (
    find_valid_mnemonics,
    existing_mnemonic_partial)
from eth2deposit.utils.constants import (
    WORD_LISTS_PATH,
)

def check_python_version() -> None:
    '''
    Checks that the python version running is sufficient and exits if not.
    '''
    if sys.version_info < (3, 7):
        click.pause('Your python version is insufficient, please install version 3.7 or greater.')
        sys.exit()


@click.group()
def cli() -> None:
    pass


cli.add_command(existing_mnemonic)
cli.add_command(new_mnemonic)
cli.add_command(existing_mnemonic_partial)


if __name__ == '__main__':
    check_python_version()
    mnemonic = 'humor square core remember flower cradle morning travel search shield olive sphere winner syrup average argue swim mus march toddler trial trap blood enforc'
    print(find_valid_mnemonics(mnemonic, 'english', WORD_LISTS_PATH))
    cli()
