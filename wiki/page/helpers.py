""" Contains helper classes and methods for the page app """
import re

class WikiStringHelper:
	""" Contains functions for handling string-related cases """
	def get_article_short_description(html, pure_length):
		"""
		Gets an html string and calculates the length for short description
		Short description length = pure text length + all the tags that are in between
		"""

		pure_length_used = 0
		full_length = 0
		open_tag = False
		short_description = ''

		html = html.replace("<br/>", "").replace("<br>","")

		# do this check after regex removing all tags
		if len(WikiStringHelper.remove_tags_from_string(html)) <= pure_length:
			return html

		open_tags = []

		while full_length < pure_length:
			if html[0] is '<':
				closing_brace_index = html.find(">")
				if html[1] is '/':
					tag_name = html[2:closing_brace_index]
					open_tags.remove(tag_name)
					short_description += html[:closing_brace_index+1]
				else:
					short_description += html[:closing_brace_index+1]
					tag_name = html[1:closing_brace_index]
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

# take pure_length substring
# using regex find all <.*> and </.*> matches in the substr
# while there are elements in </.*> matches
# 	find according </.*> match, remove both
# add closing tags for all remaining <.*> matches



# go through chars 1 by 1
# if <.*> encountered - mem it
# if </.*> encountered - forget according <.*> match
# if normal char encountered - count it and continue
# do while counter < pure_length