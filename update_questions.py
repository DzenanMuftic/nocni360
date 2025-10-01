#!/usr/bin/env python3
"""
Script to update question table with new template questions
"""

from admin_app import admin_app, db, Question, Assessment
from datetime import datetime

def update_questions():
    with admin_app.app_context():
        # Delete all existing questions
        Question.query.delete()
        db.session.commit()
        print('All existing questions deleted.')

        # Find or create template assessment
        template_assessment = Assessment.query.filter_by(title='Template Assessment Questions').first()
        if not template_assessment:
            # Ensure we have at least one user and company for the template
            from admin_app import User, Company

            # Get or create system user
            system_user = User.query.filter_by(email='system@template.local').first()
            if not system_user:
                system_user = User(
                    email='system@template.local',
                    name='System Template',
                    role='admin',
                    is_active=False
                )
                db.session.add(system_user)
                db.session.flush()

            # Get or create system company
            system_company = Company.query.filter_by(name='System Template Company').first()
            if not system_company:
                system_company = Company(
                    name='System Template Company',
                    description='System company for template questions',
                    is_active=False
                )
                db.session.add(system_company)
                db.session.flush()

            # Create template assessment
            template_assessment = Assessment(
                title='Template Assessment Questions',
                description='Template containing predefined assessment questions - DO NOT DELETE',
                creator_id=system_user.id,
                company_id=system_company.id,
                created_at=datetime.utcnow(),
                is_active=False
            )
            db.session.add(template_assessment)
            db.session.commit()
            print('Created Template Assessment with system user and company')
        else:
            print(f'Using existing Template Assessment (ID: {template_assessment.id})')

        # Define questions
        questions_data = [
            (1, 'Odgovornost', 'Zadatke obavlja tačno i blagovremeno'),
            (2, 'Odgovornost', 'Prihvata odgovornost za lični uspeh'),
            (3, 'Odgovornost', 'Preuzima odgovornost za neuspjehe'),
            (4, 'Odgovornost', 'Pokazuje dosljednost u riječima i na djelu'),
            (5, 'Odgovornost', 'Postavlja visoka očekivanja za sebe'),
            (6, 'Fokus na klijenta', 'Traži načine za dodavanje vrijednosti izvan očekvanja klijenata'),
            (7, 'Fokus na klijenta', 'Istražuje i bavi se neutvrdjenim, temeljnim i dugoročnim potrebama klijenata'),
            (8, 'Fokus na klijenta', 'Poboljšava sistem i proces pružanja usluga klijentima'),
            (9, 'Fokus na klijenta', 'Predviđa buduće potrebe i brige klijenata'),
            (10, 'Komunikacija', 'Prilagođava komunikaciju publici'),
            (11, 'Komunikacija', 'Pruža efikasne, visokokvalitetne prezentacije'),
            (12, 'Komunikacija', 'Efikasno koristi metode neverbalne komunikacije'),
            (13, 'Komunikacija', 'Dijeli odgovarajuću količinu informacija'),
            (14, 'Komunikacija', 'Profesionalno podnosi kritike'),
            (15, 'Usluge klijentima', 'Aktivno sluša klijente'),
            (16, 'Usluge klijentima', 'Odgovara na zahtjeve klijenata'),
            (17, 'Usluge klijentima', 'Profesionalno i ljubazno rješava pritužbe klijenata'),
            (18, 'Usluge klijentima', 'Pokazuje empatiju i razumijevanje prema klijentima'),
            (19, 'Usluge klijentima', 'Komunicira zahtjeve klijenata menadžmentu na odgovarajući način'),
            (20, 'Strateško razmišljanje', 'Predviđa dugoročne implikacije predloženih rješenja'),
            (21, 'Strateško razmišljanje', 'Prosudjuje razumno u novim situacijama'),
            (22, 'Strateško razmišljanje', 'Identificira i razmatra nove mogućnosti i rizike'),
            (23, 'Strateško razmišljanje', 'Pruža nove informacije ili podatke za ključnu odluku'),
            (24, 'Strateško razmišljanje', 'Pokazuje pronicljivo razumijevanje organizacijskog konteksta i prioreta'),
            (25, 'Timski rad', 'Odaje priznanje i priznaje doprinose i napore drugih članova tima'),
            (26, 'Timski rad', 'Ulaže izuzetne napore da pomogne članovima tima'),
            (27, 'Timski rad', 'Njeguje timski duh'),
            (28, 'Timski rad', 'Osigurava da svi članovi grupe imaju priliku da doprinesu grupnim diskusijama'),
            (29, 'Timski rad', 'Pomaže u izgradnji konsenzusa među članovima tima'),
            (30, 'Rješavanje problema', 'Pristupa složenim problemima tako što ih dijeli na komponente kojima se može upravljati'),
            (31, 'Rješavanje problema', 'Identifikuje optimalna rješenja važući prednosti i mane alternativnih pristupa'),
            (32, 'Rješavanje problema', 'Identificira i traži informacije potrebne za rješavanje problema'),
            (33, 'Rješavanje problema', 'Predviđa moguće negativne ishode odluka'),
            (34, 'Rješavanje problema', 'Nakon implementacije, ocjenjuje učinkovitost i efikasnost rešenja'),
            (35, 'Upravaljanje vremenom', 'Prikladno određuje prioritete zadataka prema važnosti i vremenskom ograničenju'),
            (36, 'Upravaljanje vremenom', 'Precizno predviđa vrijeme potrebno za završetak zadatka'),
            (37, 'Upravaljanje vremenom', 'Koristi sisteme za upravljanje projektima i kalendare za organizaciju vremena'),
            (38, 'Upravaljanje vremenom', 'Uvijek je svjestan statusa svih dodijeljenih zadataka'),
            (39, 'Upravaljanje vremenom', 'Redovno obavještava druge o statusu zadatka'),
        ]

        # Add questions
        for order, group, text in questions_data:
            question = Question(
                assessment_id=template_assessment.id,
                question_text=text.strip(),
                question_group=group.strip(),
                question_type='rating',
                order=order - 1
            )
            db.session.add(question)

        db.session.commit()
        print(f'Successfully added {len(questions_data)} questions!')

        # Print summary
        from sqlalchemy import func
        summary = db.session.query(Question.question_group, func.count(Question.id)).filter_by(assessment_id=template_assessment.id).group_by(Question.question_group).order_by(Question.question_group).all()
        print('\nQuestions by group:')
        for group, count in summary:
            print(f'  - {group}: {count} questions')

if __name__ == '__main__':
    update_questions()
