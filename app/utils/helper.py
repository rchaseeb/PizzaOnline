class UtilMethods(object):
    @staticmethod
    def str_to_bool(text):
        if isinstance(text, bool):
            if text in [True, False]:
                return text
        elif str(text).lower() in ['true', '1']:
            return True
        elif str(text).lower() in ['false', '0']:
            return False
        else:
            return text
