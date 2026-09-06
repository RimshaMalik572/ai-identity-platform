
// ================================================================
// AI IDENTITY PLATFORM — NEO4J GRAPH SCHEMA
// ================================================================

CREATE CONSTRAINT user_id_unique IF NOT EXISTS
FOR (u:User)
REQUIRE u.user_id IS UNIQUE;

CREATE CONSTRAINT device_id_unique IF NOT EXISTS
FOR (d:Device)
REQUIRE d.device_id IS UNIQUE;

CREATE CONSTRAINT document_id_unique IF NOT EXISTS
FOR (d:Document)
REQUIRE d.document_id IS UNIQUE;

CREATE CONSTRAINT fraud_case_id_unique IF NOT EXISTS
FOR (f:FraudCase)
REQUIRE f.case_id IS UNIQUE;

CREATE INDEX user_phone IF NOT EXISTS
FOR (u:User)
ON (u.phone);

CREATE INDEX user_ip IF NOT EXISTS
FOR (u:User)
ON (u.ip_address);

CREATE INDEX biometric_user IF NOT EXISTS
FOR (b:BiometricProfile)
ON (b.user_id);
