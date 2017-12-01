--DROP SCHEMA IF EXISTS simco_dev;
--CREATE SCHEMA simco_dev;

--DROP GROUP simco_dev_rw;
--CREATE GROUP simco_dev_rw;

--GRANT USAGE ON SCHEMA simco_dev TO GROUP simco_dev_rw;
--GRANT SELECT, UPDATE, DELETE, INSERT ON ALL TABLES IN SCHEMA simco_dev TO GROUP simco_dev_rw;
--GRANT CREATE ON SCHEMA simco_dev TO GROUP simco_dev_rw;

--DROP USER IF EXISTS dev_etl;
--CREATE USER sor_etl WITH PASSWORD 'Passw0rd' IN GROUP simco_dev_rw;

CREATE TABLE asset (
	id INTEGER NOT NULL,
	type VARCHAR(10) NOT NULL,
	symbol VARCHAR(25) NOT NULL,
	description VARCHAR(25) NOT NULL,
	exchange VARCHAR(10) NOT NULL,
	size INTEGER,
	PRIMARY KEY (id)
);
CREATE TABLE allocation (
	id INTEGER NOT NULL,
  date_mod VARCHAR(28) NOT NULL,
	portfolio VARCHAR(10) NOT NULL,
	asset_id INTEGER,
	allocation FLOAT NOT NULL,
	PRIMARY KEY (id),
	FOREIGN KEY(asset_id) REFERENCES asset (id)
);

INSERT INTO asset Values (0, "equity", "AMZN", "Amazon", "NASDAQ", 1);
INSERT INTO asset Values (1, "equity", "GOOG", "Alphabet", "NASDAQ", 1);
INSERT INTO asset Values (2, "future", "VIX", "CBOE Volatility Index", "CBOE", 1000);
INSERT INTO asset Values (3, "future", "ES", "S&P500 e-mini", "CME", 50);
INSERT INTO asset Values (4, "option", "AMZN 171215C01170000", "Amazon.com, Inc. Dec 15 2017 1170 Call", "CBO", 100);

INSERT INTO allocation Values (0, "2017-06-01T23:00:00.00Z", "port1", 0, 0.05);
INSERT INTO allocation Values (1, "2017-06-01T23:00:00.00Z", "port1", 1, 0.10);
INSERT INTO allocation Values (2, "2017-06-01T23:00:00.00Z", "port1", 2, 0.12);
INSERT INTO allocation Values (3, "2017-06-01T23:00:00.00Z", "port1", 3, 0.08);
