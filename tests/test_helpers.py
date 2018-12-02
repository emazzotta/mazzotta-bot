from src.bot import remove_command


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
