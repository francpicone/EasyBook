INSERT INTO `AUTORE` (`nome`, `cognome`, `id_aut`) VALUES
('Thomas', 'Cormen', 0),
('James', 'Kurose', 0),
('Paolo', 'Atzeni', 0),
('Andrew', 'Tanembaum', 0),
('Ian', 'Sommerville', 0),
('Alan', 'Dix', 0),
('Al', 'Kelley', 0),
('Bjarne', 'Stroustrup', 0),
('Italo', 'Calvino', 0),
('George', 'R_R Martin', 0),
('J_R_R', 'Tolkien', 0),
('Stephen', 'King', 0),
('Erasmo', 'Da Rotterdam', 0),
('George', 'Orwell', 0),
('William', 'Shakespeare', 0),
('Dante', 'Alighieri', 0),
(' F.S', 'Fitzgerald', 0),
('Charlotte', 'Brontë', 0),
('Miguel', 'De Cervantes', 0),
('Jane', 'Austen', 0),
('Alexandre', 'Dumas', 0),
('Omero', '', 0);

INSERT INTO `BIBLIOTECA` (`Id_biblioteca`, `Nome`, `Num_telefono`, `Indirizzo`, `Cord_X`, `Cord_Y`, `Posti_aula_studio`) VALUES
(0, 'Biblioteca Comunale di Salerno', '0816547821', 'Via Bastia, 1-3', 40.6811, 14.764, 1),
(0, 'Biblioteca Comunale di Pomigliano', '3388354219', 'Corso Vittorio Emanuele', 40.9087, 14.3875, 60),
(0, 'Biblioteca Comunale \"I.Caliendo\"', '0814138192', 'Corso Tommaso Vitale', 40.9252, 14.5282, 40),
(0, 'Biblioteca Universitaria di Napoli', '0815467878', 'Via Giovanni Paladino 39', 40.8473, 14.2571, 80),
(0, 'Biblioteca Statale Oratoriana dei Girolamini', '0816789121', 'Via Duomo, 114', 40.8524, 14.2588, 45),
(0, 'Biblioteca Comunale di Frattaminore', '0811235421', ' Via Filippo Turati', 40.9645, 14.2774, 120),
(0, 'Biblioteca Di Napoli San Giovanni', '0819536728', ' Piazza Giambattista Pacichelli, 10', 40.8311, 14.3115, 90),
(0, 'Biblioteca nazionale centrale di Roma', '0819216985', 'Viale Castro Pretorio, 105', 41.9355, 12.4982, 240);

INSERT INTO `EDITORE` (`id_editore`, `nome`) VALUES
(0, 'McGraw-Hill'),
(0, 'Pearson'),
(0, 'Zanichelli'),
(0, 'Addison-Wesley Professional'),
(0, 'Mondadori'),
(0, 'Bompiani'),
(0, 'Sperling Paperback'),
(0, 'Feltrinelli');

INSERT INTO `GENERE` (`id_genere`, `descrizione_genere`) VALUES
(0, 'Informatica'),
(0, 'Romanzo'),
(0, 'Fantasy'),
(0, 'Horror'),
(0, 'Tragedia'),
(0, 'Poema'),
(0, 'Saggio');

INSERT INTO `UTENTE` (`nome_ut`, `cognome_ut`, `email`, `CF`, `sesso`, `data_nascita`, `PW`, `QR`, `citta_ut`, `token_ut`, `admin`) VALUES
('Biblioteca Comunale', 'di Pomigliano', 'bibpom@bib.it', '438589358973', NULL, '2021-12-16', 'pbkdf2:sha256:260000$6OYb5LvgfNxlLgzn$ca4ee2a25643961221a41c42f7d77af6d5389b3e3d8028ec6c66600082a833c2', NULL, 'Pomigliano', 'liykltetegebpxfykbvrsdnpduvdnbdlhwwfxowullbrapaqgdviitvsnrhmvpob', 1),
('Mario', 'Rossi', 'mario.rossi@gmail.com', 'MRS', NULL, '2021-12-16', 'pbkdf2:sha256:260000$rxne1D3cJNUmAd2m$9752b6071319952eb391be888d19b2948279979856377581094958ab8230fc33', NULL, 'Napoli', 'vuxwlceusdcmfinnyowgyhuxftuocapnrhjrbijxnzopwpnqswyhdurkwxtjobfb', NULL),
('Francesco', 'Picone', 'francescopicone@francesco.it', 'PCN', NULL, '2021-12-16', 'pbkdf2:sha256:260000$BmB0608N74Vx6Cj5$123598c54afec5c13df0e25e84522afe768a5f26d845686201f729760144e480', NULL, 'Napoli', 'glfgqdoeiglqqguxldwvsvlugjqrhdfrvjpmrcpjfytntetnngxhbbiugrxsxjxd', NULL);