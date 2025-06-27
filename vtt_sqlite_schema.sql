
PRAGMA foreign_keys = ON;

-- Tabela User
DROP TABLE IF EXISTS User;

CREATE TABLE IF NOT EXISTS User (
  idUser INTEGER PRIMARY KEY,
  password TEXT NOT NULL,
  email TEXT NOT NULL UNIQUE,
  username TEXT NOT NULL
);

-- Tabela Gametable
DROP TABLE IF EXISTS Gametable;

CREATE TABLE IF NOT EXISTS Gametable (
  idGametable INTEGER NOT NULL,
  gametablename TEXT,
  gm_userid INTEGER NOT NULL,
  PRIMARY KEY (idGametable, gm_userid),
  FOREIGN KEY (gm_userid) REFERENCES User(idUser)
);
