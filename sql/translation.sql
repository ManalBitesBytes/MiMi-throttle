CREATE TABLE dim_job_titles (
    id SERIAL PRIMARY KEY,
    job_title_normalized_en VARCHAR(1024) NOT NULL,
    job_title_display_en VARCHAR(1024) NOT NULL UNIQUE,
    job_title_normalized_ar VARCHAR(1024) NOT NULL,
    job_title_display_ar VARCHAR(1024) NOT NULL,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE dim_education_majors (
    id SERIAL PRIMARY KEY,
    education_display_en VARCHAR(1024) NOT NULL UNIQUE,
    education_normalized_en VARCHAR(1024) NOT NULL,
    education_display_ar VARCHAR(1024) NOT NULL,
    education_normalized_ar VARCHAR(1024) NOT NULL,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE dim_skills (
    id SERIAL PRIMARY KEY,
    skill_normalized_en VARCHAR(1024) NOT NULL UNIQUE,
    skill_display_en VARCHAR(1024) NOT NULL,
    skill_normalized_ar VARCHAR(1024) NOT NULL,
    skill_display_ar VARCHAR(1024) NOT NULL,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);