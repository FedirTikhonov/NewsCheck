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
    category_id INT REFERENCES category(id),
    article_id INT REFERENCES article(id),
    UNIQUE (category_id, article_id)
);

CREATE TABLE source(
    id SERIAL PRIMARY KEY,
    source_href VARCHAR(1023),
    source_num SMALLINT,
    article_id INT REFERENCES article(id)
);

CREATE TABLE paragraph(
    id SERIAL PRIMARY KEY,
    paragraph_text VARCHAR(1023),
    paragraph_num SMALLINT,
    article_id INT REFERENCES article(id)
);

CREATE TABLE metric(
    id SERIAL PRIMARY KEY,
    emotionality_score VARCHAR(255),
    emotionality_desc VARCHAR(1023),
    factuality_score SMALLINT,
    factuality_desc VARCHAR(1023),
    credibility_score SMALLINT,
    credibility_reason VARCHAR (1023),
    clickbaitness_score SMALLINT,
    clickbaitness_reason VARCHAR(1023),
    article_id INT REFERENCES article(id)
);