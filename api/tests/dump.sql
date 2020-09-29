--
-- PostgreSQL database dump
--

-- Dumped from database version 12.3 (Debian 12.3-1.pgdg100+1)
-- Dumped by pg_dump version 12.3 (Debian 12.3-1.pgdg100+1)

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: artists; Type: TABLE; Schema: public; Owner: play_backend_user
--

CREATE TABLE public.artists (
    artist_id serial primary key,
    artist_name character varying(255),
    artist_cover character varying(255)
);


ALTER TABLE public.artists OWNER TO play_backend_user;

CREATE TABLE public.playlists (
    playlist_id serial primary key,
    playlist_public boolean,
    playlist_name character varying(255),
    playlist_cover character varying(50)
);


ALTER TABLE public.playlists OWNER TO play_backend_user;

CREATE TABLE public.playlists_x_tracks (
    playlist_id integer,
    track_id integer
);


ALTER TABLE public.playlists_x_tracks OWNER TO play_backend_user;

--
-- Name: releases; Type: TABLE; Schema: public; Owner: play_backend_user
--

CREATE TABLE public.releases (
    release_id serial primary key,
    release_name character varying(255),
    release_year date,
    artist_id integer,
    release_cover character varying(255)
);


ALTER TABLE public.releases OWNER TO play_backend_user;

CREATE TABLE public.tracks (
    track_id serial primary key,
    artist_id integer,
    release_id integer,
    track_name character varying(255)
);


ALTER TABLE public.tracks OWNER TO play_backend_user;


CREATE TABLE public.user_x_playlist (
    playlist_id integer,
    user_id integer
);


ALTER TABLE public.user_x_playlist OWNER TO play_backend_user;

CREATE TABLE public.users (
    user_id serial primary key,
    username character varying(30),
    email character varying(50),
    hash_password character varying(128),
    disabled boolean,
    active boolean
);


ALTER TABLE public.users OWNER TO play_backend_user;

INSERT INTO public.artists(artist_name, artist_cover) VALUES ('Шлем', 'shlem.jpg');
INSERT INTO public.artists(artist_name, artist_cover) VALUES ('Karzer', 'karzer.jpg');
INSERT INTO public.artists(artist_name, artist_cover) VALUES ('Oskal', 'oskal.jpg');
INSERT INTO public.artists(artist_name, artist_cover) VALUES ('Every Time I Die', 'etid.jpg');
INSERT INTO public.artists(artist_name, artist_cover) VALUES ('Baptists', 'baptists.jpg');
INSERT INTO public.artists(artist_name, artist_cover) VALUES ('Black Breath', 'blackbreath.jpg');
INSERT INTO public.artists(artist_name, artist_cover) VALUES ('Kvelertak', 'kvelertak.jpg');
INSERT INTO public.artists(artist_name, artist_cover) VALUES ('Duke Nukem', 'dukenukem.jpg');
INSERT INTO public.artists(artist_name, artist_cover) VALUES ('Leftover Crack', 'leftovercrack.jpg');
INSERT INTO public.artists(artist_name, artist_cover) VALUES ('Ария', 'aria.jpg');



--
-- Data for Name: playlists; Type: TABLE DATA; Schema: public; Owner: play_backend_user
--

INSERT INTO public.playlists  (playlist_public, playlist_name, playlist_cover) VALUES (true, 'black metal', 'playlist.png');
INSERT INTO public.playlists  (playlist_public, playlist_name, playlist_cover) VALUES (true, 'punk', 'playlist.png');
INSERT INTO public.playlists  (playlist_public, playlist_name, playlist_cover) VALUES (false, 'rock', 'playlist.png');
INSERT INTO public.playlists  (playlist_public, playlist_name, playlist_cover) VALUES (false, 'hooi', 'playlist.png');
INSERT INTO public.playlists  (playlist_public, playlist_name, playlist_cover) VALUES (NULL, 'hip-hop', 'playlist.png');
INSERT INTO public.playlists  (playlist_public, playlist_name, playlist_cover) VALUES (false, 'crust', 'playlist.png');
INSERT INTO public.playlists  (playlist_public, playlist_name, playlist_cover) VALUES (false, 'hardcore', 'playlist.png');
INSERT INTO public.playlists  (playlist_public, playlist_name, playlist_cover) VALUES (false, 'metal', 'playlist.png');
INSERT INTO public.playlists  (playlist_public, playlist_name, playlist_cover) VALUES (false, 'dbeat', 'playlist.png');


--
-- Data for Name: playlists_x_tracks; Type: TABLE DATA; Schema: public; Owner: play_backend_user
--

INSERT INTO public.playlists_x_tracks VALUES (1, 20);
INSERT INTO public.playlists_x_tracks VALUES (3, 21);
INSERT INTO public.playlists_x_tracks VALUES (9, 23);
INSERT INTO public.playlists_x_tracks VALUES (1, 1);
INSERT INTO public.playlists_x_tracks VALUES (1, 7);
INSERT INTO public.playlists_x_tracks VALUES (1, 23);
INSERT INTO public.playlists_x_tracks VALUES (1, 10);
INSERT INTO public.playlists_x_tracks VALUES (1, 12);
INSERT INTO public.playlists_x_tracks VALUES (2, 21);
INSERT INTO public.playlists_x_tracks VALUES (2, 7);
INSERT INTO public.playlists_x_tracks VALUES (2, 15);
INSERT INTO public.playlists_x_tracks VALUES (3, 1);
INSERT INTO public.playlists_x_tracks VALUES (3, 10);
INSERT INTO public.playlists_x_tracks VALUES (8, 2);
INSERT INTO public.playlists_x_tracks VALUES (8, 12);
INSERT INTO public.playlists_x_tracks VALUES (8, 21);
INSERT INTO public.playlists_x_tracks VALUES (9, 20);
INSERT INTO public.playlists_x_tracks VALUES (9, 7);
INSERT INTO public.playlists_x_tracks VALUES (9, 12);
INSERT INTO public.playlists_x_tracks VALUES (9, 15);
INSERT INTO public.playlists_x_tracks VALUES (9, 21);
INSERT INTO public.playlists_x_tracks VALUES (7, 3);


--
-- Data for Name: releases; Type: TABLE DATA; Schema: public; Owner: play_backend_user
--

INSERT INTO public.releases (release_name, release_year, artist_id, release_cover) VALUES ('Шлемодержавие', '2019-03-11', 1, 'shlem.jpg');
INSERT INTO public.releases (release_name, release_year, artist_id, release_cover) VALUES ('Крысы', '2017-03-12', 2, 'karzer.jpg');
INSERT INTO public.releases (release_name, release_year, artist_id, release_cover) VALUES ('Оскал', '2017-03-12', 3, 'oskal.jpg');
INSERT INTO public.releases (release_name, release_year, artist_id, release_cover) VALUES ('Low Teens', '2018-03-12', 4, 'etid.jpg');
INSERT INTO public.releases (release_name, release_year, artist_id, release_cover) VALUES ('Золотые Хиты', '2020-03-12', 1, 'shlem2.jpg');
INSERT INTO public.releases (release_name, release_year,artist_id,  release_cover) VALUES ('Slaves Beyond Death', '2017-03-12', 6, 'blackbreath.jpg');
INSERT INTO public.releases (release_name, release_year,artist_id,  release_cover) VALUES ('Beacon of Faith', '2018-03-12', 5, 'baptists.jpg');
INSERT INTO public.releases (release_name, release_year,artist_id,  release_cover) VALUES ('Герой асфальта', '1990-03-11', 10, 'aria.jpg');
INSERT INTO public.releases (release_name, release_year,artist_id,  release_cover) VALUES ('Shit Happens', '2008-03-11', 4, 'etid2.jpg');
INSERT INTO public.releases (release_name, release_year,artist_id,  release_cover) VALUES ('From parts unknown', '2008-03-11', 4, 'etid3.jpg');
INSERT INTO public.releases (release_name, release_year,artist_id,  release_cover) VALUES ('Splid', '2020-02-11', 7, 'kvelertak.jpg');
INSERT INTO public.releases (release_name, release_year,artist_id,  release_cover) VALUES ('MotorPunk', '2017-02-11', 8, 'dukenukem.jpg');
INSERT INTO public.releases (release_name, release_year,artist_id,  release_cover) VALUES ('Mediocre Generica', '2012-02-11', 9, 'leftovercrack.jpg');


--
-- Data for Name: tracks; Type: TABLE DATA; Schema: public; Owner: play_backend_user
--

INSERT INTO public.tracks (artist_id, release_id, track_name) values (1, 1, 'Имя его Шлем');
INSERT INTO public.tracks (artist_id, release_id, track_name) values(1, 1, 'Бой топорами');
INSERT INTO public.tracks (artist_id, release_id, track_name)values (1, 1, 'Чёрная водка');
INSERT INTO public.tracks (artist_id, release_id, track_name)values (1, 1, 'Хекс');
INSERT INTO public.tracks (artist_id, release_id, track_name) values (1, 1, 'Хуярит так, что охуеть');
INSERT INTO public.tracks (artist_id, release_id, track_name) values (1, 1, 'Сорни-Най');
INSERT INTO public.tracks (artist_id, release_id, track_name) values (2, 2, 'Крысы');
INSERT INTO public.tracks (artist_id, release_id, track_name) values (2, 2, 'Ересь');
INSERT INTO public.tracks (artist_id, release_id, track_name) values (1, 5, 'Кукулькан');
INSERT INTO public.tracks (artist_id, release_id, track_name) values (4, 4, 'Fear and Trembling (feat. Tim Singer of Deadguy)');
INSERT INTO public.tracks (artist_id, release_id, track_name) values (4, 4, 'Glitches');
INSERT INTO public.tracks (artist_id, release_id, track_name) values (4, 4, 'C++ (Love Will Get You Killed)');
INSERT INTO public.tracks (artist_id, release_id, track_name) values (4, 4, 'Two Summers');
INSERT INTO public.tracks (artist_id, release_id, track_name) values (4, 4, 'Awful Lot');
INSERT INTO public.tracks (artist_id, release_id, track_name) values (4, 4, 'I Didnt Want to Join Your Stupid Cult Anyway');
INSERT INTO public.tracks (artist_id, release_id, track_name) values (4, 4, 'It Remembers');
INSERT INTO public.tracks (artist_id, release_id, track_name) values (4, 4, 'Petal');
INSERT INTO public.tracks (artist_id, release_id, track_name) values (4, 4, 'The Coin Has a Say');
INSERT INTO public.tracks (artist_id, release_id, track_name) values (4, 4, 'Religion of Speed');
INSERT INTO public.tracks (artist_id, release_id, track_name) values (4, 4, 'Just as Real but Not as Brightly Lit');
INSERT INTO public.tracks (artist_id, release_id, track_name) values (6, 6, 'Pleasure, Pain, Disease');
INSERT INTO public.tracks (artist_id, release_id, track_name) values (6, 6, 'Slaves Beyond Death');
INSERT INTO public.tracks (artist_id, release_id, track_name) values (6, 6, 'Reaping Flesh');
INSERT INTO public.tracks (artist_id, release_id, track_name) values (6, 6, 'Seed Of Cain');
INSERT INTO public.tracks (artist_id, release_id, track_name) values (6, 6, 'Arc Of Violence ');
INSERT INTO public.tracks (artist_id, release_id, track_name) values (5, 7, 'Worse Than Hate');
INSERT INTO public.tracks (artist_id, release_id, track_name) values (5, 7, 'Absolved of Life / Spent Cells');
INSERT INTO public.tracks (artist_id, release_id, track_name) values (5, 7, 'Beacon of Faith');
INSERT INTO public.tracks (artist_id, release_id, track_name) values (5, 7, 'Gift Taker');
INSERT INTO public.tracks (artist_id, release_id, track_name) values (5, 7, 'Capsule');
INSERT INTO public.tracks (artist_id, release_id, track_name) values (8, 8, 'Герой');
INSERT INTO public.tracks (artist_id, release_id, track_name) values (3, 3, 'Оскал');


--
-- Data for Name: user_x_playlist; Type: TABLE DATA; Schema: public; Owner: play_backend_user
--

INSERT INTO public.user_x_playlist VALUES (3, 1);
INSERT INTO public.user_x_playlist VALUES (7, 1);
INSERT INTO public.user_x_playlist VALUES (8, 1);
INSERT INTO public.user_x_playlist VALUES (9, 1);


--
-- Data for Name: users; Type: TABLE DATA; Schema: public; Owner: play_backend_user
--

INSERT INTO public.users VALUES (1, 'johndoe', 'userfastapitest@gmail.com', '$6$rounds=656000$6cGZEyWFOnnuLzDP$CccXwdElsPja78LFjYXlVhXzqoUI4JXUepyuADOvM3Ju6M8iCYATHO07X/dIzmOtTVw3Tys8q5A2xJR6ZJgSC/', false, true);


--
-- Name: artists_id_seq; Type: SEQUENCE SET; Schema: public; Owner: play_backend_user
--

--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_email_key UNIQUE (email);

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_username_key UNIQUE (username);

ALTER TABLE ONLY public.playlists
    ADD CONSTRAINT playlists_playlist_name_key UNIQUE (playlist_name);

ALTER TABLE ONLY public.playlists_x_tracks
    ADD CONSTRAINT playlists_x_tracks_playlist_id_fkey FOREIGN KEY (playlist_id) REFERENCES public.playlists(playlist_id);

ALTER TABLE ONLY public.playlists_x_tracks
    ADD CONSTRAINT playlists_x_tracks_track_id_fkey FOREIGN KEY (track_id) REFERENCES public.tracks(track_id);

ALTER TABLE ONLY public.releases
    ADD CONSTRAINT releases_artist_id_fkey FOREIGN KEY (artist_id) REFERENCES public.artists(artist_id);

ALTER TABLE ONLY public.tracks
    ADD CONSTRAINT tracks_artist_id_fkey FOREIGN KEY (artist_id) REFERENCES public.artists(artist_id);

ALTER TABLE ONLY public.tracks
    ADD CONSTRAINT tracks_release_id_fkey FOREIGN KEY (release_id) REFERENCES public.releases(release_id);

ALTER TABLE ONLY public.user_x_playlist
    ADD CONSTRAINT user_x_playlist_playlist_id_fkey FOREIGN KEY (playlist_id) REFERENCES public.playlists(playlist_id);

ALTER TABLE ONLY public.user_x_playlist
    ADD CONSTRAINT user_x_playlist_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(user_id);
