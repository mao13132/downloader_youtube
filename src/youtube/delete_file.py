# ---------------------------------------------
# Program by @developer_telegrams
#
#
# Version   Date        Info
# 1.0       2023    Initial Version
#
# ---------------------------------------------
import os


def delete_file(file_patch):
    try:
        os.remove(file_patch)
    except Exception as es:
        print(f'Не могу удалить файл, ошибка "{es}"')

        return False

    return True
