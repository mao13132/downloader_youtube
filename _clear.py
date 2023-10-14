# ---------------------------------------------
# Program by @developer_telegrams
#
#
# Version   Date        Info
# 1.0       2023    Initial Version
#
# ---------------------------------------------

async def _clear():
    import os

    _dir = 'down'

    if os.path.exists(_dir):
        try:
            test = [os.remove(os.path.join(os.path.dirname(__file__), _dir, x)) for x in os.listdir(_dir)]
        except:
            return False

        return True

    return False