// Setting contexts
USE ROLE SYSADMIN;
USE WAREHOUSE COMPUTE_WH;

// Create Database ADQ
CREATE DATABASE ADQ;

//SET CONTEXT TO DATABASE ADQ;
USE DATABASE ADQ;
USE SCHEMA PUBLIC;

// Creating auto increment sequences of IDs for tables
CREATE OR REPLACE SEQUENCE "ADQ"."PUBLIC".dp_id_seq START 1 INCREMENT 1;
CREATE OR REPLACE SEQUENCE "ADQ"."PUBLIC".cp_id_seq START 1 INCREMENT 1;


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
  parent_id integer DEFAULT 0 ,
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
SELECT * FROM data_profile;
SELECT * FROM column_profile;

// Run for an example of a full data profile including the name of column's data type
SELECT c.*, dt.name AS "data_type" FROM column_profile c
JOIN data_type dt
ON c.type_id = dt.type_id
//WHERE DP_ID = 1
;
// Add WHERE if you want to look at a single profile