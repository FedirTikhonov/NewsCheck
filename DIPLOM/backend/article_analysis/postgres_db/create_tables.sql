CREATE TABLE article(
    id SERIAL PRIMARY KEY,
    title VARCHAR(511),
    href VARCHAR(1023),
    outlet VARCHAR(255),
    published_at TIMESTAMPTZ,
    created_at TIMESTAMPTZ,
    STATUS VARCHAR(31)
);

CREATE TABLE category(
    id SERIAL PRIMARY KEY ,
    name VARCHAR(255),
    description VARCHAR(511)
);

CREATE TABLE factcheck_category(
    id SERIAL PRIMARY KEY ,
    category_id INT REFERENCES category(id) ON DELETE CASCADE,
    article_id INT REFERENCES article(id) ON DELETE CASCADE,
    UNIQUE (category_id, article_id)
);

CREATE TABLE source(
    id SERIAL PRIMARY KEY,
    source_href VARCHAR(1023),
    source_num SMALLINT,
    article_id INT REFERENCES article(id) ON DELETE CASCADE
);

CREATE TABLE paragraph(
    id SERIAL PRIMARY KEY,
    paragraph_text VARCHAR(2047),
    paragraph_num SMALLINT,
    article_id INT REFERENCES article(id) ON DELETE CASCADE
);

CREATE TABLE metric(
    id SERIAL PRIMARY KEY,
    emotionality_score VARCHAR(255),
    emotionality_reason VARCHAR(1023),
    factuality_score SMALLINT,
    factuality_reason VARCHAR(1023),
    credibility_score SMALLINT,
    credibility_reason VARCHAR (1023),
    clickbaitness_score SMALLINT,
    clickbaitness_reason VARCHAR(1023),
    article_id INT REFERENCES article(id) ON DELETE CASCADE
);

CREATE TABLE recommended_article (
    id SERIAL PRIMARY KEY,
    source_article_id INT REFERENCES article(id) ON DELETE CASCADE,
    recommended_article_id INT REFERENCES article(id) ON DELETE CASCADE,
    similarity_score FLOAT,
    last_updated TIMESTAMPTZ,
    UNIQUE (source_article_id, recommended_article_id)
);

CREATE TABLE weekly_report(
    id SERIAL PRIMARY KEY,
    digest_text TEXT,
    digest_date DATE
);

CREATE TABLE weekly_stats(
    id SERIAL PRIMARY KEY,
    category_id INT REFERENCES category(id) ON DELETE CASCADE,
    category_num INT,
    date DATE
);

INSERT INTO category(name, description) VALUES('Маніпуляції з військовими діями та втратами', 'Дезінформація про перебіг бойових дій, втрати сторін, стан військових підрозділів та процеси обміну полоненими з метою створення викривленої картини війни.');
INSERT INTO category(name, description) VALUES('Виправдання російської агресії', 'Спроби легітимізувати військові злочини РФ через фальшиві пояснення ракетних ударів по цивільних об''єктах, атак на мирне населення та початку війни загалом.');
INSERT INTO category(name, description) VALUES('Маніпуляції з політичними процесами', 'Викривлення інформації про політичних лідерів, виборчі процеси, міжнародні відносини та спроби легітимізації окупаційної влади на захоплених територіях.');
INSERT INTO category(name, description) VALUES('Дезінформація про міжнародну підтримку України', 'Фальсифікація даних про обсяги військової та економічної допомоги Україні, намагання дискредитувати міжнародну підтримку та створити враження її неефективності.');
INSERT INTO category(name, description) VALUES('Загальна російська пропаганда', 'Системна діяльність російських державних медіа та пропагандистів, спрямована на поширення наративів Кремля та формування потрібної РФ картини світу.');
INSERT INTO category(name, description) VALUES('Маніпуляції з громадською думкою та медіа', 'Використання фейкових опитувань, підроблених досліджень та атак на незалежні ЗМІ для формування потрібної суспільної думки та підриву довіри до об''єктивної інформації.');
INSERT INTO category(name, description) VALUES('Маніпуляції з історією та культурою', 'Перекручування історичних фактів, релігійних питань та культурних символів для виправдання агресії та створення псевдоісторичних підстав для територіальних претензій.');
INSERT INTO category(name, description) VALUES('Дезінформація про життя в Європі та туризм', 'Поширення неправдивої інформації про умови життя в ЄС, міграційні процеси та туристичні потоки з метою дискредитації європейських цінностей та створення ілюзії переваг життя в РФ.');
INSERT INTO category(name, description) VALUES('Спеціальні інформаційні операції', 'Цілеспрямовані кампанії з використанням вразливих груп населення (діти, меншини) та створення фейкових образів (диверсанти, екстремісти) для досягнення конкретних пропагандистських цілей.');
INSERT INTO category(name, description) VALUES('Геополітичні маніпуляції', 'Дезінформація про глобальний вплив РФ, міжнародні санкції, діяльність російських медіа за кордоном та кібербезпеку з метою перебільшення ролі Росії на світовій арені.');
