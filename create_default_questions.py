#!/usr/bin/env python3
"""
Create default_questions table and populate it with the 39 template questions
"""

from admin_app import admin_app, db
from sqlalchemy import Column, Integer, String, Text

# Define the DefaultQuestion model
class DefaultQuestion(db.Model):
    __tablename__ = 'default_questions'

    id = db.Column(db.Integer, primary_key=True)
    group_name = db.Column(db.String(100), nullable=False)
    question_text = db.Column(db.Text, nullable=False)
    question_type = db.Column(db.String(50), default='rating')
    display_order = db.Column(db.Integer, default=0)

def create_default_questions_table():
    with admin_app.app_context():
        # Create the table
        print('Creating default_questions table...')
        db.create_all()
        print('✓ Table created')

        # Clear existing data
        DefaultQuestion.query.delete()
        db.session.commit()
        print('✓ Cleared existing data')

        # Define the 39 questions
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

        print(f'\nInserting {len(questions_data)} default questions...')

        # Insert questions
        for order, group, text in questions_data:
            question = DefaultQuestion(
                id=order,
                group_name=group,
                question_text=text,
                question_type='rating',
                display_order=order - 1
            )
            db.session.add(question)

        db.session.commit()
        print(f'✓ Successfully inserted {len(questions_data)} questions!')

        # Print summary
        from sqlalchemy import func
        summary = db.session.query(
            DefaultQuestion.group_name,
            func.count(DefaultQuestion.id)
        ).group_by(DefaultQuestion.group_name).order_by(DefaultQuestion.group_name).all()

        print('\n' + '=' * 80)
        print('Summary by Group:')
        print('-' * 80)
        for group, count in summary:
            print(f'  • {group:<30} {count} questions')
        print('=' * 80)

        # Verify total
        total = DefaultQuestion.query.count()
        print(f'\nTotal questions in default_questions table: {total}')

if __name__ == '__main__':
    create_default_questions_table()
