create database ai_services_prod;


-- insert Root User, password:BlooVo@145$a
INSERT INTO public.ai_service_apis_account ("password",last_login,is_superuser,username,first_name,last_name,email,is_staff,is_active,date_joined) VALUES
	 ('pbkdf2_sha256$260000$WMQxGCjk56iax0CbuAocQF$Lc67XNqhwxi0ECJHPIkgJpQCoGqqXNUi4flH3o4hHw8=','2021-10-05 10:22:34+03',true,'admin','admin','admin','admin@kabi.com',true,true,'2021-10-05 10:22:38+03');


CREATE TABLE public.job_position_details (
	id serial NOT NULL,
	job_title varchar(255) NULL,
	job_summary text NULL,
	job_qualifications _text NULL,
	job_responsibilities _text NULL,
	seniority_level varchar(255) NULL,
	country varchar(255) NULL,
	job_type varchar(255) NULL,
	sector varchar(255) NULL,
	functional_area varchar(255) NULL,
	content_language varchar NULL DEFAULT 'EN'::character varying,
	position_overview text NULL,
	required_skills _text NULL,
	required_education _text NULL,
	required_certificates _text NULL,
	similar_positions _json NULL,
	updated_at timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
	is_checked int4 NULL DEFAULT 0,
	CONSTRAINT job_position_job_position UNIQUE (job_title, seniority_level, country, job_type, sector, functional_area, content_language),
	CONSTRAINT job_position_pkey PRIMARY KEY (id)
);


CREATE TABLE public.dim_skills (
	id serial NOT NULL,
	skill_name text NULL,
	CONSTRAINT dim_skills_v1_key UNIQUE (skill_name),
	CONSTRAINT dim_skills_v1_pkey PRIMARY KEY (id)
);


CREATE TABLE public.dim_positions (
	id serial4 NOT NULL,
	position_name varchar(255) NULL,
	CONSTRAINT dim_positions_pkey PRIMARY KEY (id),
	CONSTRAINT dim_positions_position_name UNIQUE (position_name)
);

CREATE TABLE public.dim_educations (
	id serial4 NOT NULL,
	education_name varchar(255) NULL,
	CONSTRAINT dim_educations_education_name UNIQUE (education_name),
	CONSTRAINT dim_educations_pkey PRIMARY KEY (id)
);

CREATE TABLE public.dim_city (
    id SERIAL PRIMARY KEY,
    city_name_en varchar(255) NULL,
    city_name_ar varchar(255) NULL,
    country_name_en varchar(255) NULL,
    CONSTRAINT dim_city_city_name_en UNIQUE (city_name_en)
);

CREATE TABLE public.country_nationality_currency (
    id SERIAL PRIMARY KEY,
	country_name_ar varchar(255) NULL,
	country_name_en varchar(255) NULL,
	nationality_name_ar varchar(255) NULL,
	nationality_name_en varchar(255) NULL,
	currency_name_ar varchar(255) NULL,
	currency_name_en varchar(255) NULL,
	currency_code_en varchar(10) NULL,
	other_currency_codes text null,
	CONSTRAINT country_nationality_currency_country_name_en UNIQUE (country_name_en)
);