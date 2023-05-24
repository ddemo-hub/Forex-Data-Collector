CREATE TABLE IF NOT EXISTS Forex_Rates(
    timestamp BIGINT,
    currency VARCHAR(3),
    exchange VARCHAR(20),
    buy_sell VARCHAR(1),
    rate FLOAT,
    PRIMARY KEY (timestamp, currency, exchange, buy_sell),
    CHECK (buy_sell in ('buy', 'sell'))
);
