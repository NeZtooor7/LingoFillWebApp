-- Reference data required by registration and the interface language selectors.
-- Application data (users, sessions and exercises) is not imported.
INSERT INTO public.languages (code, name, original_name)
VALUES
    ('en', 'English', 'English'),
    ('es', 'Spanish', 'Español'),
    ('de', 'German', 'Deutsch'),
    ('ja', 'Japanese', '日本語'),
    ('hi', 'Hindi', 'हिन्दी'),
    ('ro', 'Romanian', 'Română'),
    ('it', 'Italian', 'Italiano'),
    ('pt', 'Portuguese', 'Português')
ON CONFLICT (code) DO NOTHING;
