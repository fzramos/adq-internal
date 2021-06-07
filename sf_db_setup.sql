// Setting contexts
USE ROLE SYSADMIN;
USE WAREHOUSE COMPUTE_WH;

// Create Database ADQ
CREATE DATABASE ADQ;

//SET CONTEXT TO DATABASE ADQ;
USE DATABASE ADQ;
USE SCHEMA PUBLIC;

// Creating auto increment sequences of IDs for tables
CREATE OR REPLACE SEQUENCE "ADQ"."PUBLIC".user_id_seq START 0 INCREMENT 1;
CREATE OR REPLACE SEQUENCE "ADQ"."PUBLIC".dp_id_seq START 0 INCREMENT 1;
CREATE OR REPLACE SEQUENCE "ADQ"."PUBLIC".cp_id_seq START 0 INCREMENT 1;

// Creating User table and inserting a User
CREATE OR REPLACE TRANSIENT TABLE user (
  user_id integer PRIMARY KEY DEFAULT user_id_seq.nextval,
  acct_number integer NOT NULL
);
INSERT INTO user (acct_number) VALUES
    (12345);

CREATE OR REPLACE TRANSIENT TABLE data_type (
  type_id integer PRIMARY KEY NOT NULL,
  name VARCHAR(8) NOT NULL
);

INSERT INTO data_type VALUES
    (0, 'int'),
    (1, 'float'),
    (2, 'str'),
    (3, 'datetime'),
    (4, 'error');

// Create data_profile table and column_profile table
CREATE OR REPLACE TRANSIENT TABLE data_profile (
  dp_id integer PRIMARY KEY DEFAULT dp_id_seq.nextval, -- auto incrementing IDs   
  user_id integer NOT NULL references user(user_id),
  created_at timestamp DEFAULT current_timestamp()
);

CREATE OR REPLACE TRANSIENT TABLE column_profile (
  cp_id integer PRIMARY KEY DEFAULT cp_id_seq.nextval, -- auto incrementing IDs   
  dp_id integer NOT NULL references data_profile(dp_id),
  column_name VARCHAR(100),
  type_id integer NOT NULL references data_type(type_id),
  value_count integer,
  missing integer,
  percent_missing float,
  unique_count integer,
  max_length integer,
  min_length integer,
  mean float,
  stdev float,
  minimum float,
  perc25 float,
  perc50 float,
  perc75 float,
  maximum float
);

// Run these to see if data profiles have been sucessfully uploaded
SELECT * FROM user;
SELECT * FROM data_profile;
SELECT * FROM column_profile;
SELECT * FROM data_type;

// See all data profiles connected to a user
SELECT u.user_id, dp.dp_id, c.COLUMN_NAME, dt.name AS "data_type", c.VALUE_COUNT, c.MISSING, 
c.PERCENT_MISSING, c.UNIQUE_COUNT, c.MAX_LENGTH, c.MIN_LENGTH, c.STDEV, c.MINIMUM, c.PERC25,
c.PERC50, c.PERC75, c.MAXIMUM
FROM column_profile c
JOIN data_type dt
ON c.type_id = dt.type_id
JOIN data_profile dp
ON dp.dp_id = c.dp_id
JOIN user u
ON u.user_id = dp.user_id
WHERE u.user_id = 0;