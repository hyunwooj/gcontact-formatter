gcontact-formatter
==================

문제
----

주소록에 있는 전화번호의 포멧이 각기 다름.

1. 국가번호 지정 여부
2. 구분자 지정 여부 혹은 그 종류 ('-', ' ', '')


해결방법
--------

1. [gdata][]로 전화번호 목록 가져옴.
2. 한국번호와 미국번호를 정규식으로 분류함.
3. [phonenumbers][]를 이용해 포멧팅.
4. [gdata][]로 변경된 전화번호 업데이트.

[gdata]:https://pypi.python.org/pypi/gdata/
[phonenumbers]:https://pypi.python.org/pypi/phonenumbers
