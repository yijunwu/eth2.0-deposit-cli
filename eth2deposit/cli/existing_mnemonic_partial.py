import itertools

import click
from typing import (
    Sequence, List)

from eth2deposit.key_handling.key_derivation.mnemonic import (
    get_languages,
    _get_word_list, _word_to_index, _uint11_array_to_uint, _get_checksum)
from eth2deposit.utils.constants import (
    WORD_LISTS_PATH,
)

languages = get_languages(WORD_LISTS_PATH)


@click.command(
    help='Generate (or recover) keys from an existing mnemonic',
)
@click.pass_context
@click.option(
    '--mnemonic',
    help=('The mnemonic that you used to generate your keys. (It is recommended not to use this argument, and wait for '
          'the CLI to ask you for your mnemonic as otherwise it will appear in your shell history.)'),
    prompt='Please enter your mnemonic separated by spaces (" ")',
    required=True,
    type=str,
)
@click.option(
    '--mnemonic_language',
    default='english',
    help='The language that your (partial) mnemonic is in.',
    prompt='Please choose your mnemonic language',
    type=click.Choice(languages, case_sensitive=False),
)
def existing_mnemonic_partial(ctx: click.Context, mnemonic: str, mnemonic_language: str) -> None:
    print(find_valid_mnemonics(mnemonic, mnemonic_language, WORD_LISTS_PATH))


def find_valid_mnemonics(mnemonic: str, language: str, words_path: str) -> List[List[str]]:
    """
    Given a mnemonic, verify it against its own checksum."
    """
    result = []

    try:
        word_list = _get_word_list(language, words_path)
        mnemonic_list = mnemonic.split(' ')
        if len(mnemonic_list) not in range(12, 25, 3):
            return []
        word_lists = [_word_prefix_to_word_list(word_list, prefix) for prefix in mnemonic_list]
        word_lists_expanded = list(map(lambda s: list(s), itertools.product(*word_lists)))
        for word_list2 in word_lists_expanded:
            word_indices = [_word_to_index(word_list, word) for word in word_list2]
            mnemonic_int = _uint11_array_to_uint(word_indices)
            checksum_length = len(mnemonic_list) // 3
            checksum = mnemonic_int & 2**checksum_length - 1
            entropy = (mnemonic_int - checksum) >> checksum_length
            entropy_bits = entropy.to_bytes(checksum_length * 4, 'big')
            if _get_checksum(entropy_bits) == checksum:
                result.append(word_list2)
    except ValueError:
        pass
    return result


def _word_prefix_to_word_list(word_list: Sequence[str], prefix: str) -> Sequence[str]:
    result = list(filter(lambda s: s.startswith(prefix), word_list))
    if not result:
        raise ValueError('No word in BIP39 word-list starts with prefix %s' % prefix)
    return result
