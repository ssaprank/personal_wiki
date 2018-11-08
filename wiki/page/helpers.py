""" Contains helper classes and methods for the page app """
import re

class WikiStringHelper:
	""" Contains functions for handling string-related cases """
	def get_article_short_description(html, pure_length):
		"""
		Gets an html string and returns the substr of it, consisting of
		pure_length number of chars + tags that come in between
		"""
		pure_length_used = 0
		full_length = 0
		open_tag = False
		short_description = ''

		html = html.replace("<br/>", "").replace("<br>","").replace("<hr>","")

		# do this check after regex removing all tags
		if len(WikiStringHelper.remove_tags_from_string(html)) <= pure_length:
			return html

		open_tags = []

		while full_length < pure_length:
			if html[0] is '<':
				closing_brace_index = html.find(">")
				next_space_index = html.find(" ")
				if html[1] is '/':
					tag_name = html[2:closing_brace_index]
					open_tags.remove(tag_name)
					short_description += html[:closing_brace_index+1]
				else:
					short_description += html[:closing_brace_index+1]

					tag_name_index = min(closing_brace_index, next_space_index) \
						if next_space_index > -1 \
							else closing_brace_index

					tag_name = html[1:tag_name_index]
					open_tags.append(tag_name)
				html = html[closing_brace_index+1:]
			else:
				short_description += html[0]
				full_length += 1
				html = html[1:]

		for tag in reversed(open_tags):
			short_description += "</" + tag + ">"

		return short_description

	def remove_tags_from_string(input):
		return re.sub(r"<\/?[^<>]+>", "", input)

class KanaHelper:
	def rus_to_hiragana(string):
		string = string.strip()
		output = ''

		while(len(string) > 0):
			c = string[0]
			polivanov_row = POLIVANOV_SYSTEM.get(c, '')

			if polivanov_row == '':
				#todo raise exception
				return output

			if isinstance(polivanov_row, dict):
				cc = string[1]

				if cc == c:
					# consonant doubling - handle it with appropriate symbol
					pass

				polivanov_col = polivanov_row.get(cc, '')

				if polivanov_col == '':
					#todo raise exception
					return output

				output += polivanov_col[0]
				string = string[2:]
			else:
				output += polivanov_row[0]
				string = string[1:]

		return output

# дз* символы
# н
# удвоение согл и гл
POLIVANOV_SYSTEM = {
	'а' : ['あ', 'ア'],
	'и' : ['い', 'イ'],
	'у' : ['う', 'ウ'],
	'э' : ['え', 'エ'],
	'о' : ['お', 'オ'],
	'я' : ['や', 'ヤ'],
	'ю' : ['ゆ', 'ユ'],
	'ё' : ['よ', 'ヨ'],
	'к' : {'а' : ['か', 'カ'], 'и' : ['き', 'キ'], 'у' : ['く', 'ク'], 'э' : ['け', 'ケ'], 'о' : ['こ', 'コ'], 'я' : ['きゃ', 'キャ'], 'ю' : ['きゅ', 'キュ'], 'ё' : ['きょ', 'キョ']},
	'г' : {'а' : ['が', 'ガ'], 'и' : ['ぎ', 'ギ'], 'у' : ['ぐ', 'グ'], 'э' : ['げ', 'ゲ'], 'о' : ['ご', 'ゴ'], 'я' : ['ぎゃ', 'ギャ'], 'ю' : ['ぎゅ', 'ギュ'], 'ё' : ['ぎょ', 'ギョ']},
	'с' : {'а' : ['さ', 'サ'], 'и' : ['し', 'シ'], 'у' : ['す', 'ス'], 'э' : ['せ', 'セ'], 'о' : ['そ', 'ソ'], 'я' : ['しゃ', 'シャ'], 'ю' : ['しゅ', 'シュ'], 'ё' : ['しょ', 'ショ']},
	'дз': {'а' : ['ざ', 'ザ'], 'и' : ['じ', 'ジ'], 'у' : ['ず', 'ズ'], 'э' : ['ぜ', 'ゼ'], 'о' : ['ぞ', 'ゾ'], 'я' : ['じゃ', 'ジャ'], 'ю' : ['じゅ', 'ジュ'], 'ё' : ['じょ', 'ジョ']},
	'т' : {'а' : ['た', 'タ'], 'и' : ['ち', 'チ'], 'э' : ['て', 'テ'], 'о' : ['と', 'ト'], 'я' : ['ちゃ', 'チャ'], 'ю' : ['ちゅ', 'チュ'], 'ё' : ['ちょ', 'チョ']},
	'ц' : {'у' : ['つ', 'ツ']},
	'д' : {'а' : ['だ', 'ダ'], 'зи' : ['ぢ', 'ヂ'], 'зу' : ['づ', 'ヅ'], 'э' : ['で', 'デ'], 'о' : ['ど', 'ド'], 'зя' : ['ぢゃ', 'ヂャ'], 'зю' : ['ぢゅ', 'ヂュ'], 'зё' : ['ぢょ', 'ヂョ']},
	'н' : {'н' : ['ん', 'ン'], 'а' : ['な', 'ナ'], 'и' : ['に', 'ニ'], 'у' : ['ぬ', 'ヌ'], 'э' : ['ね', 'ネ'], 'о' : ['の', 'ノ'], 'я' : ['にゃ', 'ニャ'], 'ю' : ['にゅ', 'ニュ'], 'ё' : ['にょ', 'ニョ']},
	'х' : {'а' : ['は', 'ハ'], 'и' : ['ひ', 'ヒ'], 'э' : ['へ', 'へ'], 'о' : ['ほ', 'ホ'], 'я' : ['ひゃ', 'ヒャ'], 'ю' : ['ひゅ', 'ヒュ'], 'ё' : ['ひょ', 'ヒョ']},
	'ф' : {'у' : ['ふ', 'フ']},
	'б' : {'а' : ['ば', 'バ'], 'и' : ['び', 'ビ'], 'у' : ['ぶ', 'ブ'], 'э' : ['べ', 'べ'], 'о' : ['ぼ', 'ボ'], 'я' : ['びゃ', 'ビャ'], 'ю' : ['びゅ', 'ビュ'], 'ё' : ['びょ', 'ビョ']},
	'п' : {'а' : ['ぱ', 'パ'], 'и' : ['ぴ', 'ピ'], 'у' : ['ぷ', 'プ'], 'э' : ['ぺ', 'ぺ'], 'о' : ['ぽ', 'ポ'], 'я' : ['ぴゃ', 'ピャ'], 'ю' : ['ぴゅ', 'ピュ'], 'ё' : ['ぴょ', 'ピョ']},
	'м' : {'а' : ['ま', 'マ'], 'и' : ['み', 'ミ'], 'у' : ['む', 'ム'], 'э' : ['め', 'メ'], 'о' : ['も', 'モ'], 'я' : ['みゃ', 'ミャ'], 'ю' : ['みゅ', 'ミュ'], 'ё' : ['みょ', 'ミョ']},
	'р' : {'а' : ['ら', 'ラ'], 'и' : ['り', 'リ'], 'у' : ['る', 'ル'], 'э' : ['れ', 'レ'], 'о' : ['ろ', 'ロ'], 'я' : ['りゃ', 'リャ'], 'ю' : ['りゅ', 'リュ'], 'ё' : ['りょ', 'リョ']},
	'в' : {'а' : ['わ', 'ワ'], 'о' : ['を', 'ヲ']}
}
