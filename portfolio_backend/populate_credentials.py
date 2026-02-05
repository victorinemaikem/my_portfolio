"""
Script to populate Credentials section data from resume.
Run with: python manage.py shell < populate_credentials.py
"""
import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'portfolio_backend.settings')
django.setup()

from portfolio.models import Language, Certification, Hackathon, Conference, LeadershipActivity
from datetime import date

# Clear existing data (optional - comment out if you want to keep existing)
# Language.objects.all().delete()
# Hackathon.objects.all().delete()
# Conference.objects.all().delete()
# LeadershipActivity.objects.all().delete()

# ========================================
# LANGUAGES
# ========================================
languages_data = [
    {'name': 'English', 'proficiency': 'native', 'flag_code': 'us', 'order': 1},
    {'name': 'French', 'proficiency': 'fluent', 'flag_code': 'fr', 'order': 2},
]

for lang in languages_data:
    Language.objects.get_or_create(
        name=lang['name'],
        defaults={
            'proficiency': lang['proficiency'],
            'flag_code': lang['flag_code'],
            'order': lang['order'],
            'is_active': True
        }
    )
print(f"✓ Created {len(languages_data)} languages")

# ========================================
# CERTIFICATIONS (Update existing + add new)
# ========================================
certifications_data = [
    {
        'title': 'Stanford Data Science in Precision Medicine and Cloud Computing',
        'issuer': 'Stanford University',
        'year': 2025,
        'description': 'Advanced training in precision medicine and cloud computing for healthcare applications.',
        'order': 1
    },
    {
        'title': 'HL7 FHIR Training Program',
        'issuer': 'HELINA',
        'year': 2025,
        'description': 'Health Level 7 Fast Healthcare Interoperability Resources standard training.',
        'order': 2
    },
    {
        'title': 'Gen AI Intensive Course',
        'issuer': 'Google & Kaggle',
        'year': 2025,
        'description': 'Intensive generative AI training program.',
        'order': 3
    },
    {
        'title': 'Full Stack Development Nanodegree',
        'issuer': 'Udacity',
        'year': 2022,
        'description': 'Comprehensive full-stack web development program.',
        'order': 4
    },
    {
        'title': 'Data Science & Machine Learning Bootcamp',
        'issuer': 'Africa Agility',
        'year': 2022,
        'description': 'Intensive bootcamp covering data science and machine learning fundamentals.',
        'order': 5
    },
]

for cert in certifications_data:
    Certification.objects.update_or_create(
        title=cert['title'],
        defaults={
            'issuer': cert['issuer'],
            'year': cert['year'],
            'description': cert.get('description', ''),
            'order': cert['order'],
            'is_active': True
        }
    )
print(f"✓ Created/updated {len(certifications_data)} certifications")

# ========================================
# CONFERENCES
# ========================================
conferences_data = [
    {
        'name': 'Canadian Pain Society Annual Conference',
        'date': date(2025, 5, 1),
        'location': 'Canada',
        'role': 'attendee',
        'description': 'Enabled hybrid knowledge sharing at a national healthcare conference.',
        'order': 1
    },
]

for conf in conferences_data:
    Conference.objects.get_or_create(
        name=conf['name'],
        defaults={
            'date': conf['date'],
            'location': conf['location'],
            'role': conf['role'],
            'description': conf.get('description', ''),
            'order': conf['order'],
            'is_active': True
        }
    )
print(f"✓ Created {len(conferences_data)} conferences")

# ========================================
# LEADERSHIP ACTIVITIES
# ========================================
leadership_data = [
    {
        'title': 'One Million Leaders Africa Fellow',
        'organization': 'One Million Leaders Africa',
        'activity_type': 'fellowship',
        'start_date': date(2022, 1, 1),
        'end_date': date(2023, 12, 31),
        'description': 'Completed global leadership program focused on African youth development.',
        'order': 1
    },
    {
        'title': 'Aspire Leaders Program',
        'organization': 'Aspire Leaders Institute',
        'activity_type': 'fellowship',
        'start_date': date(2022, 1, 1),
        'end_date': date(2022, 12, 31),
        'description': 'Global leadership and professional development fellowship.',
        'order': 2
    },
    {
        'title': 'McKinsey Forward Program',
        'organization': 'McKinsey & Company',
        'activity_type': 'training',
        'start_date': date(2023, 1, 1),
        'end_date': date(2023, 6, 30),
        'description': 'Strategy and leadership training program by McKinsey.',
        'order': 3
    },
    {
        'title': 'UPG Sustainability Fellowship',
        'organization': 'UPG',
        'activity_type': 'fellowship',
        'start_date': date(2023, 1, 1),
        'end_date': date(2023, 12, 31),
        'description': 'Sustainability-focused leadership and impact program.',
        'order': 4
    },
    {
        'title': 'Chairperson, ALU Christian Fellowship',
        'organization': 'African Leadership University',
        'activity_type': 'mentoring',
        'start_date': date(2022, 1, 1),
        'end_date': date(2023, 12, 31),
        'description': 'Led campus-wide faith-based events for 500+ students.',
        'order': 5
    },
    {
        'title': 'Microsoft Learn Student Ambassador',
        'organization': 'Microsoft',
        'activity_type': 'mentoring',
        'start_date': date(2022, 1, 1),
        'end_date': None,
        'description': 'Facilitated technical workshops and peer mentorship.',
        'order': 6
    },
    {
        'title': 'Community Health Volunteer',
        'organization': 'Zoe Health Foundation & Welisane Foundation',
        'activity_type': 'volunteering',
        'start_date': date(2020, 1, 1),
        'end_date': None,
        'description': 'Supporting community health advocacy and outreach initiatives.',
        'order': 7
    },
]

for activity in leadership_data:
    LeadershipActivity.objects.get_or_create(
        title=activity['title'],
        defaults={
            'organization': activity['organization'],
            'activity_type': activity['activity_type'],
            'start_date': activity['start_date'],
            'end_date': activity['end_date'],
            'description': activity.get('description', ''),
            'order': activity['order'],
            'is_active': True
        }
    )
print(f"✓ Created {len(leadership_data)} leadership activities")

print("\n✅ Credentials data populated successfully!")
