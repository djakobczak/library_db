CREATE OR REPLACE VIEW v_wypozyczenia_uzytkownika as
	SELECT  u.nazwa_uzytkownika, k.tytul, w.data_wypozyczenia, w.data_oddania 
	FROM wypozyczenia w
	INNER JOIN egzemplarze e ON e.id = w.egzemplarz_id
	INNER JOIN ksiazki k ON k.id = e.ksiazka_id
	INNER JOIN uzytkownicy u ON u.id = w.uzytkownik_id

CREATE OR REPLACE VIEW v_rezerwacje_uzytkownika as
	SELECT  u.nazwa_uzytkownika, k.tytul, r.data_rezerwacji 
	FROM rezerwacje r
	INNER JOIN ksiazki k ON k.id = r.ksiazka_id
	INNER JOIN uzytkownicy u ON u.id = r.uzytkownik_id
	
drop view v_ksiazki_dostepne;
CREATE OR REPLACE VIEW v_ksiazki_dostepne as
	SELECT k.tytul, a.imie, a.nazwisko, count(*) as ilosc
	FROM ksiazki k
	INNER JOIN autor a ON k.autor_id = a.id
	INNER JOIN egzemplarze e ON e.ksiazka_id = k.id
	LEFT JOIN wypozyczenia w ON e.id = w.egzemplarz_id WHERE w.egzemplarz_id IS NULL
	GROUP BY k.tytul, a.imie, a.nazwisko;

CREATE OR REPLACE VIEW v_kary_uzytkownik as
	SELECT tk.typ_kary, tk.wysokosc, u.nazwa_uzytkownika
	FROM kary k
	INNER JOIN typ_kary tk ON tk.id = k.typ_kary_id
	INNER JOIN uzytkownicy u ON u.id = k.uzytkownik_id
	
	
select * from v_wypozyczenia_uzytkownika  where nazwa_uzytkownika = 'admin'
select * from v_rezerwacje_uzytkownika  where nazwa_uzytkownika = 'admin'
select * from v_ksiazki_dostepne
select * from v_kary_uzytkownik 

delete from wypozyczenia where id = 2

select * from wypozyczenia 
select * from ksiazki 
select * from egzemplarze
select * from biblioteki 
select * from uzytkownicy 
select * from rezerwacje 

select * from jezyk
select * from kary
select * from autor 
select * from typ_konta 
select * from typ_kary 
select * from wydawca 

alter table typ_kary alter column typ_kary TYPE varchar(150);
insert into typ_konta VALUES (1, 'klient');
insert into typ_konta VALUES (2, 'pracownik');
insert into typ_kary VALUES (1, 'zniszczenie', '50.00');
insert into typ_kary VALUES (2, 'oddanie do miesiaca po terminie', '20.00');
insert into biblioteki  VALUES (1, 'Biblioteka Kraków', 'Kraków, ul. Biblioteczna 15');
insert into biblioteki  VALUES (2, 'Biblioteka Warszawa', 'Warszawa, ul. Biblioteczna 20');
insert into jezyk VALUES (1, 'polski');

insert into autor VALUES (1, 'Henryk', 'Sienkiewicz');
insert into wydawca  VALUES (1, 'wydawnictwoA');
insert into ksiazki VALUES (1, 'Ogniem i Mieczem', 1, 1, '0000000001', '1998-04-21', '2010',1);
insert into ksiazki VALUES (2, 'Potop', 1, 1, '0000000002', '1999-04-21', '2011',1);
insert into egzemplarze VALUES (1,1);
insert into egzemplarze VALUES (2,1);
insert into egzemplarze VALUES (3,1);
insert into egzemplarze VALUES (4,2);
insert into egzemplarze VALUES (5,2);

insert into uzytkownicy VALUES (1,'Mariusz', 'Hariusz', 'mail@mail.com', 'Kwiatowa 5', 'admin', 'admin', 1, 1);
insert into wypozyczenia VALUES (1, 1, 1, '2019-12-20', '2020-01-19');
insert into wypozyczenia VALUES (2, 1, 2, '2019-12-20', '2020-01-19');
insert into rezerwacje VALUES (1,1,'2019-10-10',2);
insert into kary VALUES (1,1,1,1);
