insert into typ_konta(typ_konta) VALUES ('klient');
insert into typ_konta(typ_konta) VALUES ('pracownik');
insert into typ_kary(typ_kary, wysokosc) VALUES ('zniszczenie', '50.00');
insert into typ_kary(typ_kary, wysokosc) VALUES ('oddanie do miesiaca po terminie', '20.00');
insert into biblioteki(nazwa, adres)  VALUES ('Biblioteka Kraków', 'Kraków, ul. Biblioteczna 15');
insert into biblioteki(nazwa, adres)  VALUES ('Biblioteka Warszawa', 'Warszawa, ul. Biblioteczna 20');
insert into jezyk(jezyk) VALUES ('polski');
insert into jezyk(jezyk) VALUES ('angielski');
insert into kategoria(kategoria) VALUES ('powieść');
insert into kategoria(kategoria) VALUES ('historyczna');
insert into kategoria(kategoria) VALUES ('dla dzieci');
insert into kategoria(kategoria) VALUES ('dramat');
insert into autor(imie, nazwisko) VALUES ('Henryk', 'Sienkiewicz');
insert into autor(imie, nazwisko) VALUES ('Renata', 'Piątkowska');
insert into autor(imie, nazwisko) VALUES ('Beatrice', 'Alemagna');
insert into autor(imie, nazwisko) VALUES ('Alexandra', 'Maxeiner');
insert into autor(imie, nazwisko) VALUES ('William', 'Shakespeare');
insert into autor(imie, nazwisko) VALUES ('Sofokles', '');
insert into autor(imie, nazwisko) VALUES ('Juliusz', 'Słowacki');
insert into autor(imie, nazwisko) VALUES ('Jonathan', 'Swift');
insert into autor(imie, nazwisko) VALUES ('ANONIM', 'ANONIM');
insert into wydawca(nazwa) VALUES ('wydawnictwoA');
insert into wydawca(nazwa) VALUES ('wydawnictwoB');

insert into ksiazki(tytul, autor_id, wydawca_id, ean, data_premiery, rok_wydania, jezyk_id) VALUES ('Ogniem i Mieczem', 1, 1, '0000000001', '1998-04-21', '2010',1);
insert into ksiazki(tytul, autor_id, wydawca_id, ean, data_premiery, rok_wydania, jezyk_id) VALUES ('Potop', 1, 1, '0000000002', '1999-04-21', '2011',1);
insert into ksiazki(tytul, autor_id, wydawca_id, ean, data_premiery, rok_wydania, jezyk_id) VALUES ('Krzyżacy', 1, 1, '0000000002', '1999-04-21', '2011',1);
insert into ksiazki(tytul, autor_id, wydawca_id, ean, data_premiery, rok_wydania, jezyk_id) VALUES ('Która to Malala?', 2, 2, '0000000003', '2015-04-21', '2015',1);
insert into ksiazki(tytul, autor_id, wydawca_id, ean, data_premiery, rok_wydania, jezyk_id) VALUES ('Pięciu Nieudanych', 3, 2, '0000000004', '2017-04-21', '2016',1);
insert into ksiazki(tytul, autor_id, wydawca_id, ean, data_premiery, rok_wydania, jezyk_id) VALUES ('To wszystko pyszne!', 4, 1, '0000000005', '2010-04-21', '2011',1);
insert into ksiazki(tytul, autor_id, wydawca_id, ean, data_premiery, rok_wydania, jezyk_id) VALUES ('Makbet', 5, 1, '0000000006', '2010-01-01', '2011',1);
insert into ksiazki(tytul, autor_id, wydawca_id, ean, data_premiery, rok_wydania, jezyk_id) VALUES ('Antygona', 6, 1, '0000000007', '2009-04-21', '2009',1);
insert into ksiazki(tytul, autor_id, wydawca_id, ean, data_premiery, rok_wydania, jezyk_id) VALUES ('Balladyna ', 7, 1, '0000000008', '2008-04-21', '2009',1);
insert into ksiazki(tytul, autor_id, wydawca_id, ean, data_premiery, rok_wydania, jezyk_id) VALUES ('Gulliver’s Travels', 8, 2, '0000000009', '2010-04-21', '2011',2);
insert into ksiazki(tytul, autor_id, wydawca_id, ean, data_premiery, rok_wydania, jezyk_id) VALUES ('Książka I', 9, 1, '0000000010', '1999-04-21', '2011',1);
insert into ksiazki(tytul, autor_id, wydawca_id, ean, data_premiery, rok_wydania, jezyk_id) VALUES ('Książka II', 9, 1, '0000000011', '1999-04-21', '2011',1);
insert into ksiazki(tytul, autor_id, wydawca_id, ean, data_premiery, rok_wydania, jezyk_id) VALUES ('Książka III', 9, 1, '0000000012', '1999-04-21', '2011',1);
insert into ksiazki(tytul, autor_id, wydawca_id, ean, data_premiery, rok_wydania, jezyk_id) VALUES ('Książka IV', 9, 1, '0000000013', '1999-04-21', '2011',1);
insert into ksiazki(tytul, autor_id, wydawca_id, ean, data_premiery, rok_wydania, jezyk_id) VALUES ('Książka V', 9, 1, '0000000014', '1999-04-21', '2011',1);
insert into ksiazki(tytul, autor_id, wydawca_id, ean, data_premiery, rok_wydania, jezyk_id) VALUES ('Książka VI', 9, 1, '0000000015', '1999-04-21', '2011',1);
insert into ksiazki(tytul, autor_id, wydawca_id, ean, data_premiery, rok_wydania, jezyk_id) VALUES ('Książka VII', 9, 1, '0000000016', '1999-04-21', '2011',1);
insert into ksiazki(tytul, autor_id, wydawca_id, ean, data_premiery, rok_wydania, jezyk_id) VALUES ('Książka VIII', 9, 1, '0000000017', '1999-04-21', '2011',1);
insert into ksiazki(tytul, autor_id, wydawca_id, ean, data_premiery, rok_wydania, jezyk_id) VALUES ('Książka IX', 9, 2, '0000000018', '1999-04-21', '2011',1);
insert into ksiazki(tytul, autor_id, wydawca_id, ean, data_premiery, rok_wydania, jezyk_id) VALUES ('Książka X', 9, 2, '0000000019', '1999-04-21', '2011',1);
insert into ksiazki(tytul, autor_id, wydawca_id, ean, data_premiery, rok_wydania, jezyk_id) VALUES ('Książka XI', 9, 2, '0000000020', '1999-04-21', '2011',1);
insert into ksiazka_kategoria VALUES (1,1);
insert into ksiazka_kategoria VALUES (2,1);
insert into ksiazka_kategoria VALUES (1,2);
insert into ksiazka_kategoria VALUES (2,2);
insert into ksiazka_kategoria VALUES (3,3);
insert into ksiazka_kategoria VALUES (3,4);
insert into ksiazka_kategoria VALUES (3,5);
insert into ksiazka_kategoria VALUES (4,6);
insert into ksiazka_kategoria VALUES (4,7);
insert into ksiazka_kategoria VALUES (4,8);
insert into ksiazka_kategoria VALUES (5,9);
insert into ksiazka_kategoria VALUES (5,10);
insert into ksiazka_kategoria VALUES (5,11);
insert into ksiazka_kategoria VALUES (5,12);
insert into ksiazka_kategoria VALUES (5,13);
insert into ksiazka_kategoria VALUES (5,14);
insert into ksiazka_kategoria VALUES (5,15);
insert into ksiazka_kategoria VALUES (5,16);
insert into ksiazka_kategoria VALUES (5,17);
insert into ksiazka_kategoria VALUES (5,18);
insert into ksiazka_kategoria VALUES (5,19);
insert into ksiazka_kategoria VALUES (5,20);
insert into ksiazka_kategoria VALUES (5,21);

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
insert into uzytkownicy(imie, nazwisko, pesel, email, adres, nazwa_uzytkownika, haslo, typ_konta_id, biblioteka_id)
VALUES ('User', 'Uzytkownicki', '01234567211', 'user@user.com', 'Uzytkownika 5', 'user', '$2y$12$8AOe1VEj5YSxSlHpdcUsL.n987drqUXi9TLTgnmTsK23ZUwEuhEme', 1, 1);
INSERT INTO uzytkownicy (imie, nazwisko, pesel, email, adres, nazwa_uzytkownika, haslo, typ_konta_id, biblioteka_id)
VALUES ('Jan', 'Kowalski', '12345678913', 'admin@admin.com', 'Polna 2', 'admin', '$2b$12$I7W8Q3SOF4WmcH/Y5jLqse6gFNT.HZiwxQCAPV3MWCQKGzCCIyplO', 2, 1);
insert into wypozyczenia(uzytkownik_id, egzemplarz_id, data_wypozyczenia, data_oddania) VALUES (1, 1, '2019-12-20', NULL);
insert into wypozyczenia(uzytkownik_id, egzemplarz_id, data_wypozyczenia, data_oddania) VALUES (1, 2, '2019-12-20', NULL);
insert into rezerwacje(uzytkownik_id, data_rezerwacji, ksiazka_id) VALUES (1,'2019-10-10',2);
insert into kary(uzytkownik_id, egzemplarz_id, typ_kary_id, wysokosc) VALUES (1,1,1,50.50);

INSERT INTO opinie(ksiazka_id, uzytkownik_id, opinia, data_dodania) VALUES (2, 1,'Dla mnie bomba', '1724-02-01');
INSERT INTO opinie(ksiazka_id, uzytkownik_id, opinia, data_dodania) VALUES (1, 1,'Ta ksiazka odmienila moje życie! POLECAM', '1924-02-01');
INSERT INTO opinie(ksiazka_id, uzytkownik_id, opinia, data_dodania) VALUES (2, 1,'Średnia', '1424-02-01');