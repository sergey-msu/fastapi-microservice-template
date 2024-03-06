-- **************** Users ****************

CREATE TABLE "tokens" (
    "id"            SERIAL PRIMARY KEY,
    "create_date"   TIMESTAMP NOT NULL,
    "access_token"  VARCHAR(1024) NOT NULL,
    "refresh_token" VARCHAR(1024) NOT NULL
);
CREATE INDEX idx_tokens_create_date ON "tokens"(create_date);
