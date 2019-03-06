
class m_singelton:
    msingle = None



    def __init__(self):
        if m_singelton.msingle:
            raise m_singelton.msingle
        m_singelton.msingle = self

