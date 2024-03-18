from typing import List


def not_in(list_src: List[str], list_compare: List[str]):
    return [x for x in list_src if x not in list_compare]
