DROP TABLE IF EXISTS CUSTODISCE;
DROP TABLE IF EXISTS APPARTIENE;
DROP TABLE IF EXISTS PRENDE_IN_PRESTITO;
DROP TABLE  IF EXISTS PUBBLICA;
DROP TABLE IF EXISTS PRENOTAZIONI_POSTO;
DROP TABLE IF EXISTS UTENTE;
DROP TABLE IF EXISTS COPIA_LIBRO;
DROP TABLE IF EXISTS LIBRO;
DROP TABLE IF EXISTS EDITORE;
DROP TABLE IF EXISTS GENERE;
DROP TABLE IF EXISTS AUTORE;
DROP TABLE IF EXISTS BIBLIOTECA;


create table AUTORE
(
    nome    char(12) null,
    cognome char(15) null,
    id_aut  int not null primary key AUTO_INCREMENT
);


create table BIBLIOTECA
(
    Id_biblioteca int not null primary key AUTO_INCREMENT,
    Nome          char(50) null,
    Num_telefono  char(13) null,
    Indirizzo     char(50) null,
    Cord_X        float(15) null,
    Cord_Y        float(15) null,
    Posti_aula_studio int       
);


create table EDITORE
(
    id_editore int not null primary key AUTO_INCREMENT, 
    nome char(50) null
);

create table GENERE
(
    id_genere          int       not null
        primary key AUTO_INCREMENT,
    descrizione_genere char(100) null
);

create table LIBRO
(
    ISBN        int      not null primary key,
    genere_lib  int      null,
    editore_lib int      null,
    tipo_lib    int      null,
    titolo      char(30) null,
    valutazione int      null,
    edizione    char(50) null,
    copertina   char(50) null,
    autore_lib  int null,
    descrizione char(250) null,
    constraint chiave_esterna_lib
        foreign key (editore_lib) references EDITORE (id_editore),
    constraint chiave_esterna_lib2
        foreign key (genere_lib) references GENERE (id_genere),
    constraint chiave_esterna_lib3
        foreign key (autore_lib) references AUTORE (id_aut)
);

create table COPIA_LIBRO
(
    num_copia int not null primary key AUTO_INCREMENT,
    qt int not null,
    isbn int not null,
    id_bibl_copia int not null,
    Disponibile boolean,
    constraint chiave_esterna_copia
        foreign key (id_bibl_copia) references BIBLIOTECA (Id_biblioteca),
    constraint chiave_esterna_copia1
        foreign key (isbn) references LIBRO (ISBN)
);

create table CUSTODISCE
(
    Id_biblioteca_1 int null,
    num_copia_1     int null,
    constraint chiave_esterna_cust
        foreign key (Id_biblioteca_1) references BIBLIOTECA (Id_biblioteca),
    constraint chiave_esterna_cust1
        foreign key (num_copia_1) references COPIA_LIBRO (num_copia)
);


create table APPARTIENE
(
    ISBN_lib_2  int null,
    num_copia_2 int null,
    constraint chiave_esterna_app
        foreign key (ISBN_lib_2) references LIBRO (ISBN),
    constraint chiave_esterna_app1
        foreign key (num_copia_2) references COPIA_LIBRO (num_copia)
);

create table PUBBLICA
(
    id_aut_1   int null,
    ISBN_lib_1 int null,
    constraint chiave_esterna_pubb
        foreign key (id_aut_1) references AUTORE (id_aut),
    constraint chiave_esterna_pubbl1
        foreign key (ISBN_lib_1) references LIBRO (ISBN)
);

create table UTENTE
(
    nome_ut      char(50)  null,
    cognome_ut   char(50)  null,
    email        char(40)  null,
    CF           char(20)  not null
        primary key,
    sesso        char      null,
    data_nascita date      null,
    PW           char(200)  null,
    QR           char(150) null,
    citta_ut     char(40)  null,
    token_ut     char(100) null,
    admin        int       null,
    constraint chiave_esterna_admin
        foreign key (admin) references BIBLIOTECA (Id_biblioteca)
);

create table PRENDE_IN_PRESTITO
(
    Id_prestito          int  not null primary key AUTO_INCREMENT,
    codice_fiscale       char(20) null,
    num_copia_prestito   int      null,
    data_prestito        date     null,
    data_di_restituzione date     null,
    restituito boolean,
    constraint chiave_esterna_pr
        foreign key (codice_fiscale) references UTENTE (CF),
    constraint chiave_esterna_pr1
        foreign key (num_copia_prestito) references COPIA_LIBRO (num_copia)
);

create table PRENOTAZIONI_POSTO
(
    Id_prenotazione      int not null primary key AUTO_INCREMENT,   
    Id_biblioteca_prenotazione int,        
    Utente   char(20),
    Data_prenotazione date not null,
    constraint chiave_esterna_prenotazione_utente
        foreign key (Utente) references UTENTE (CF),
    constraint chiave_esterna_bib_posto foreign key (Id_biblioteca_prenotazione) references BIBLIOTECA(Id_biblioteca)
        
)


