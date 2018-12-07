from ..helpers import WikiStringHelper, KanaHelper

import pytest

testdata_short_description = [
	('<ul><li><b>Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod</b></li></ul>','<ul><li><b>Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed</b></li></ul>',60),
	('<ul><li>first list, first element</li></ul>some text before the paragraph<p>paragraph</p><ul><li>second list first element</li></ul>', '<ul><li>first list, first element</li></ul>some text before the paragraph<p>parag</p>', 60),
	('<h2>Basic HTML Table</h2><table><tr><th>Firstname</th><th>Age</th></tr><tr><td>Jill</td><td>50</td></tr><tr><td>Eve</td><td>94</td></tr><tr><td>John</td><td>Doe</td></tr></table>', '<h2>Basic HTML Table</h2><table><tr><th>Firstname</th><th>Age</th></tr><tr><td>Ji</td></tr></table>', 30),
	('Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor', 'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor', 80),
	('<h2>Basic HTML Table</h2><table><tr><th>Firstname</th><th>Age</th></tr><tr><td>Jill</td><td>50</td></tr><tr><td>Eve</td><td>94</td></tr><tr><td>John</td><td>Doe</td></tr></table>', '<h2>Basic HTML Table</h2><table><tr><th>Firstname</th><th>Age</th></tr><tr><td>Jill</td><td>50</td></tr><tr><td>Eve</td><td>94</td></tr><tr><td>John</td><td>Doe</td></tr></table>', 60),
	('<div attr1="zalupa" attr2="huj">ночь пришла, а за ней гроза. Грустный дождь да ветер шутник.</div>', '<div attr1="zalupa" attr2="huj">ночь пришл</div>', 10)
]

testdata_remove_tags = [
	('<br/>text<h1>header</h1><p>paragraph text</p>again plain text<br/>and<div style="width:10px;">div with styling</div>', 'textheaderparagraph textagain plain textanddiv with styling')
]

testdata_rus_to_hiragana = [
	('дэванайдэсу', 'でわないです'), ('кацумото', 'かつもと'), ('тётта', 'ちょった'),
	('а', 'あ'), ('ауёо', 'あうよお'), ('каки', 'かき'), ('сёгун', 'しょぐん'),
	('гамбару', 'がんばる'), ('дзюнитаки', 'じゅにたき'), ('дакутэн', 'だくてん'),
	('коохии', 'こうひい'), ('яСУМИ', 'やすみ'), ('киССАТЭН', 'きっさてん'), ('дзё:ДЗУ', 'じょえず'),
	('аТАРАСИй', 'あたらしい'), ('дэНВАБАнго:', 'でんわばんごう'), ('ниой', 'におい'), ('ниппон', 'にっぽん')
]

testdata_rus_to_katakana = [
	('дэванайдэсу', 'デワナイデス'), ('кацумото', 'カツモト'), ('тётта', 'チョンタ'),
	('а', 'ア'), ('ауёо', 'アウヨオ'), ('каки', 'カキ'), ('сёгун', 'ショグン'),
	('гамбару', 'ガンバル'), ('дзюнитаки', 'ジュニタキ'), ('дакутэн', 'ダクテン'),
	('коохии', 'コーヒー'), ('яСУМИ', 'ヤスミ'), ('киССАТЭН', 'キンサテン'), ('дзё:ДЗУ', 'ジョーズ'),
	('аТАРАСИй', 'アタラシイ'), ('дэНВАБАнго:', 'デンワバンゴー'), ('ниой', 'ニオイ'), ('ниппон', 'ニンポン')
]

@pytest.mark.parametrize("html,expected_short_description,pure_length", testdata_short_description)
def test_short_description(html, expected_short_description, pure_length):
	actual_short_description = WikiStringHelper.get_article_short_description(html, pure_length)

	assert expected_short_description == actual_short_description

@pytest.mark.parametrize("tagged_string,expected_output", testdata_remove_tags)
def test_remove_tags_from_string(tagged_string, expected_output):
	actual_string = WikiStringHelper.remove_tags_from_string(tagged_string)

	assert expected_output == actual_string

@pytest.mark.parametrize("rus_transcription,expected_hiragana", testdata_rus_to_hiragana)
def test_rus_to_hiragana(rus_transcription, expected_hiragana):
	actual_hiragana = KanaHelper.rus_to_hiragana(rus_transcription)

	assert expected_hiragana == actual_hiragana

@pytest.mark.parametrize("rus_transcription,expected_katakana", testdata_rus_to_katakana)
def test_rus_to_katakana(rus_transcription, expected_katakana):
	actual_katakana = KanaHelper.rus_to_katakana(rus_transcription)

	assert expected_katakana == actual_katakana