--
-- PostgreSQL database dump
--

SET statement_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SET check_function_bodies = false;
SET client_min_messages = warning;

SET search_path = public, pg_catalog;

--
-- Data for Name: vida_core_country; Type: TABLE DATA; Schema: public; Owner: -
--

SET SESSION AUTHORIZATION DEFAULT;

ALTER TABLE vida_core_country DISABLE TRIGGER ALL;

COPY vida_core_country (iso_code, name) FROM stdin;
US	United States of America
\.


ALTER TABLE vida_core_country ENABLE TRIGGER ALL;

--
-- Data for Name: vida_core_address; Type: TABLE DATA; Schema: public; Owner: -
--

ALTER TABLE vida_core_address DISABLE TRIGGER ALL;

COPY vida_core_address (id, address_line1, address_line2, city, state_province, postal_code, country_id, geom) FROM stdin;
8	PO Box 154		Newkirk	OK	74647-0154	US	\N
100226	Zuni Independent Fire District # 8	\N	\N	\N	13010	43121	43121	505-782-7191	505-782-7224	Mostly Volunteer	Local (includes career  combination  and volunteer)		2015-03-07 19:49:11.779002+00	2015-03-07 19:49:11.779022+00	NM
\.


ALTER TABLE firestation_firedepartment ENABLE TRIGGER ALL;

--
-- Name: firestation_firedepartment_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('firestation_firedepartment_id_seq', 100226, true);


--
-- PostgreSQL database dump complete
--

