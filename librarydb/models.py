# coding: utf-8
from sqlalchemy import Column, Date, DateTime, ForeignKey, Integer, Numeric, String, Table, Text, text, MetaData
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from librarydb import login_manager, db
from flask_login import UserMixin

# Base = declarative_base()
# metadata = Base.metadata

metadata = MetaData()
# metadata.clear()  # clears already defined models
db.metadata.clear()


@login_manager.user_loader
def load_user(uid):
    """
    :param uid:     (int)   : user id
    :return:        (obj)   : User instance
    """
    return Uzytkownicy.query.get(int(uid))


class Autor(db.Model):
    __tablename__ = 'autor'

    id = Column(Integer, primary_key=True, server_default=text("nextval('autor_id_seq'::regclass)"))
    imie = Column(String(20), nullable=False)
    nazwisko = Column(String(20))


class Jezyk(db.Model):
    __tablename__ = 'jezyk'

    id = Column(Integer, primary_key=True, server_default=text("nextval('jezyk_id_seq'::regclass)"))
    jezyk = Column(String(15), nullable=False)


class TypKary(db.Model):
    __tablename__ = 'typ_kary'

    id = Column(Integer, primary_key=True, server_default=text("nextval('typ_kary_id_seq'::regclass)"))
    typ_kary = Column(String(150), nullable=False)
    wysokosc = Column(Numeric(9, 2), nullable=False)


class TypKonta(db.Model):
    """
    1 - klient
    2 - pracownik
    """
    __tablename__ = 'typ_konta'

    id = Column(Integer, primary_key=True, server_default=text("nextval('typ_konta_id_seq'::regclass)"))
    typ_konta = Column(String(10), nullable=False)


class Wydawca(db.Model):
    __tablename__ = 'wydawca'

    id = Column(Integer, primary_key=True, server_default=text("nextval('wydawca_id_seq'::regclass)"))
    nazwa = Column(String(20), nullable=False)


class Ksiazki(db.Model):
    __tablename__ = 'ksiazki'
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True, server_default=text("nextval('ksiazki_id_seq'::regclass)"))
    tytul = Column(String(40), nullable=False)
    autor_id = Column(ForeignKey('autor.id'))
    wydawca_id = Column(ForeignKey('wydawca.id'))
    ean = Column(String(20), nullable=False)
    data_premiery = Column(Date)
    rok_wydania = Column(Integer)
    jezyk_id = Column(ForeignKey('jezyk.id'))

    autor = relationship('Autor')
    jezyk = relationship('Jezyk')
    wydawca = relationship('Wydawca')

    def __str__(self):
        return f'({self.id}, {self.tytul}, {self.autor_id}, {self.wydawca_id})'


class Kategoria(db.Model):
    __tablename__ = 'kategoria'

    id = Column(Integer, primary_key=True, server_default=text("nextval('kategoria_id_seq'::regclass)"))
    kategoria = Column(String(15), nullable=False)

    ksiazka = relationship('Ksiazki', secondary='ksiazka_kategoria')

class Uzytkownicy(db.Model, UserMixin):
    __tablename__ = 'uzytkownicy'
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True, server_default=text("nextval('uzytkownicy_id_seq'::regclass)"))
    imie = Column(String(20), nullable=False)
    nazwisko = Column(String(20), nullable=False)
    pesel = Column(String(11), nullable=False, unique=True)
    email = Column(String(30), nullable=False)
    adres = Column(String(40))
    nazwa_uzytkownika = Column(String(15), nullable=False)
    haslo = Column(String(40), nullable=False)
    typ_konta_id = Column(ForeignKey('typ_konta.id'))
    biblioteka_id = Column(ForeignKey('biblioteki.id'))

    biblioteka = relationship('Biblioteki')
    typ_konta = relationship('TypKonta')

    def __str__(self):
        return f'({self.id}, {self.imie}, {self.nazwisko}, {self.nazwa_uzytkownika})'


class Egzemplarze(db.Model):
    __tablename__ = 'egzemplarze'

    id = Column(Integer, primary_key=True, server_default=text("nextval('egzemplarze_id_seq'::regclass)"))
    ksiazka_id = Column(ForeignKey('ksiazki.id'))
    biblioteka_id = Column(ForeignKey('biblioteki.id'))

    ksiazka = relationship('Ksiazki')
    biblioteka = relationship('Biblioteki')

class Biblioteki(db.Model):
    __tablename__ = 'biblioteki'

    id = Column(Integer, primary_key=True, server_default=text("nextval('biblioteki_id_seq'::regclass)"))
    nazwa = Column(String(20), nullable=False)
    adres = Column(String(40))

    egzemplarzs = relationship('Egzemplarze', secondary='biblioteka_egzemplarz')

# t_ksiazka_kategoria = Table(
#     'ksiazka_kategoria', metadata,
#     Column('kategoria_id', ForeignKey('kategoria.id'), primary_key=True, nullable=False),
#     Column('ksiazka_id', ForeignKey('ksiazki.id'), primary_key=True, nullable=False)
# )


class Opinie(db.Model):
    __tablename__ = 'opinie'

    id = Column(Integer, primary_key=True, server_default=text("nextval('opinie_id_seq'::regclass)"))
    ksiazka_id = Column(ForeignKey('ksiazki.id'))
    uzytkownik_id = Column(ForeignKey('uzytkownicy.id'))
    opinia = Column(Text, nullable=False)
    data_dodania = Column(DateTime, nullable=False)

    ksiazka = relationship('Ksiazki')
    uzytkownik = relationship('Uzytkownicy')


class Rezerwacje(db.Model):
    __tablename__ = 'rezerwacje'

    id = Column(Integer, primary_key=True, server_default=text("nextval('rezerwacje_id_seq'::regclass)"))
    uzytkownik_id = Column(ForeignKey('uzytkownicy.id'))
    data_rezerwacji = Column(DateTime, nullable=False)
    ksiazka_id = Column(ForeignKey('ksiazki.id'))

    ksiazka = relationship('Ksiazki')
    uzytkownik = relationship('Uzytkownicy')


class Kary(db.Model):
    __tablename__ = 'kary'

    id = Column(Integer, primary_key=True, server_default=text("nextval('kary_id_seq'::regclass)"))
    uzytkownik_id = Column(ForeignKey('uzytkownicy.id'))
    egzemplarz_id = Column(ForeignKey('egzemplarze.id'))
    typ_kary_id = Column(ForeignKey('typ_kary.id'))

    egzemplarz = relationship('Egzemplarze')
    typ_kary = relationship('TypKary')
    uzytkownik = relationship('Uzytkownicy')


class Wypozyczenia(db.Model):
    __tablename__ = 'wypozyczenia'

    id = Column(Integer, primary_key=True, server_default=text("nextval('wypozyczenia_id_seq'::regclass)"))
    uzytkownik_id = Column(ForeignKey('uzytkownicy.id'))
    egzemplarz_id = Column(ForeignKey('egzemplarze.id'))
    data_wypozyczenia = Column(DateTime, nullable=False)
    data_oddania = Column(DateTime, nullable=False)

    egzemplarz = relationship('Egzemplarze')
    uzytkownik = relationship('Uzytkownicy')


class Platnosci(db.Model):
    __tablename__ = 'platnosci'

    id = Column(Integer, primary_key=True, server_default=text("nextval('platnosci_id_seq'::regclass)"))
    id_kary = Column(ForeignKey('kary.id'))
    data_platnosci = Column(DateTime, nullable=False)

    kary = relationship('Kary')


class Ksiazka_kategoria(db.Model):
    __table_args__ = (
        db.PrimaryKeyConstraint('kategoria_id', 'ksiazka_id', name='pk_kategoria_ksiazka_id'),
    )

    __tablename__ = 'ksiazka_kategoria'

    kategoria_id = Column(Integer, ForeignKey('kategoria.id'))
    ksiazka_id = Column(ForeignKey('ksiazki.id'))

    kategoria = relationship('Kategoria')


class Biblioteka_egzemplarz(db.Model):
    __table_args__ = (
        db.PrimaryKeyConstraint('biblioteka_id', 'egzemplarz_id', name='pk_biblioteka_egzemplarz_id'),
    )

    __tablename__ = 'biblioteka_egzemplarz'

    biblioteka_id = Column(Integer, ForeignKey('biblioteki.id'))
    egzemplarz_id = Column(ForeignKey('egzemplarze.id'))