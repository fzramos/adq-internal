USE ROLE SYSADMIN;
USE WAREHOUSE COMPUTE_WH;

// Create Database ADQ
CREATE DATABASE ADQ;

//SET CONTEXT TO DATABASE ADQ;
USE DATABASE ADQ;
USE SCHEMA PUBLIC;

// Creating auto increment sequences of ID's for tables
CREATE SEQUENCE "ADQ"."PUBLIC".dp_id_seq START 1 INCREMENT 1;
CREATE SEQUENCE "ADQ"."PUBLIC".cp_id_seq START 1 INCREMENT 1;

// Create data_profile table and column_profile table
// Making them transient since don't need extra data protection of permanent tables
CREATE OR REPLACE TRANSIENT TABLE data_profile (
  dp_id integer PRIMARY KEY DEFAULT dp_id_seq.nextval, -- auto incrementing IDs   
  parent_id integer DEFAULT 0 ,
  created_at timestamp DEFAULT current_timestamp()
);

CREATE OR REPLACE TRANSIENT TABLE column_profile (
  cp_id integer PRIMARY KEY DEFAULT cp_id_seq.nextval, -- auto incrementing IDs   
  dp_id integer NOT NULL references data_profile(dp_id),
  column_name VARCHAR(100),
  data_type VARCHAR(100),
  "count" integer,
  missing integer,
  percent_missing float,
  unique_count integer,
  max_length integer,
  min_length integer,
  mean float,
  "std" float,
  "min" float,
  "25%" float,
  "75%" float,
  "max" float
);