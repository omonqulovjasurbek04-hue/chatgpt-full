import re

def format_to_html(text: str) -> str:
    text = text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")

    text = re.sub(
        r'```(\w*)\n(.*?)```',
        r'<pre>\2</pre>',
        text, flags=re.DOTALL
    )

    text = re.sub(r'`(.*?)`', r'<code>\1</code>', text)

    text = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', text, flags=re.DOTALL)

    text = re.sub(r'\*(.*?)\*', r'<i>\1</i>', text, flags=re.DOTALL)

    text = re.sub(r'^###\s+(.*?)$', r'<b>\1</b>', text, flags=re.MULTILINE)

    text = re.sub(r'^##\s+(.*?)$', r'<b>\1</b>', text, flags=re.MULTILINE)

    text = re.sub(r'^#\s+(.*?)$', r'<b>\1</b>', text, flags=re.MULTILINE)

    text = re.sub(r'\[(.*?)\]\((.*?)\)', r'<a href="\2">\1</a>', text)

    return text
