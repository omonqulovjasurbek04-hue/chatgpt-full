import re


def format_to_html(text: str) -> str:
    """Markdown matnni Telegram HTML formatiga aylantirish"""

    # HTML maxsus belgilarini qochirish
    text = text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")

    # ```code block``` -> <pre> (avval kod bloklarni ajratamiz)
    text = re.sub(
        r'```(\w*)\n(.*?)```',
        r'<pre>\2</pre>',
        text, flags=re.DOTALL
    )

    # `inline code` -> <code>
    text = re.sub(r'`(.*?)`', r'<code>\1</code>', text)

    # **qalin matn** -> <b> (TUZATILDI: oldin <i> edi!)
    text = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', text, flags=re.DOTALL)

    # *kursiv matn* -> <i>
    text = re.sub(r'\*(.*?)\*', r'<i>\1</i>', text, flags=re.DOTALL)

    # ### Sarlavha -> <b>
    text = re.sub(r'^###\s+(.*?)$', r'<b>\1</b>', text, flags=re.MULTILINE)

    # ## Sarlavha -> <b>
    text = re.sub(r'^##\s+(.*?)$', r'<b>\1</b>', text, flags=re.MULTILINE)

    # # Sarlavha -> <b>
    text = re.sub(r'^#\s+(.*?)$', r'<b>\1</b>', text, flags=re.MULTILINE)

    # [matn](url) -> <a href="url">matn</a>
    text = re.sub(r'\[(.*?)\]\((.*?)\)', r'<a href="\2">\1</a>', text)

    return text
