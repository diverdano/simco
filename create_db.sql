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
  coupon FLOAT,
  expiry VARCHAR(25),
  strike INTEGER,
	PRIMARY KEY (id)
);
CREATE TABLE allocation (
	id INTEGER NOT NULL,
  date_mod VARCHAR(25) NOT NULL,
	portfolio VARCHAR(10) NOT NULL,
	asset_id INTEGER,
	allocation FLOAT NOT NULL,
	PRIMARY KEY (id),
	FOREIGN KEY(asset_id) REFERENCES asset (id)
);

INSERT INTO asset (type, symbol, description, exchange, size) Values
  ("equity", "AMZN", "Amazon.com, Inc.", "NASDAQ", 1),
  ("equity", "GOOG", "Alphabet, Inc.", "NASDAQ", 1),
  ("future", "VIX", "CBOE Volatility Index", "CBOE", 1000),
  ("future", "ES", "S&P500 e-mini", "CME", 50),
  ("option", "AMZN 171215C01170000", "Amazon.com, Inc. Dec 15 2017 1170 Call", "CBO", 100),
  ("equity", "AAPL", "Apple, Inc.", "NASDAQ", 1),
  ("equity", "IBM", "International Business Machines, Inc.", "NYSE", 1),
  ("bond", "912828U57", "US Treasury Note 2.125 30nov2023 7Y", "OTC", 1000);

INSERT INTO allocation (date_mod, portfolio, asset_id, allocation) Values
  ("2017-06-01T23:00:00Z", "port1", 1, 0.25),
  ("2017-06-01T23:00:00Z", "port1", 3, 0.25),
  ("2017-06-01T23:00:00Z", "port1", 5, 0.25),
  ("2017-06-01T23:00:00Z", "port1", 8, 0.25),
  ("2017-07-01T23:00:00Z", "port1", 1, 0.20),
  ("2017-07-01T23:00:00Z", "port1", 3, 0.20),
  ("2017-07-01T23:00:00Z", "port1", 5, 0.20),
  ("2017-07-01T23:00:00Z", "port1", 8, 0.20),
  ("2017-08-01T23:00:00Z", "port1", 1, 0.15),
  ("2017-08-01T23:00:00Z", "port1", 3, 0.15),
  ("2017-08-01T23:00:00Z", "port1", 5, 0.15),
  ("2017-08-01T23:00:00Z", "port1", 8, 0.15),
  ("2017-09-01T23:00:00Z", "port1", 1, 0.30),
  ("2017-09-01T23:00:00Z", "port1", 3, 0.30),
  ("2017-09-01T23:00:00Z", "port1", 5, 0.30);
