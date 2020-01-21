CREATE OR REPLACE VIEW v_wypozyczenia as
	SELECT w.id, u.nazwa_uzytkownika, k.tytul, w.data_wypozyczenia, w.data_oddania, e.id as egzemplarz_id, k.id as ksiazka_id
	FROM wypozyczenia w
	INNER JOIN egzemplarze e ON e.id = w.egzemplarz_id
	INNER JOIN ksiazki k ON k.id = e.ksiazka_id
	INNER JOIN uzytkownicy u ON u.id = w.uzytkownik_id;

CREATE OR REPLACE VIEW v_rezerwacje as
	SELECT r.id, u.nazwa_uzytkownika, k.tytul, r.data_rezerwacji
	FROM rezerwacje r
	INNER JOIN uzytkownicy u ON u.id = r.uzytkownik_id
	INNER JOIN ksiazki k ON k.id = r.ksiazka_id
	order by r.data_rezerwacji;

CREATE OR REPLACE VIEW v_ksiazki as
	SELECT k.id, k.tytul, a.imie, a.nazwisko, w.nazwa, k.ean, k.data_premiery, k.rok_wydania, j.jezyk
	FROM ksiazki k
	INNER JOIN jezyk j ON j.id = k.jezyk_id
	INNER JOIN autor a ON a.id = k.autor_id
	INNER JOIN wydawca w ON w.id = k.wydawca_id;

CREATE OR REPLACE VIEW v_ksiazki_kategoria as
	SELECT k.id, kat.kategoria, k.tytul, a.imie, a.nazwisko
	FROM ksiazki k
	INNER JOIN autor a ON a.id = k.autor_id
	INNER JOIN ksiazka_kategoria kk ON kk.ksiazka_id = k.id
	INNER JOIN kategoria kat ON kat.id = kk.kategoria_id
	ORDER BY kat.kategoria;

CREATE OR REPLACE VIEW v_egzemplarze as
	SELECT e.id, k.tytul, a.imie, a.nazwisko, b.nazwa, k.id AS ksiazka_id
	FROM egzemplarze e
	INNER JOIN ksiazki k ON k.id = e.ksiazka_id
	INNER JOIN autor a ON a.id = k.autor_id
	INNER JOIN biblioteki b ON b.id = e.biblioteka_id
	ORDER BY k.tytul, a.nazwisko;

CREATE OR REPLACE VIEW v_platnosci as
	SELECT p.id, p.data_platnosci, u.id AS user_id, u.nazwa_uzytkownika, ks.tytul,
	 				tk.typ_kary, e.id as egzemplarz_id, tk.wysokosc
	FROM platnosci p
	INNER JOIN kary k ON k.id = p.id_kary
	INNER JOIN uzytkownicy u ON u.id = k.uzytkownik_id
	INNER JOIN typ_kary tk ON tk.id = k.typ_kary_id
	INNER JOIN egzemplarze e ON e.id = k.egzemplarz_id
	INNER JOIN ksiazki ks ON ks.id = e.ksiazka_id;

CREATE OR REPLACE VIEW v_opinie as
	SELECT o.id, k.tytul, u.nazwa_uzytkownika, o.opinia
	FROM opinie o
	INNER JOIN uzytkownicy u ON u.id = o.uzytkownik_id
	INNER JOIN ksiazki k ON k.id = o.ksiazka_id;

CREATE OR REPLACE VIEW v_uzytkownicy as
	SELECT u.id, u.imie, u.nazwisko, u.email, u.adres, u.nazwa_uzytkownika,
	u.haslo, tk.typ_konta, b.nazwa as nazwa_biblioteki
	FROM uzytkownicy u
	INNER JOIN typ_konta tk ON tk.id = u.typ_konta_id
	INNER JOIN biblioteki b ON b.id = u.biblioteka_id
	order by u.nazwa_uzytkownika;

create or replace view vp_ksiazki_niedostepne as
	SELECT k.id, count(*)
	FROM wypozyczenia w
	INNER JOIN egzemplarze e ON w.egzemplarz_id = e.id
	INNER JOIN ksiazki k ON k.id = e.ksiazka_id
	WHERE w.data_oddania is null
	GROUP BY k.id;

CREATE OR REPLACE VIEW v_ksiazki_niedostepne as
	SELECT k.tytul, a.imie, a.nazwisko, k.id
	FROM ksiazki k
	INNER JOIN autor a ON k.autor_id = a.id
	INNER JOIN egzemplarze e ON e.ksiazka_id = k.id
	INNER JOIN wypozyczenia w ON e.id = w.egzemplarz_id
	where (select count from vp_ksiazki_niedostepne where id = k.id) >= (select count(*) from egzemplarze where ksiazka_id = k.id group by ksiazka_id)
	GROUP BY k.tytul, a.imie, a.nazwisko, k.id
	ORDER BY k.tytul;

CREATE OR REPLACE VIEW v_ksiazki_dostepne as
	SELECT k.tytul, a.imie, a.nazwisko, count(*) as ilosc, k.id
	FROM ksiazki k
	INNER JOIN autor a ON k.autor_id = a.id
	INNER JOIN egzemplarze e ON e.ksiazka_id = k.id
	LEFT JOIN wypozyczenia w ON e.id = w.egzemplarz_id WHERE w.egzemplarz_id IS NULL OR (select egzemplarz_id from wypozyczenia where data_oddania is null AND egzemplarz_id = e.id) is null
	GROUP BY k.tytul, a.imie, a.nazwisko, k.id
	ORDER BY k.tytul;

CREATE OR REPLACE VIEW v_wypozyczenia_najczestsze as
	select k.id, w.tytul, count(*) as ilosc from v_wypozyczenia w
	INNER JOIN ksiazki k ON k.id = w.ksiazka_id
	group by k.id, w.tytul order by ilosc desc limit 3;

CREATE OR REPLACE VIEW v_wypozyczenia_najrzadsze as
	select k.id, w.tytul, count(*) as ilosc from v_wypozyczenia w
	INNER JOIN ksiazki k ON k.id = w.ksiazka_id
	group by k.id, w.tytul order by ilosc limit 3;

CREATE OR REPLACE VIEW v_wypozyczenia_czestsze_niz_srednia as
	select k.id, w.tytul, count(*) as ilosc from v_wypozyczenia w
	INNER JOIN ksiazki k ON k.id = w.ksiazka_id
	group by k.id, w.tytul HAVING COUNT(*) > (select avg(t.ilosc) as srednia from (select count(*) as ilosc from v_wypozyczenia group by ksiazka_id) as t);

CREATE OR REPLACE VIEW v_kary_oplacone as
 SELECT k.id,
    u.nazwa_uzytkownika,
    ks.tytul,
    tk.typ_kary,
    e.id AS egzemplarz_id
   FROM kary k
     JOIN uzytkownicy u ON u.id = k.uzytkownik_id
     JOIN typ_kary tk ON tk.id = k.typ_kary_id
     JOIN egzemplarze e ON e.id = k.egzemplarz_id
     JOIN ksiazki ks ON ks.id = e.ksiazka_id
     INNER JOIN platnosci p ON p.id_kary = k.id
  ORDER BY u.nazwa_uzytkownika;

CREATE OR REPLACE VIEW v_kary_nieoplacone as
 SELECT k.id as ksiazka_id,
    u.nazwa_uzytkownika,
		u.id as uzytkownik_id,
    ks.tytul,
    tk.typ_kary,
    e.id AS egzemplarz_id,
		k.wysokosc
   FROM kary k
     JOIN uzytkownicy u ON u.id = k.uzytkownik_id
     JOIN typ_kary tk ON tk.id = k.typ_kary_id
     JOIN egzemplarze e ON e.id = k.egzemplarz_id
     JOIN ksiazki ks ON ks.id = e.ksiazka_id
     LEFT JOIN platnosci p ON p.id_kary = k.id where p.id_kary is null
  ORDER BY u.nazwa_uzytkownika;


CREATE OR REPLACE VIEW v_egzemplarze_wypozyczenia as
	SELECT e.id as egzemplarz_id, EXISTS (select 1 from wypozyczenia w where egzemplarz_id = e.id) as czy_wypozyczona
	FROM egzemplarze e
	left JOIN wypozyczenia w ON w.egzemplarz_id = e.id
	ORDER BY e.id;


CREATE OR REPLACE VIEW v_egzemplarze_rezerwacje_wypozyczenia as
	SELECT k.id as ksiazka_id, e.id as egzemplarz_id, EXISTS (select 1 from wypozyczenia w where egzemplarz_id = e.id and data_oddania is null) as czy_wypozyczona,
		EXISTS (select 1 from rezerwacje where ksiazka_id = k.id) as czy_rezerwacja_na_ksiazke
	FROM egzemplarze e
	INNER JOIN ksiazki k ON k.id = e.ksiazka_id
	ORDER BY e.id;
