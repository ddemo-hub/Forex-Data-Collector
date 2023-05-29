CREATE TABLE IF NOT EXISTS Forex_Rates(
    timestamp BIGINT,
    currency VARCHAR(3),
    exchange VARCHAR(20),
    buy_sell VARCHAR(4),
    rate FLOAT,
    PRIMARY KEY (timestamp, currency, exchange, buy_sell),
    CHECK (buy_sell in ('BUY', 'SELL')),
    CHECK (currency in ('USD', 'EUR', 'GBP')),
    CHECK (exchange in ('TCMB', 'yapikredi'))
);
