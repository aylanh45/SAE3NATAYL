DROP TABLE IF EXISTS Etape;
DROP TABLE IF EXISTS Mission;
DROP TABLE IF EXISTS Type_mission;
DROP TABLE IF EXISTS Agent;
DROP TABLE IF EXISTS Moyen_transport;
DROP TABLE IF EXISTS Lieu;

#mysql --user=nfoucaul  --password=mdp --host=serveurmysql --database=BDD_nfoucaul
CREATE TABLE Agent
(
    Id_Agent        INT AUTO_INCREMENT,
    Nom             VARCHAR(50),
    Prenom          VARCHAR(50),
    AdresseDomicile VARCHAR(50),
    Telephone       VARCHAR(10),
    AdresseTravail  VARCHAR(50),
    PRIMARY KEY (Id_Agent)
)
;

CREATE TABLE Type_mission
(
   Id_TypeMission INT AUTO_INCREMENT,
   LibelleTypeMission VARCHAR(50),
   PRIMARY KEY(Id_TypeMission)
);

CREATE TABLE Mission
(
    Id_Mission INT AUTO_INCREMENT,
    DateDébut  DATE,
    DateFin    DATE,
    Kg_CO2     NUMERIC(15, 2),
    Id_TypeMission INT NOT NULL ,
    Id_Agent   INT NOT NULL,
    Budget NUMERIC(15),
    PRIMARY KEY (Id_Mission),
    FOREIGN KEY (Id_TypeMission) REFERENCES Type_mission (Id_TypeMission) ,
    FOREIGN KEY (Id_Agent) REFERENCES Agent (Id_Agent)
)
;

CREATE TABLE Lieu
(
    Id_Lieu     INT AUTO_INCREMENT,
    LibelleLieu VARCHAR(50),
    PRIMARY KEY (Id_Lieu)
)
;

CREATE TABLE Moyen_transport
(
    Id_MoyenTransport INT AUTO_INCREMENT,
    LibelleTransport  VARCHAR(50),
    EmissionsCO2_km   NUMERIC(15, 5),
    PRIMARY KEY (Id_MoyenTransport)
)
;


CREATE TABLE Etape
(
    Id_Etape          INT AUTO_INCREMENT,
    DistanceParcourue INT,
    Id_MoyenTransport INT NOT NULL,
    Heure_depart    TIME ,
    Heure_arrivee   TIME ,
    Id_Lieu_depart    INT NOT NULL ,
    Id_Lieu_arrivee   INT NOT NULL ,
    Id_Mission        INT NOT NULL,
    PRIMARY KEY (Id_Etape),
    FOREIGN KEY (Id_MoyenTransport) REFERENCES Moyen_transport (Id_MoyenTransport),
    FOREIGN KEY (Id_Lieu_depart) REFERENCES Lieu (Id_Lieu),
    FOREIGN KEY (Id_Lieu_arrivee) REFERENCES Lieu (Id_Lieu),
    FOREIGN KEY (Id_Mission) REFERENCES Mission (Id_Mission)
)
;

INSERT INTO Lieu (Id_Lieu, LibelleLieu)
VALUES (NULL, 'Lyon'),
       (NULL, 'Marseilles'),
       (NULL, 'Grenobles'),
       (NULL, 'Paris'),
       (NULL, 'Poitiers'),
       (NULL, 'Poitiers'),
       (NULL, 'Belfort'),
       (NULL, 'Nice'),
       (NULL, 'Orléans'),
       (NULL, 'Avallon')
;

INSERT INTO Type_mission (Id_TypeMission, LibelleTypeMission)
VALUES (NULL, 'Infiltration'),
       (NULL, 'Espionnage'),
       (NULL, 'Audit'),
       (NULL, 'Recherche'),
       (NULL, 'Destruction'),
       (NULL, 'Conseil')
;


INSERT INTO Agent (Id_Agent, Nom, Prenom, AdresseDomicile, AdresseTravail, Telephone)
VALUES (NULL, 'Besoul', 'Bertrand', '9 rue de tilted tower', '6 rue de Flush Factory',06999999),
       (NULL, 'Amar', 'Oussama', '6 rue de Greasy Groove', '6 rue de Retail Row', 06555555),
       (NULL, 'Valouzz', 'Pidi', '6 rue de Retail Row', '69 rue de Haunted Hills', 067777777),
       (NULL, 'Foucault', 'Nathan', '69 rue de Haunted Hills', '6 rue de Retail Row', 0689696969),
       (NULL, 'Damidot', 'Valérie', '6 rue de Junk Junction', '6 rue de Junk Junction',06888888),
       (NULL, 'Haddouchi', 'Aylan', '6 rue de Flush Factory', '6 rue de Retail Row', 061111111)
;

INSERT INTO Mission (Id_Mission, DateDébut, DateFin, Kg_CO2, Id_Agent, Id_TypeMission, Budget)
VALUES (NULL, '2024-01-18', '2024-02-20', 60, 1, 1,1000),
       (NULL, '2024-02-23', '2024-02-27', 2822, 2, 2,2500),
       (NULL, '2024-03-12', '2024-03-12', 0.136, 3, 3,3000),
       (NULL, '2024-04-04', '2024-04-12', 4013, 4, 4,4000),
       (NULL, '2024-05-28', '2024-06-01', 47, 5, 5,6700)
;

INSERT INTO Moyen_transport (id_MoyenTransport, LibelleTransport, EmissionsCO2_km)
VALUES (NULL, 'Train', 0.19),
       (NULL, 'Avion', 4.9),
       (NULL, 'Tramway', 0.034),
       (NULL, 'TGV', 0.88),
       (NULL, 'Voiture', 0.214)
;

INSERT INTO Etape(Id_Etape, DistanceParcourue, id_MoyenTransport, Id_Mission, Heure_depart, Heure_arrivee, Id_Lieu_depart, Id_Lieu_arrivee)
VALUES (NULL, '315', 1, 1,'17:03:04','19:43:48',4, 5),
       (NULL, '576', 4, 2,'16:59:34','17:03:04',6,2),
       (NULL, '4', 3, 3,'09:38:50', '16:59:34',7,1),
       (NULL, '819', 2, 4,'16:59:34', '09:38:50',1, 3),
       (NULL, '224', 5, 5,'16:59:34', '19:43:48', 3,4)
;



SELECT * FROM Agent;
SELECT * FROM Moyen_transport;
SELECT * FROM Lieu;
SELECT * FROM Mission;
SELECT * FROM Etape;
