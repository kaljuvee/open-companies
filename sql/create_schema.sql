-- Create schema for company data
CREATE SCHEMA IF NOT EXISTS company;

-- Companies table
CREATE TABLE IF NOT EXISTS company.companies (
    id SERIAL PRIMARY KEY,
    registry_code VARCHAR(50) UNIQUE NOT NULL,
    name TEXT NOT NULL,
    status VARCHAR(50),
    country_code VARCHAR(2) DEFAULT 'EE',
    address TEXT,
    registration_date TIMESTAMP,
    liquidation_date TIMESTAMP,
    bankruptcy_date TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Ultimate Beneficial Owners (UBOs) table
CREATE TABLE IF NOT EXISTS company.ubos (
    id SERIAL PRIMARY KEY,
    company_id INTEGER REFERENCES company.companies(id) ON DELETE CASCADE,
    name TEXT NOT NULL,
    identification_code VARCHAR(50),
    country VARCHAR(100),
    ownership_percentage DECIMAL(5,2),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Company events table (formations, liquidations, etc.)
CREATE TABLE IF NOT EXISTS company.events (
    id SERIAL PRIMARY KEY,
    company_id INTEGER REFERENCES company.companies(id) ON DELETE CASCADE,
    event_type VARCHAR(50) NOT NULL,
    event_date TIMESTAMP NOT NULL,
    description TEXT,
    source_url TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Statistics table for tracking deletions and other metrics
CREATE TABLE IF NOT EXISTS company.statistics (
    id SERIAL PRIMARY KEY,
    country_code VARCHAR(2) NOT NULL,
    stat_type VARCHAR(50) NOT NULL,
    stat_date DATE NOT NULL,
    count INTEGER DEFAULT 0,
    metadata JSONB,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(country_code, stat_type, stat_date)
);

-- Create indexes for better query performance
CREATE INDEX IF NOT EXISTS idx_companies_status ON company.companies(status);
CREATE INDEX IF NOT EXISTS idx_companies_country ON company.companies(country_code);
CREATE INDEX IF NOT EXISTS idx_companies_registry_code ON company.companies(registry_code);
CREATE INDEX IF NOT EXISTS idx_events_company_id ON company.events(company_id);
CREATE INDEX IF NOT EXISTS idx_events_type ON company.events(event_type);
CREATE INDEX IF NOT EXISTS idx_ubos_company_id ON company.ubos(company_id);
CREATE INDEX IF NOT EXISTS idx_statistics_country_date ON company.statistics(country_code, stat_date);

-- Update trigger for updated_at columns
CREATE OR REPLACE FUNCTION company.update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER update_companies_updated_at BEFORE UPDATE ON company.companies
    FOR EACH ROW EXECUTE FUNCTION company.update_updated_at_column();

CREATE TRIGGER update_ubos_updated_at BEFORE UPDATE ON company.ubos
    FOR EACH ROW EXECUTE FUNCTION company.update_updated_at_column();
