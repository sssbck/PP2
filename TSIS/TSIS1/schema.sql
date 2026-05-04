-- Создание таблицы групп
CREATE TABLE IF NOT EXISTS groups (
    id   SERIAL PRIMARY KEY,
    name VARCHAR(50) UNIQUE NOT NULL
);

-- Добавление новых полей в основную таблицу контактов
-- Предполагаем, что таблица contacts уже существует из практики 8
ALTER TABLE contacts ADD COLUMN IF NOT EXISTS email VARCHAR(100);
ALTER TABLE contacts ADD COLUMN IF NOT EXISTS birthday DATE;
ALTER TABLE contacts ADD COLUMN IF NOT EXISTS group_id INTEGER REFERENCES groups(id);
ALTER TABLE contacts ADD COLUMN IF NOT EXISTS created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP;

-- Создание таблицы телефонов (1-ко-многим)
CREATE TABLE IF NOT EXISTS phones (
    id         SERIAL PRIMARY KEY,
    contact_id INTEGER REFERENCES contacts(id) ON DELETE CASCADE,
    phone      VARCHAR(20)  NOT NULL,
    type       VARCHAR(10)  CHECK (type IN ('home', 'work', 'mobile'))
);

-- Начальное заполнение групп
INSERT INTO groups (name) VALUES ('Family'), ('Work'), ('Friend'), ('Other') ON CONFLICT DO NOTHING;