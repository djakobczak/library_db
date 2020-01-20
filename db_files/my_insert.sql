insert into typ_konta(typ_konta) VALUES ('klient');
insert into typ_konta(typ_konta) VALUES ('pracownik');
insert into typ_kary(typ_kary, wysokosc) VALUES ('zniszczenie', '50.00');
insert into typ_kary(typ_kary, wysokosc) VALUES ('oddanie do miesiaca po terminie', '20.00');
insert into biblioteki(nazwa, adres)  VALUES ('Biblioteka Kraków', 'Kraków, ul. Biblioteczna 15');
insert into biblioteki(nazwa, adres)  VALUES ('Biblioteka Warszawa', 'Warszawa, ul. Biblioteczna 20');
insert into jezyk(jezyk) VALUES ('polski');
insert into kategoria(kategoria) VALUES ('powieść');
insert into kategoria(kategoria) VALUES ('historyczna');
insert into kategoria(kategoria) VALUES ('dla dzieci');
insert into kategoria(kategoria) VALUES ('dramat');
insert into autor(imie, nazwisko) VALUES ('Henryk', 'Sienkiewicz');
insert into wydawca(nazwa) VALUES ('wydawnictwoA');

insert into ksiazki(tytul, autor_id, wydawca_id, ean, data_premiery, rok_wydania, jezyk_id) VALUES ('Ogniem i Mieczem', 1, 1, '0000000001', '1998-04-21', '2010',1);
insert into ksiazki(tytul, autor_id, wydawca_id, ean, data_premiery, rok_wydania, jezyk_id) VALUES ('Potop', 1, 1, '0000000002', '1999-04-21', '2011',1);
insert into ksiazka_kategoria VALUES (1,1);
insert into ksiazka_kategoria VALUES (2,1);
insert into ksiazka_kategoria VALUES (1,2);
insert into ksiazka_kategoria VALUES (2,2);

insert into egzemplarze(ksiazka_id, biblioteka_id) VALUES (1, 1);
insert into egzemplarze(ksiazka_id, biblioteka_id) VALUES (1, 1);
insert into egzemplarze(ksiazka_id, biblioteka_id) VALUES (1, 1);
insert into egzemplarze(ksiazka_id, biblioteka_id) VALUES (2, 1);
insert into egzemplarze(ksiazka_id, biblioteka_id) VALUES (2, 2);
insert into egzemplarze(ksiazka_id, biblioteka_id) VALUES (2, 2);
insert into egzemplarze(ksiazka_id, biblioteka_id) VALUES (2, 2);
insert into egzemplarze(ksiazka_id, biblioteka_id) VALUES (2, 1);
insert into egzemplarze(ksiazka_id, biblioteka_id) VALUES (2, 1);

insert into uzytkownicy(imie, nazwisko, pesel, email, adres, nazwa_uzytkownika, haslo, typ_konta_id, biblioteka_id)
VALUES ('Mariusz', 'Hariusz', '01234567891', 'mail@mail.com', 'Kwiatowa 5', 'Marek', '$2y$12$8AOe1VEj5YSxSlHpdcUsL.n987drqUXi9TLTgnmTsK23ZUwEuhEme', 1, 1);
INSERT INTO uzytkownicy (imie, nazwisko, pesel, email, adres, nazwa_uzytkownika, haslo, typ_konta_id, biblioteka_id)
VALUES ('Jan', 'Kowalski', '12345678913', 'admin@admin.com', 'Polna 2', 'admin', '$2b$12$I7W8Q3SOF4WmcH/Y5jLqse6gFNT.HZiwxQCAPV3MWCQKGzCCIyplO', 2, 1);
insert into wypozyczenia(uzytkownik_id, egzemplarz_id, data_wypozyczenia, data_oddania) VALUES (1, 1, '2019-12-20', NULL);
insert into wypozyczenia(uzytkownik_id, egzemplarz_id, data_wypozyczenia, data_oddania) VALUES (1, 2, '2019-12-20', NULL);
insert into rezerwacje(uzytkownik_id, data_rezerwacji, ksiazka_id) VALUES (1,'2019-10-10',2);
insert into kary(uzytkownik_id, egzemplarz_id, typ_kary_id) VALUES (1,1,1);
