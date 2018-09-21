import re

class WikiStringHelper:
	def get_article_short_description(html, pure_length):
		"""
		Gets an html string and calculates the length for short description
		Short description length = pure text length + all the tags that are in between
		"""
		pure_length_used = 0
		full_length = 0
		is_tag = False
		open_tag = False
		short_description = ''

		if len(html) < pure_length:
			pure_length = len(html) - 1

		while pure_length_used <= pure_length:
			if html[full_length] is '<':
				is_tag = True
				open_tag = True
			elif html[full_length] is '>':
				if html[full_length - 1] is '/':
					open_tag = False
				is_tag = False
			else:
				pure_length_used += 1
			full_length += 1

		if open_tag is True:
			# last tag is still open - remove it
			short_description = html[: full_length]
			short_description = html[: short_description.rindex('<')] + html[short_description.rindex('>') + 1 : full_length]
		else:
			short_description = html[: full_length - 1]

		return short_description