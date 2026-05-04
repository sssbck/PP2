-- 0. Гарантия уникальности имени (необходимо для UPSERT)
ALTER TABLE contacts DROP CONSTRAINT IF EXISTS contacts_name_key;
ALTER TABLE contacts ADD CONSTRAINT contacts_name_key UNIQUE (name);

CREATE OR REPLACE FUNCTION is_contact_exists(p_name VARCHAR)
RETURNS BOOLEAN AS $$
BEGIN
    -- Вернет True, если найдет хотя бы одну запись, и False, если нет
    RETURN EXISTS(SELECT 1 FROM contacts WHERE name = p_name);
END;
$$ LANGUAGE plpgsql;

-- 1, 7, 8: ЕДИНАЯ ПРОЦЕДУРА СОЗДАНИЯ/ОБНОВЛЕНИЯ (Используется для меню, CSV и JSON)
CREATE OR REPLACE PROCEDURE upsert_full_contact(
    p_name VARCHAR, p_email VARCHAR, p_birthday DATE, 
    p_group_name VARCHAR, p_phone VARCHAR, p_phone_type VARCHAR
) LANGUAGE plpgsql AS $$
DECLARE
    v_contact_id INT;
BEGIN
    -- Вставка или обновление основного контакта
    INSERT INTO contacts (name, email, birthday)
    VALUES (p_name, p_email, p_birthday)
    ON CONFLICT (name) DO UPDATE 
    SET email = EXCLUDED.email, birthday = EXCLUDED.birthday
    RETURNING id INTO v_contact_id;

    -- Привязка к группе (создаст группу, если её нет)
    IF p_group_name IS NOT NULL AND TRIM(p_group_name) <> '' THEN
        INSERT INTO groups (name) VALUES (TRIM(p_group_name)) ON CONFLICT (name) DO NOTHING;
        UPDATE contacts SET group_id = (SELECT id FROM groups WHERE name = TRIM(p_group_name))
        WHERE id = v_contact_id;
    END IF;

    -- Добавление телефона (только если передан)
    IF p_phone IS NOT NULL AND TRIM(p_phone) <> '' THEN
        INSERT INTO phones (contact_id, phone, type)
        VALUES (v_contact_id, p_phone, LOWER(p_phone_type));
    END IF;
END;
$$;

-- 2: РАСШИРЕННЫЙ ПОИСК
CREATE OR REPLACE FUNCTION search_contacts_extended(p_query VARCHAR)
RETURNS TABLE(id INT, name VARCHAR, email VARCHAR, phones TEXT, group_name VARCHAR) AS $$
BEGIN
    RETURN QUERY
    SELECT 
        c.id, 
        c.name, 
        c.email, 
        -- Добавляем DISTINCT сюда, чтобы убрать дубликаты номеров
        COALESCE(string_agg(DISTINCT p.phone || ' (' || p.type || ')', ', '), 'Нет телефона'), 
        COALESCE(g.name, 'Без группы')
    FROM contacts c
    LEFT JOIN phones p ON c.id = p.contact_id
    LEFT JOIN groups g ON c.group_id = g.id
    WHERE c.name ILIKE '%' || p_query || '%' 
       OR c.email ILIKE '%' || p_query || '%'
       OR p.phone ILIKE '%' || p_query || '%'
    GROUP BY c.id, g.name;
END;
$$ LANGUAGE plpgsql;

-- 3: ФИЛЬТР ПО ГРУППЕ
CREATE OR REPLACE FUNCTION get_contacts_by_group(p_group_name VARCHAR)
RETURNS TABLE(name VARCHAR, email VARCHAR, phones TEXT) AS $$
BEGIN
    RETURN QUERY
    SELECT c.name, c.email, COALESCE(string_agg(p.phone, ', '), 'Нет тел.')
    FROM contacts c JOIN groups g ON c.group_id = g.id LEFT JOIN phones p ON c.id = p.contact_id
    WHERE g.name ILIKE p_group_name GROUP BY c.id;
END;
$$ LANGUAGE plpgsql;

-- 4: ПАГИНАЦИЯ
CREATE OR REPLACE FUNCTION get_contacts_paginated(p_limit INT, p_offset INT)
RETURNS TABLE(id INT, name VARCHAR, email VARCHAR) AS $$
BEGIN
    RETURN QUERY SELECT c.id, c.name, c.email FROM contacts c ORDER BY c.id LIMIT p_limit OFFSET p_offset;
END;
$$ LANGUAGE plpgsql;

-- 5: СОРТИРОВКА (1-Имя, 2-ДР)
CREATE OR REPLACE FUNCTION get_sorted_contacts(sort_col INT)
RETURNS TABLE(name VARCHAR, email VARCHAR, birthday DATE) AS $$
BEGIN
    RETURN QUERY SELECT c.name, c.email, c.birthday FROM contacts c
    ORDER BY CASE WHEN sort_col = 1 THEN c.name END ASC, CASE WHEN sort_col = 2 THEN c.birthday END ASC;
END;
$$ LANGUAGE plpgsql;

-- 6: ЭКСПОРТ В JSON (Вся сборка JSON происходит в базе!)
CREATE OR REPLACE FUNCTION get_contacts_for_export() RETURNS JSON AS $$
BEGIN
    RETURN (SELECT json_agg(t) FROM (
        SELECT c.name, c.email, c.birthday, g.name as group, 
               array_agg(p.phone || ':' || p.type) FILTER (WHERE p.phone IS NOT NULL) as phones
        FROM contacts c LEFT JOIN groups g ON c.group_id = g.id LEFT JOIN phones p ON c.id = p.contact_id GROUP BY c.id, g.name
    ) t);
END;
$$ LANGUAGE plpgsql;

-- 9: ДОБАВИТЬ ТЕЛЕФОН
CREATE OR REPLACE PROCEDURE add_phone(p_name VARCHAR, p_phone VARCHAR, p_type VARCHAR) LANGUAGE plpgsql AS $$
BEGIN
    INSERT INTO phones (contact_id, phone, type) 
    SELECT id, p_phone, LOWER(p_type) FROM contacts WHERE name = p_name;
END;
$$;

-- 10: СМЕНИТЬ ГРУППУ
CREATE OR REPLACE PROCEDURE move_to_group(p_name VARCHAR, p_group_name VARCHAR) LANGUAGE plpgsql AS $$
BEGIN
    INSERT INTO groups (name) VALUES (p_group_name) ON CONFLICT (name) DO NOTHING;
    UPDATE contacts SET group_id = (SELECT id FROM groups WHERE name = p_group_name) WHERE name = p_name;
END;
$$;

-- 11: УМНОЕ УДАЛЕНИЕ (По имени ИЛИ телефону)
CREATE OR REPLACE PROCEDURE delete_contact_smart(p_target VARCHAR) LANGUAGE plpgsql AS $$
BEGIN
    DELETE FROM contacts WHERE name = p_target OR id IN (SELECT contact_id FROM phones WHERE phone = p_target);
END;
$$;