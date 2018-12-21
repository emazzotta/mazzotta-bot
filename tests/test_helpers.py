from src.bot import remove_command, extract_language_and_text


def should_correctly_remove_bot_prefix():
    assert remove_command('/say') == ''
    assert remove_command('/say hello') == 'hello'
    assert remove_command('/say@') == ''
    assert remove_command('/say@ hello') == 'hello'
    assert remove_command('/say@file') == ''
    assert remove_command('/say@file hello') == 'hello'
    assert remove_command('/say@file_transfer_bot') == ''
    assert remove_command('/say@file_transfer_bot hello') == 'hello'
    assert remove_command('/say@file_transfer_bot ') == ''
    assert remove_command('/say@file_transfer_bot hello') == 'hello'


def should_correctly_recognize_language_and_text():
    assert extract_language_and_text('hello') == ('en', 'hello')
    assert extract_language_and_text('lang=fr hello') == ('fr', 'hello')
    assert extract_language_and_text('lang=frhello') == ('fr', 'hello')
    assert extract_language_and_text('lang=it hello') == ('it', 'hello')
