from random import random
import re
from hgtk.checker import has_batchim
from ..utils.dictionary import sort_by_key
from ..utils.hangul import create_possible_syllables, is_complete_syllable

# See https://namu.wiki/w/야민정음
raw_yamin_dictionary = {
    # 한글 - 한글 (받침 포함)
    '겨': '저',
    '대': '머',
    '귀': '커',
    '파': '과',
    '피': '끠',
    '끠': '괴',
    '괴': '피',
    '포': '쪼',
    '비': '네',
    '삐': '볘',
    '눠': '부',
    '며': '띠',
    '거': '지',
    '고': '끄',
    '켜': '궈',
    '교': '꼬',
    '티': '더',

    # 한글 - 한글 (받침 미포함)
    '인': '외',
    '유': '윾',
    '위': '읶',
    '우': '윽',
    '굿': '긋',
    '공': '퐁',
    '읍': '윰',
    '왕': '앟',
    '왱': '앻',
    '왓': '앛',
    '왯': '앷',
    '욋': '잋',
    '통': '듷',
    '봉': '넣',
    '두': '득',
    '딘': '되',
    '익': '의',
    '임': '읜',
    '일': '읟',
    '억': '여',
    '백': '뿌',
    '산': '솨',
    '번': '놴',
    '부': '넉',
    '보': '넌',

    '근': 'ㄹ',
    '너': 'ㅂ',
    '든': 'ㅌ',
    '병': 'ㅹ',

    '개새끼': '7H^H77l',
    '대통령': '새토깽',
    '이명박': '어맹뿌',
    '푸틴': '곡틴',

    # 한글 - 영어
    '내': 'LH',
    '배': 'IdH',
    '애': 'OH',
    '야': 'OF',
    '태': 'EH',

    # 한글 - 한자
    '뉘': '爿',
    '몸': '啚',
    '묵': '号',
    '숲': '金',
    '스': '亼',
    '슥': '今',
    '쓰': '丛',
    '조': '丕',
    '크': '彐',
    '튽': '長',
    '표': '丑',
    '푸': '辛',

    # 한글 - 기타문자
    '망': 'ㅁ5',
    '응': '%',
    'ㅋ': 'ヲ',

    # 영어 - 영어
    'I': 'l',
    'cl': 'd',
    'lo': 'b',
    'rn': 'm',

    # 영어 - 기타문자
    'l': '|',
    '|': 'I',
    'EU': '日J',

    # 기타
    '4': 'Ч',

    # 글자 압축
    '구구': '뀨',
    '굴국': '뀱',
    '도도': '뚀',
    '돌돔': '뚊',
    '딘딘': '田',
    '보보': '뾰',
    '복복': '뾲',
    '부부': '쀼',
    '북북': '쀾',
    '불붙': '쁉',
    'ㅅㅂㄹㅁ': '섊',
    '속삭': '쏶',
    '스스': '쓰',
    '스시': '씌',
    '조조': '쪼',
    '존좋': '쬲',
    '주작': '짞',
    '주주': '쮸',

    # 180도 회전
    '근육': '뇽근',
    '눈물': '롬곡',
    '물음표': '표믕롬',
    '육군': '곤뇽',
    '폭풍': '옾눞',
}

yamin_dictionary = raw_yamin_dictionary.copy()

for key, value in raw_yamin_dictionary.items():
    if is_complete_syllable(key) and not has_batchim(key) \
            and is_complete_syllable(value) and not has_batchim(value):
        first_chars = create_possible_syllables(key)
        second_chars = create_possible_syllables(value)
        for i in range(27):
            yamin_dictionary[first_chars[i]] = second_chars[i]

for key, value in yamin_dictionary.copy().items():
    if value not in yamin_dictionary:
        yamin_dictionary[value] = key

yamin_dictionary = sort_by_key(yamin_dictionary, lambda a, b:
                               (1 if len(a[0]) < len(b[0]) else -1) if len(a[0]) != len(b[0])
                               else (-1 if a[0] < b[0] else 1))


def encode_yamin(text: str, *, active_rate=1.0) -> str:
    replaced_tokens = [token for token in yamin_dictionary.keys() if random() < active_rate]
    regex_escaped_tokens = [token.replace('|', '\\|') if '|' in token else token for token in replaced_tokens]
    yamin_match_pattern = f'({"|".join(regex_escaped_tokens)})'
    yamin_match_regex = re.compile(yamin_match_pattern)
    text = re.sub(yamin_match_regex, lambda match: yamin_dictionary[match.group(0)], text)
    return text
