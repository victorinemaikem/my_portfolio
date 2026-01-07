"""
Django management command to seed the database with Victorine Maikem's portfolio content.
Run with: python manage.py seed_data
"""

from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import date
from portfolio.models import (
    SiteSettings, Service, Education, Experience, Certification,
    PortfolioCategory, PortfolioProject, BlogPost
)


class Command(BaseCommand):
    help = 'Seeds the database with Victorine Maikem portfolio content'

    def handle(self, *args, **options):
        self.stdout.write('🌱 Starting database seeding...\n')
        
        self.seed_site_settings()
        self.seed_services()
        self.seed_education()
        self.seed_experience()
        self.seed_certifications()
        self.seed_portfolio()
        self.seed_blog_posts()
        
        self.stdout.write(self.style.SUCCESS('\n✅ Database seeding completed successfully!'))

    def seed_site_settings(self):
        self.stdout.write('  → Seeding site settings...')
        
        settings, created = SiteSettings.objects.update_or_create(
            pk=1,
            defaults={
                'hero_greeting': 'Hello, My name is',
                'hero_name': 'Victorine Maikem',
                'hero_title': 'Digital Health Systems Builder | AI in Healthcare | Health Informatics',
                'hero_description': '''I build data-driven and AI-enabled health systems that work in the real world — across public health, clinical care, and research.

My work sits at the intersection of health informatics, data engineering, and machine learning, where technical decisions shape policy, workflows, and outcomes.''',
                'about_title': 'Building digital health systems that <span class="primary-clr">solve real problems.</span>',
                'about_description': '''I am a health informatics professional with a strong technical background, focused on how data, technology, and people come together within real health systems.

My work sits at the intersection of health informatics, data engineering, and applied AI. I'm interested not only in what technology can do, but in how it is designed, governed, and used in practice — particularly in public health, research, and clinical contexts where decisions carry real consequences.

Through experiences across academic institutions, public health organisations, and applied research initiatives, I've worked on digital health platforms, data pipelines, and AI-enabled tools that support decision-making at scale. These experiences have shaped how I approach my work: starting with system needs, understanding context and constraints, and building solutions that are responsible, usable, and sustainable.

I'm currently pursuing a Master of Health Informatics at the University of Toronto, where I continue to deepen my understanding of health systems, data governance, and the role of AI in improving care and population health. Across everything I do, I'm motivated by a simple principle — technology should strengthen trust, not complicate it.''',
                'footer_text': 'Victorine Maikem',
            }
        )
        self.stdout.write(self.style.SUCCESS(' Done'))

    def seed_services(self):
        self.stdout.write('  → Seeding services...')
        
        services_data = [
            {
                'title': 'Digital Health & Health Informatics Systems',
                'description': 'I design and evaluate digital health systems that support clinical care, public health, and research workflows. My work emphasizes interoperability, data governance, and usability — ensuring that technology aligns with real-world health system needs.',
                'order': 1,
            },
            {
                'title': 'Health Data Engineering & Analytics',
                'description': 'I work with complex, multi-source health datasets, building ETL pipelines, harmonizing data, and developing analytical dashboards that support evidence-based decision-making.',
                'order': 2,
            },
            {
                'title': 'Applied AI & Machine Learning in Healthcare',
                'description': 'I apply machine learning to health and public health problems where prediction, prioritization, or pattern recognition can meaningfully support decisions — with careful attention to model validity, ethics, and deployment context.',
                'order': 3,
            },
            {
                'title': 'Research & Knowledge Translation',
                'description': 'I support applied health and AI research by developing data platforms, analytical tools, and visual outputs that bridge technical, clinical, and policy audiences.',
                'order': 4,
            },
            {
                'title': 'Leadership & Program Coordination',
                'description': 'I contribute to and lead initiatives that build capacity in digital health and AI, coordinating stakeholders, mentoring emerging talent, and supporting program delivery in academic and public health settings.',
                'order': 5,
            },
        ]
        
        for data in services_data:
            Service.objects.update_or_create(
                title=data['title'],
                defaults=data
            )
        self.stdout.write(self.style.SUCCESS(' Done'))

    def seed_education(self):
        self.stdout.write('  → Seeding education...')
        
        education_data = [
            {
                'degree': 'Master of Health Informatics',
                'subtitle': 'MHI',
                'institution': 'University of Toronto — Dalla Lana School of Public Health',
                'start_date': date(2024, 9, 1),
                'end_date': date(2026, 6, 30),
                'description': 'Graduate training focused on the design, evaluation, and governance of digital health systems. Coursework and applied projects emphasize health data analytics, health information systems, AI in healthcare, decision support, and health systems integration.',
                'order': 1,
            },
            {
                'degree': 'Bachelor of Science (Honours)',
                'subtitle': 'First Class',
                'institution': 'African Leadership University',
                'start_date': date(2021, 1, 1),
                'end_date': date(2024, 6, 30),
                'description': 'Strong technical foundation in software engineering, data structures, machine learning, and systems development, complemented by leadership training and applied, project-based learning.',
                'order': 2,
            },
        ]
        
        for data in education_data:
            Education.objects.update_or_create(
                degree=data['degree'],
                institution=data['institution'],
                defaults=data
            )
        self.stdout.write(self.style.SUCCESS(' Done'))

    def seed_experience(self):
        self.stdout.write('  → Seeding experience...')
        
        experience_data = [
            {
                'organization': 'University of Toronto — Dalla Lana School of Public Health',
                'role': 'AI4PH Internship Lead',
                'start_date': date(2025, 11, 1),
                'end_date': None,
                'description': 'Supporting the coordination and delivery of applied AI for Public Health internships that connect students with partner organisations across academia, healthcare, and public health.',
                'order': 1,
            },
            {
                'organization': 'Africa Centres for Disease Control and Prevention (Africa CDC)',
                'role': 'Health Data Science Intern',
                'start_date': date(2025, 5, 1),
                'end_date': date(2025, 8, 31),
                'description': 'Worked within the Science & Innovation Directorate to support data-driven decision-making across research prioritisation and outbreak preparedness initiatives.',
                'order': 2,
            },
            {
                'organization': 'Digital Health Canada — AI in Action',
                'role': 'Volunteer Research Collaborator',
                'start_date': date(2025, 1, 1),
                'end_date': date(2025, 12, 31),
                'description': 'Contributed to a national collaborative initiative examining the real-world adoption of AI in clinical care across Canada.',
                'order': 3,
            },
            {
                'organization': 'Vanguard Economics Ltd.',
                'role': 'Database Developer Intern',
                'start_date': date(2023, 6, 1),
                'end_date': date(2023, 12, 31),
                'description': 'Supported backend system development and database optimisation for organisational data platforms.',
                'order': 4,
            },
            {
                'organization': 'Freelance',
                'role': 'Web & Software Developer',
                'start_date': date(2021, 6, 1),
                'end_date': None,
                'description': 'Alongside academic and institutional roles, worked independently on digital platforms for small organisations and businesses.',
                'order': 5,
            },
        ]
        
        for data in experience_data:
            Experience.objects.update_or_create(
                organization=data['organization'],
                role=data['role'],
                defaults=data
            )
        self.stdout.write(self.style.SUCCESS(' Done'))

    def seed_certifications(self):
        self.stdout.write('  → Seeding certifications...')
        
        certs_data = [
            {'title': 'Google & Kaggle Generative AI Intensive Course', 'issuer': 'Google & Kaggle', 'year': 2025, 'order': 1},
            {'title': 'Data Science in Precision Medicine', 'issuer': 'Stanford Online', 'year': 2025, 'order': 2},
            {'title': 'Fundamentals of Data-Driven Precision Medicine for Diabetes', 'issuer': 'Stanford Online', 'year': 2025, 'order': 3},
            {'title': 'HL7 FHIR Certification', 'issuer': 'HELINA', 'year': 2025, 'order': 4},
            {'title': 'Full Stack Development Nanodegree', 'issuer': 'Udacity', 'year': 2022, 'order': 5},
            {'title': 'Data Science & Machine Learning Bootcamp', 'issuer': 'Africa Agility', 'year': 2022, 'order': 6},
        ]
        
        for data in certs_data:
            Certification.objects.update_or_create(
                title=data['title'],
                defaults=data
            )
        self.stdout.write(self.style.SUCCESS(' Done'))

    def seed_portfolio(self):
        self.stdout.write('  → Seeding portfolio categories and projects...')
        
        # Create categories
        categories_data = [
            {'name': 'AI Healthcare', 'slug': 'ai-healthcare', 'order': 1},
            {'name': 'Data Engineering', 'slug': 'data-engineering', 'order': 2},
            {'name': 'Digital Health', 'slug': 'digital-health', 'order': 3},
            {'name': 'Research', 'slug': 'research', 'order': 4},
            {'name': 'Web Development', 'slug': 'web-development', 'order': 5},
        ]
        
        categories = {}
        for data in categories_data:
            cat, _ = PortfolioCategory.objects.update_or_create(
                slug=data['slug'],
                defaults=data
            )
            categories[data['slug']] = cat
        
        # Create projects
        projects_data = [
            {
                'title': 'Counterfeit Drug Detection System',
                'kicker': 'AI in Healthcare • Academic Capstone',
                'role': 'Project Lead',
                'description': 'Designed an AI-enabled system for counterfeit drug detection using chemical structure analysis, focusing on real-world usability and deployment. The system leverages machine learning to identify potentially harmful counterfeit medications before they reach patients.',
                'categories': ['ai-healthcare', 'research'],
                'is_featured': True,
                'order': 1,
            },
            {
                'title': 'Health Data Analytics Dashboard',
                'kicker': 'Data Engineering • Public Health',
                'role': 'Lead Developer',
                'description': 'Built comprehensive ETL pipelines and interactive dashboards for multi-source health datasets, enabling evidence-based decision-making for public health officials. Implemented data harmonization across disparate data sources.',
                'categories': ['data-engineering', 'digital-health'],
                'is_featured': True,
                'order': 2,
            },
            {
                'title': 'AI for Public Health Outbreak Preparedness',
                'kicker': 'Africa CDC • Research Initiative',
                'role': 'Data Science Intern',
                'description': 'Contributed to research prioritization and outbreak preparedness initiatives at Africa CDC, developing data-driven tools to support continental health security and rapid response capabilities.',
                'categories': ['ai-healthcare', 'research'],
                'is_featured': True,
                'order': 3,
            },
            {
                'title': 'Clinical Decision Support System',
                'kicker': 'Digital Health • Health Informatics',
                'role': 'System Designer',
                'description': 'Designed and evaluated a clinical decision support system emphasizing HL7 FHIR interoperability standards, ensuring seamless integration with existing healthcare workflows and EHR systems.',
                'categories': ['digital-health', 'ai-healthcare'],
                'is_featured': False,
                'order': 4,
            },
            {
                'title': 'Healthcare Provider Portal',
                'kicker': 'Web Development • Freelance',
                'role': 'Full Stack Developer',
                'description': 'Developed a secure, responsive web portal for healthcare providers featuring patient management, appointment scheduling, and secure messaging capabilities with full HIPAA compliance considerations.',
                'categories': ['web-development', 'digital-health'],
                'is_featured': False,
                'order': 5,
            },
            {
                'title': 'Research Data Platform',
                'kicker': 'Data Engineering • Academic',
                'role': 'Platform Developer',
                'description': 'Created a research data platform connecting technical, clinical, and policy audiences through intuitive data visualization and knowledge translation tools. Supports collaborative research workflows.',
                'categories': ['data-engineering', 'research'],
                'is_featured': False,
                'order': 6,
            },
        ]
        
        for data in projects_data:
            cat_slugs = data.pop('categories')
            project, _ = PortfolioProject.objects.update_or_create(
                title=data['title'],
                defaults=data
            )
            project.categories.set([categories[slug] for slug in cat_slugs])
        
        self.stdout.write(self.style.SUCCESS(' Done'))

    def seed_blog_posts(self):
        self.stdout.write('  → Seeding blog posts...')
        
        posts_data = [
            {
                'title': 'The Future of AI in Public Health: Lessons from Africa CDC',
                'slug': 'future-ai-public-health-africa-cdc',
                'author': 'Victorine Maikem',
                'excerpt': 'Reflecting on my experience at Africa CDC and the transformative potential of AI-driven health surveillance systems across the continent.',
                'content': '''Artificial Intelligence is reshaping how we approach public health challenges, particularly in resource-constrained settings. During my internship at Africa CDC's Science & Innovation Directorate, I witnessed firsthand how data-driven approaches can accelerate outbreak preparedness and response.

The key insight? Technology alone isn't enough. Successful AI implementation in public health requires deep understanding of local contexts, robust data governance frameworks, and genuine collaboration between technologists and health workers.

As we look ahead, the integration of AI in public health will depend on our ability to build systems that are not only technically sound but also ethically grounded and contextually appropriate.''',
                'published_date': timezone.now(),
                'comments_count': 12,
            },
            {
                'title': 'Bridging the Gap: Health Informatics in Clinical Practice',
                'slug': 'bridging-gap-health-informatics-clinical-practice',
                'author': 'Victorine Maikem',
                'excerpt': 'Exploring how health informatics professionals can better align digital tools with the realities of clinical workflows.',
                'content': '''One of the greatest challenges in digital health is the disconnect between what technology promises and what clinical practice demands. Too often, health IT systems are designed with technical elegance but fail to account for the messy reality of healthcare delivery.

Through my work on clinical decision support systems and EHR integrations, I've learned that successful health informatics requires starting with the clinical workflow, not the technology. We must understand how clinicians actually work, what information they need at the point of care, and how technology can support rather than disrupt their practice.

The path forward requires closer collaboration between informaticists, clinicians, and patients to build systems that truly serve healthcare's ultimate goal: better patient outcomes.''',
                'published_date': timezone.now(),
                'comments_count': 8,
            },
            {
                'title': 'Data Governance in Healthcare: Why It Matters More Than Ever',
                'slug': 'data-governance-healthcare-matters',
                'author': 'Victorine Maikem',
                'excerpt': 'As health data becomes increasingly valuable, establishing robust governance frameworks is essential for maintaining trust.',
                'content': '''The explosion of health data presents both tremendous opportunities and significant risks. From electronic health records to wearable devices, we're generating more health information than ever before. But without proper governance, this data can become a liability rather than an asset.

Effective data governance in healthcare encompasses privacy protection, data quality assurance, access management, and ethical use guidelines. It requires balancing the need for data sharing to advance research and care with the imperative to protect patient privacy and autonomy.

As we build increasingly sophisticated AI systems that depend on large datasets, the importance of data governance only grows. The systems we build today will shape healthcare for decades to come — we must ensure they're built on a foundation of trust.''',
                'published_date': timezone.now(),
                'comments_count': 15,
            },
        ]
        
        for data in posts_data:
            BlogPost.objects.update_or_create(
                slug=data['slug'],
                defaults=data
            )
        
        self.stdout.write(self.style.SUCCESS(' Done'))
