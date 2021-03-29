from sqlalchemy import Boolean, Column, Integer, String, UnicodeText
from MashaRoBot.modules.sql import BASE, SESSION


class Talkmode(BASE):
    __tablename__ = "talkmode"
    chat_id = Column(String(14), primary_key=True)

    def __init__(self, chat_id):
        self.chat_id = chat_id


Talkmode.__table__.create(checkfirst=True)


def add_talkmode(chat_id: str):
    talkmoddy = Talkmode(str(chat_id))
    SESSION.add(talkmoddy)
    SESSION.commit()


def rmtalkmode(chat_id: str):
    rmtalkmoddy = SESSION.query(Talkmode).get(str(chat_id))
    if rmtalkmoddy:
        SESSION.delete(rmtalkmoddy)
        SESSION.commit()


def get_all_chat_id():
    stark = SESSION.query(Talkmode).all()
    SESSION.close()
    return stark


def is_talkmode_indb(chat_id: str):
    try:
        s__ = SESSION.query(Talkmode).get(str(chat_id))
        if s__:
            return str(s__.chat_id)
    finally:
        SESSION.close()
